import pandas as pd
import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path

#Todo: 
#Make this work with a folder of excel files and output a folder of xml file
#Make it only create an element if the value is not empty (currently it creates an empty element)
#Make it output a geojson file with the building info (the last 3 tabs of the excel file)
#Find a way to make this work with a boarder range of programs to make this into an app 

class Converter:

    def __init__(self, input_file, output_file, xml_key_sheet):
        print(f"Initializing Converter with input_file: {input_file}, output_file: {output_file}, xml_key_sheet: {xml_key_sheet}")
        self.input_file = input_file
        self.output_file = output_file
        self.xml_key_sheet = xml_key_sheet
        self.data = {}
        self.xml_key = None
        self.key_tree = None

    def load_workbook(self):
        """This function loads the excel workbook and separate the XML key sheet from the rest of the data in order to start the conversion
            @param string filename: a reference for the excel sheet that we want to convert into an xml
            returns: the sheets we want to extract data from and the xml key individually"""

        print(f"Loading: {self.input_file}") #prints the name of the sheet we are loading
        sheets = pd.read_excel(self.input_file,sheet_name=None)#puts that sheet into pandas

        for sheet_name,df in sheets.items():
            # Strip whitespace from column headers
            df.columns = df.columns.str.strip()

        #If we do not find a xml key sheet
        if self.xml_key_sheet not in sheets:
            raise ValueError(f"Workbook must contain a '{self.xml_key_sheet}' sheet") #we print an error

        #separate XML configuration sheet from the rest of the data
        xml_key = sheets.pop(self.xml_key_sheet)

        return sheets,xml_key

    def clean_xml_key(self, xml_key):
        """This function cleans the xml key so that we have no error in the conversion process
        @params string xml_key: a reference to the excel sheet that has the xml key
        @returns a cleaned xml key that has no empty values or whitespace"""
        
        #Remove completely empty rows
        xml_key = xml_key.dropna(how="all").copy()

        #Replace NaN with all empty strings
        xml_key = xml_key.fillna("")

        #Strip whitespace from string columns
        for column in xml_key.columns:
            xml_key[column] = xml_key[column].apply(lambda x:x.strip() if isinstance(x,str) else x)
        return xml_key

    def parse_header(self, header):
        """This functions parses through our source_column column of our spreadsheet and separates out units to be added to the xml_header as it's own variable
            @params string header: the column header that contains both the name and the value
            @returns: the new header with the name and the unit header"""

        header = str(header).strip() #Strip the header of any unnecessary spaces or characters 
        match = re.match(r"^(.*?)\s*\((.*?)\)\s*$",header) #reader the header as is and do not interoperate any special characters

        #When we get a header that has units and a name separate the two 
        if match:
            name = match.group(1).strip()
            unit = match.group(2).strip()

            return name,unit
        
        return header,None #return the new header

    def build_key_tree(self,xml_key):
        """This function builds a tree structure from the xml key sheet, which is used to generate the XML file
            @params string xml_key: a reference to the excel sheet that has the xml key
            @returns: a tree structure of the xml key"""

        root_row = self.get_root(xml_key)
        root_node = {"config": root_row, "children": []}

        # stack of (tag_name, node) - the top of the stack is the nearest
        # open node whose tag a subsequent row could declare as its Parent
        stack = [(str(root_row["XML_Tag"]).strip(), root_node)]

        for idx, row in xml_key.iterrows():
            if idx == root_row.name:
                continue #skip the root row itself, already handled above

            tag = str(row["XML_Tag"]).strip() #we get the tag from the row and strip any whitespace
            parent_tag = str(row["Parent"]).strip() #we get the parent tag from the row and strip any whitespace

            # Pop back up the stack until we find the specific open node that  matches this row's declared parent tag - this is what correctly scopes reused tag names to the right occurrence.
            while len(stack) > 1 and stack[-1][0] != parent_tag:
                stack.pop()

            if stack[-1][0] != parent_tag:
                raise ValueError(f"Could not find parent '{parent_tag}' for tag '{tag}' "f"(row {idx}) - check the ordering/spelling in Data_Key. "f"Data_Key rows must be listed in depth-first order.")

            node = {"config": row, "children": []} #we create a new node with the given row and an empty list of children
            stack[-1][1]["children"].append(node) #we add the new node to the children of the parent node

            # This node is now itself a candidate parent for whatever rows
            # come next in the sheet.
            stack.append((tag, node))

        return root_node

    def get_root(self, xml_key):
        """This function gets the root tag of the xml file and returns it
            @params string xml_key: a reference to the excel sheet that has the xml key
            @returns: the root tag of the xml file"""
        
        roots = xml_key[xml_key["Parent"] == ""] #set the roots to be the rows that have no parent tag, which should be the root tag of the xml file

        #If we do not find a root tag, we raise an error
        if len(roots) != 1:
            raise ValueError("XML key must contain exactly one root tag")
        
        return roots.iloc[0] #return the root tag

    def get_value(self, row, column):
        """This function gets the value of a given column in a given row and returns it
            @params string row: a reference to the row we want to get the value from
            @params string column: a reference to the column we want to get the value from
            @returns: the value of the given column in the given row"""

            #If our column is not in the row, we raise an error
        if column not in row:
            print("\nERROR FINDING COLUMN")
            print(f"Looking for: '{column}'")
            print(f"Available columns:")
            for col in row.index:
                print(f"  '{col}'")
            print(f"Row data:")
            print(row)
            
            raise ValueError(f"Column '{column}' not found in row")
            
        value = row[column] #we get the value of the given column in the given row

        #if the value is NaN, we return None
        if pd.isna(value):
            return None
        
        return value #returns the value of the given column in the given row

    def create_value_element(self, parent_element, row, config):
        """This function creates a new xml element with the given parent, row, and config
            @params string parent_element: a reference to the parent element we want to create the new element under
            @params string row: a reference to the row we want to get the value from
            @params string config: a reference to the configuration for the given tag
            @returns: the new xml element"""

        tag = config["XML_Tag"] #we get the tag from the config
        source_column = config["Source_Column"] #we get the source column from the config

        value = self.get_value(row, source_column) #we get the value from the row and source column

        _,unit = self.parse_header(source_column)  #Parse the unit from Excel header

        #create attributes
        attributes = {}

        if unit:
            attributes["unit"] = unit #we add the unit to the attributes

        #Create XML element
        element = ET.SubElement(parent_element,tag,attrib=attributes) #we create the new xml element with the given tag and attributes

        #If the excel cell is empty, we do not add any text to the xml element
        if value is None:
            element.text = None
        elif isinstance(value,float) and value.is_integer():
            element.text = str(int(value))
        else:
            element.text = str(value) #we add the value to the xml element as text

        return element #returns the new xml element

    def create_repeating_values(self, parent_element, row, config, children=None):
        """This function creates a new xml element with the given parent, row, and config for repeating values
            @params string parent_element: a reference to the parent element we want to create the new element under
            @params string row: a reference to the row we want to get the value from
            @params string config: a reference to the configuration for the given tag
            @params list children: optional list of child tree-nodes for this 'list' node. If
                present, each split value is wrapped: <tag><child_tag>item</child_tag></tag>
                (e.g. <energy_emitter_system><emitter_system_id>1</emitter_system_id></energy_emitter_system>)
                instead of being emitted as a flat, unwrapped <tag>item</tag> per value.
            @returns: a list of new xml elements"""
        
        tag = config["XML_Tag"] #we get the tag from the config
        source_column = config["Source_Column"] #we get the source column from the config

        value = self.get_value(row,source_column) #we get the value from the row and source column

        if value is None:
            return #If the value is None, we return an empty object

        value = str(value).strip() #we convert the value to a string

        if(value.startswith("[") and value.endswith("]")): #If the value starts with a [ and ends with a ], we remove them
            value = value[1:-1]

        values = value.split(",") #we split the value by commas

        #Parse the unit from Excel header
        _,unit = self.parse_header(source_column)
        attributes = {}

        if unit:
            attributes["unit"] = unit #we add the unit to the attributes

        #If this list node has a child defined in the Data_Key (e.g. 'emitter_system_id' under 'energy_emitter_system'), wrap each value in <tag><child_tag>item</child_tag></tag>
        if children:
            child_tag = children[0]["config"]["XML_Tag"] #we get the child tag from the first child in the children list
            for item in values:
                item = item.strip() #we strip any whitespace from the item
                if item == "": 
                    continue #If the item is empty, we skip it
                wrapper = ET.SubElement(parent_element,tag) #we create a new xml element with the given parent and tag
                child_element = ET.SubElement(wrapper,child_tag,attrib=attributes) #we create a new xml element with the given wrapper, child tag, and attributes
                child_element.text = item #we add the item to the child element as text
            return

        #Otherwise, fall back to the original flat behaviour (one <tag>item</tag> per value)
        for item in values:
            item = item.strip()
            if item == "":
                continue
            try:
                as_float = float(item) # Attempt to convert the item to a float
                if as_float.is_integer(): # If the float is an integer, convert it to an int and then to a string
                    item = str(int(as_float)) # If the float is not an integer, keep it as a float and convert it to a string
            except ValueError: 
                pass  # If conversion fails, keep item as string
            element = ET.SubElement(parent_element,tag,attrib=attributes)
            element.text = item

    def find_related_rows(self, data, source_sheet, relationship, parent_value):
        """This function finds the related rows in a given source sheet based on the relationship and parent value
            @params string data: a reference to the data we want to find the related rows in
            @params string source_sheet: a reference to the source sheet we want to find the related rows in
            @params string relationship: a reference to the relationship we want to use to find the related rows
            @params string parent_value: a reference to the parent value we want to use to find the related rows
            @returns: a dataframe of the related rows"""
        
        #If the source sheet is not in the data, we raise an error
        if source_sheet not in data:
            raise ValueError(f"Source sheet '{source_sheet}' was not found in workbook")

        dataframe = data[source_sheet] #we get the dataframe for the source sheet

        #If the relationship column is not in the dataframe, we raise an error
        if relationship not in dataframe.columns:
            raise ValueError(f"Relationship column '{relationship}' was not found in sheet '{source_sheet}'") 
    
        return dataframe[dataframe[relationship] == parent_value] #we return the related rows in the dataframe

    def build_node(self, parent_element, node, row, data):
        """This function builds the xml node for a given tree node and row
            @params parent_element: the parent element we want to create the new element under
            @params node: the tree node (from build_key_tree) - {"config": row, "children": [...]}
            @params row: a reference to the row we want to get the value from
            @params data: a reference to the workbook sheets (for repeating/value lookups)
            @returns: None"""

        config = node["config"]
        tag = config["XML_Tag"] #we get the tag from the config
        node_type = config["Node_Type"] #we get the node type from the config

        match node_type: #we switch on the node type
            case "value":
                source_sheet = config["Source_Sheet"] #we get the source sheet from the config
                source_column = config["Source_Column"] #we get the source column from the config

                #if the row is not None and the source column is in the row index, we create the value element
                if row is not None and source_column in row.index:
                    self.create_value_element(parent_element,row,config)
                elif source_sheet in data: #if the source sheet is in the data, we get the first row of the source sheet and create the value element
                    source_data = data[source_sheet]
                    if len(source_data) > 0:
                        source_row = source_data.iloc[0]
                        self.create_value_element(parent_element,source_row,config)
                else:
                    raise ValueError(f"Source sheet '{source_sheet}'"f"was not found for XML tag '{tag}'") #if non of the above conditions are met, we raise an error
                return
            case "list":
                if row is None:
                    return
                self.create_repeating_values(parent_element,row,config,node["children"]) #if the node type is a list, we create the new xml elements for the repeating values
                return
            case "container":
                element = ET.SubElement(parent_element,tag) #if the node type is a container, we create a new xml element with the given parent and tag

                #We iterate through the children (from the tree, not a name lookup) and build the xml nodes for each
                for child in node["children"]:
                    self.build_node(element,child,row,data)
            case "repeating":
                source_sheet = config["Source_Sheet"]
                relationship = config["Relationship"]

                if source_sheet not in data:
                    raise ValueError(
                        f"Source sheet '{source_sheet}' was not found in workbook"
                    )

                source_data = data[source_sheet]

                # If there is no parent row, repeat every row in the sheet
                if row is None:
                    for _, child_row in source_data.iterrows():
                        element = ET.SubElement(parent_element,tag)

                        for child in node["children"]:
                            self.build_node(element,child,child_row,data)
                    return
                
                # If this is a relationship-based repeating node, use the relationship to find matching child rows.
                if relationship and relationship in row.index:
                    parent_value = self.get_value(row,relationship) #we get the parent value from the row and relationship

                    if parent_value is None:
                        return

                    related_rows = self.find_related_rows(data,source_sheet,relationship,parent_value) #we find the related rows in the source sheet based on the relationship and parent value

                else:
                    related_rows = source_data   # The relationship column does not exist in the  current parent row, so don't try to use it as a parent relationship.

                # Build the repeating XML elements
                for _, child_row in related_rows.iterrows():
                    element = ET.SubElement(parent_element,tag)
                    for child in node["children"]:
                        self.build_node(element,child,child_row,data)
                return
            case default:
                raise ValueError(f"Unknown node type '{node_type}' for tag '{tag}'") #if the node type is unknown, we raise an error

    def build_xml(self):
        """This function builds the xml file for the given data and xml key
            @params data: a reference to the data we want to build the xml file for
            @params xml_key: a reference to the configuration for the given tag
            @returns: the root element of the xml file
        """
        tree = self.build_key_tree(self.xml_key) #build the actual tree once, so reused tag names don't get merged together

        root_config = tree["config"] #we get the root configuration
        root_tag = root_config["XML_Tag"] #we get the root tag from the root configuration

        # Create root element
        root_element = ET.Element(root_tag)

        #we iterate through the children of the root and build the xml nodes for each child
        for child in tree["children"]:

            tag = child["config"]["XML_Tag"]
            node_type = child["config"]["Node_Type"]

            if node_type == "repeating":
                source_sheet = child["config"]["Source_Sheet"]
                if source_sheet not in self.data:
                    raise ValueError(f"Source sheet '{source_sheet}' "f"was not found in workbook")
                dataframe = self.data[source_sheet]

                # Build one XML object for every row
                for _, row in dataframe.iterrows():
                    self.build_node(root_element,child,row,self.data)
            elif node_type == "container":
                self.build_node(root_element,child,None,self.data)
            else:
                raise ValueError(f"Unsupported root node type "f"'{node_type}' for tag '{tag}'")
        return root_element

    def save_xml(self, root_element, filename):
        """This function saves the xml file for the given root element and filename
            @params string root_element: a reference to the root element of the xml file
            @params string filename: a reference to the filename we want to save the xml file as"""
        tree = ET.ElementTree(root_element) #we create the xml tree with the given root element
        ET.indent(tree, space="    ") #we indent the xml tree for readability

        tree.write(filename, encoding="utf-8", xml_declaration=True) #we write the xml tree to the given filename
        print(f"created: {filename}") #we print the name of the file we saved the xml to

    def convert(self):
        """This function converts the excel sheet to an xml file"""
        self.data, self.xml_key = self.load_workbook() #we load the workbook and get the data and xml key
        self.xml_key = self.clean_xml_key(self.xml_key) #we clean the xml key
        root_element = self.build_xml() #we build the xml file
        print(f"Saving: {self.output_file}") #we print the name of the file we are saving the xml to
        self.save_xml(root_element, self.output_file) #we save the xml file

