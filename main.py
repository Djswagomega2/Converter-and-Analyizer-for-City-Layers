from Converter import Converter

def main():
    """This function is the main function that runs the converter"""
    converter = Converter(input_file, output_file, xml_key_sheet) #we create a converter object
    converter.convert() #we convert the excel sheet to an xml file

input_file = "_Data Template for AI M&V + City Layers.xlsx"
output_file = "Exported_XML.xml"
xml_key_sheet = "Data_Key"

if __name__ == "__main__":
    main()
