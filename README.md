# Purpose 

The purpose of this document is to provide guidance on how to effectively use the Excel data template to enter building data simulation in the City Layers tool. 

# How Data is Handled 

The Data Structure of the Template 

Data is organized hierarchically, moving from the most specific components—such as materials, electricity generation, and energy storage—to the most general level, including systems that combine these components and overarching energy system archetypes. Which can be shown below in this diagram. 



<!-- Start of picture text -->
Materials<br>Non PV/PY Energy Emitter<br>Generation Seton<br>‘One (Reference by ID) Components<br>Insulation Physical<br>[_rsain StorageSone fone or On<br>one one<br>‘by(Reference Thermal [by(Reference Thermal<br>SterageiD)* | Storagea 0) ‘One or Multiple<br>Storage Medium | —on. Thermal Storage Distributi<br>on lone oF On<br>°<br>Muttple<br>Energy System Archetype<br><!-- End of picture text -->

As shown in the diagram, the **ID is the key element of each component section** because it is used to connect and reference data across different sections of the system. For example, materials are referenced by their ID when creating **Insulation and Physical** 

**Characteristics Data** , which is then referenced by ID within **Thermal Storage** . Therefore, it is important that each ID correctly matches the data being entered so that the simulation can accurately identify and build the intended system. 

Some sections can also accept **multiple data points** for the simulation reference. This allows the data template to account for and represents **multiple scenarios** within the same system, providing greater flexibility when configuring and analyzing different system conditions. 

Since simulation data is referenced by ID, each component of the system must be **<u>AS GENERALIZED AS POSSIBLE.</u>** This means if you have multiple of the same components (ex. Heating Coils, Air Handling Units, etc.) it most only be inputted as a single a single generalized object that approximated the average of all the components combined or else the simulation my not work. 

## **How the data gets converted into XML:** 

The Data_Key is the main source of information used to turn our excel spreadsheet into an XML file that is readable by the City Layers program. Each row in the Data_Key represents a specific XML element and provides the converter with the information it needs to create that element. The sheet is organized around several key columns: 

- XML Tag — identifies the name of the XML element that will be created. 

- Parent — identifies the XML element that the current element belongs under. This establishes the hierarchy and determines where each element is placed within the XML file. 

- Node Type — identifies how the converter should handle the element. The available node types are value, list, container, and repeating. 

- Source Sheet — identifies which sheet in the Excel workbook contains the information associated with the XML element. 

- Source Column — identifies the specific column within the source sheet where the value should be obtained. 

- Relationship — identifies the relationship used to connect information between different sheets when the XML structure depends on related records. 

Together, these columns provide the converter with the instructions necessary to locate the appropriate data, determine how it should be handled, and place it in the correct location within the XML hierarchy. 

## **Node Types:** 

The Node Type column is particularly important because it determines how the converter handles the information associated with each XML tag. 

- Value — represents a single piece of information that is placed into an XML element. 

- List — represents multiple values that belong to the same section and need to be processed individually. 

- Container — represents a section that groups other XML elements together but does not directly contain a value from the Excel workbook. 

- Repeating — represents a section that can occur multiple times, with each occurrence being created from a separate data record. 

The Data_Key therefore acts as the connection between the structure of the Excel workbook and the structure expected by City Layers, allowing the converter to determine not only where information comes from, but also how that information should be organized. 

# What needs to be filled in 

When filling out your data within the excel spreadsheet, it is important to pay attention to columns **<u>highlighted in red</u>** <u>as those sections</u> **<u>MUST BE FILLED</u>** for the program to work. Columns **<u>highlighted in blue</u>** <u>are optional and can be filled in at the user's desecration.</u> Below you can find each section of the spreadsheet in text, their contents, and what needs to be filled **<u>highlighted in red</u>** <u>as well as what data type those required fields are.</u> 

Materials: 

- **Material ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- solar absorptance 

- thermal absorptance 

- visible absorptance 

- no mass 

- thermal resistance 

- density 

- specific heat 

- **Conductivity – Decimal Number (Required)** 

## Non-PV Generation Component: 

- **Generation System ID-Whole Number (Required)** 

- **Name – Text (Required)** 

- **System Type - Text (Required)** 

- Model Name 

- Manufacturer 

- **Fuel Type (Required) - Text** 

- Source Medium 

- Supply Medium 

- **Heat Efficiency - Decimal Number (Required)** 

- Nominal Heat Output 

- Minimum Heat Input 

- Maximum Heat Output 

- Cooling Efficiency 

- Cooling Energy Input Ratio 

- Nominal Cooling Output 

- Minimum Cooling Input 

- Maximum Cooling Output 

- Electricity Efficiency 

- Nominal Electricity Output 

- Minimum Heat Source Temperature 

- Maximum Heat Source Temperature 

- Minimum Heat Supply Temperature 

- Maximum Heat Supply Temperature 

- Minimum Cooling Source Temperature 

- Maximum Cooling Source Temperature 

- Minimum Cooling Supply Temperature 

- Maximum Cooling Supply Temperature 

- Minimum Source Mass Flow Rate 

- Maximum Source Mass Flow Rate 

- Minimum Supply Mass Flow Rate 

- Maximum Supply Mass Flow Rate 

- Heat Output Curve 

- Heat Fuel Consumption Curve 

- Heat Efficiency Curve 

- Heat Energy Input Ratio Curve 

- Partial Load Fraction Heat Energy Input Ratio Curve 

- Partial Load Fraction Heat Output Curve 

- Partial Flow Fraction Heat Output Curve 

- Partial Flow Fraction Heat Energy Input Ratio Curve 

- Severe Climate Heat Curve 

- Cooling Output Curve 

- Cooling Fuel Consumption Curve 

- Cooling Efficiency Curve 

- Cooling Energy Input Ratio Curve 

- Partial Load Fraction Cooling Energy Input Ratio Curve 

- Partial Load Fraction Cooling Output Curve 

- Partial Flow Fraction Cooling Output Curve 

- Partial Flow Fraction Cooling Energy Input Ratio Curve 

- **Reversible – Boolean (True/False) (Required) <== Could be a Dropdown** 

- Distribution Components <== Maybe auto populate based on ID? 

- Energy Storage Systems 

- **Four Pipe – Boolean (True/False) (Required) <== Could be a Dropdown** 

- **Investment Cost Function – Text (Required) <== Could be a Dropdown** 

- Maintenance cost Function 

- **Life Time – Whole Number (Required)** 

PV Generation Component: 

- **Generation System ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- **System Type – Text (Required)** 

- Model Name 

- Manufacturer 

- Nominal Energy Output 

- **Electricity Efficiency – Decimal Number (Required)** 

- **Nominal Ambient Temperature – Whole Number (Required)** 

- **Nominal Cell Temperature – Whole Number (Required)** 

- **Nominal Radiation – Whole Number (Required)** 

- **Standard Test Condition Cell Temperature – Whole Number (Required)** 

- **Standard Test Condition Radiation – Whole Number (Required)** 

- **Standard Test Condition Maximum Power – Whole Number (Required)** 

- **Cell Temperature Coefficient - Decimal Number (Required)** 

- **Width - Decimal Number (Required)** 

- **Height - Decimal Number (Required)** 

- Distribution Components 

- Energy Storage Systems 

- **Investment Cost Function – Text (Required) <== Could be a Dropdown** 

- Maintenance Cost Function 

- **Life Time – Whole Number (Required) (Required)** 

Thermal Storage: 

- **Storage ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- **Type Energy Stored - Text (Required) <== Could be a Dropdown** 

- Model Name 

- Manufacturer 

- Maximum Operating Temperature 

- **Insulation Material ID – Whole Number (Required) <= Takes in Material ID** 

- **Insulation Thickness – Decimal Number (Required)** 

- **Physical Characteristics Material ID – Whole Number (Required) <= Takes in Material ID** 

- **Physical Characteristics Tank Thickness – Decimal Number (Required)** 

- Physical Characteristics Height 

- Physical Characteristics Tank Material 

- Physical Characteristics Volume 

- **Storage Medium ID – Whole Number (Required)** 

- **Storage Type - Text (Required) <== Could be a Dropdown** 

- Nominal Capacity 

- Losses Ratio 

- Heating Coil Capacity 

- **Investment Cost Function – Text (Required) <== Could be a Dropdown** 

- Maintenance Cost Function 

- **Life Time – Whole Number (Required) (Required)** 

Electric Storage: 

- **Storage ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- **Type Energy Stored - Text (Required) <== Could be a Dropdown** 

- Model Name 

- Manufacturer 

- **Storage Type - Text (Required) <== Could be a Dropdown** 

- Nominal Capacity 

- Usable Capacity 

- Losses Ratio 

- Rated Output Power 

- Rated Charge Power 

- Nominal Efficiency 

- Discharge Efficiency 

- Battery Storage 

- Depth of Discharge 

- Self-Discharge Rate 

- Soc Min Operational 

- Soc Max Operational 

- Annual Capacity Fade 

- Coupling Type 

- PCS Efficiency 

- Peak Discharge Power 

- Peak Discharge Duration 

- Peak Charge Power 

- Peak Charge Duration 

- Operating Temperature Min 

- Operating Temperature Max 

- **Investment Cost Function – Text (Required) <== Could be a Dropdown** 

- Maintenance Cost Function 

- **Life Time – Whole Number (Required)** 

Distribution Components: 

- **Distribution Component ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- Model Name 

- Manufacturer 

- **Type - Text (Required) <== Could be a Dropdown** 

- Supply Temperature 

- **Distribution Component Fix Flow – Whole Number (Required)** 

- **Distribution Consumption Variable Flow – Whole Number (Required)** 

- **Heat Losses (Required)** 

- Nominal Flow Rate 

- Nominal Power Consumption 

- Pressure Rise 

- Fan Efficiency 

- Motor Efficiency 

- Fan Power Consumption Curve 

- Pressure Curve 

- Generation Systems 

- Energy Storage Systems 

- Energy Emitter Systems 

- **Investment Cost Function - Text (Required) <== Could be a Dropdown** 

- **Life Time – Whole Number (Required)** 

Energy Emitter System: 

- **Emitter System ID – Whole Number (Required)** 

- **Name – Text (Required)** 

- Model Name 

- Manufacturer 

- **Type – Text (Required) <== Could be a Dropdown** 

- **Parasitic Energy Consumption – Whole Number (Required)** 

- Nominal Heat Output 

- Nominal Cooling Output 

- Pipe Diameter 

- **Investment Cost Function - Text (Required) <== Could be a Dropdown** 

- Maintenance Cost Function 

- **Life Time – Whole Number (Required)** 

## System: 

- **System ID (Required)** 

- **Demand Type (Required) <== Takes in Multiple Values, could be a Dropdown** 

- **Name (Required)** 

- **Generation System ID (Required) <== Can Take in Multiple Generation Component (Non PV and PV Component) IDs (Required)** 

- Distribution Systems 

- **Energy Storage System ID (Required) <== Can Take in Multiple Energy Storage IDs (Electrical Storage and Thermal Storage)** 

- Configuration Schema 

- Investment Cost Function 

- Maintenance Cost Function 

- Life Time 

## Energy System Archetype: 

- Archetype Cluster ID 

- **Name (Required)** 

- **Description (Required)** 

- **Systems (Required) <== Takes in Multiple System IDs** 

***Note make sure everything is spelt correctly before putting your excel file into the converter as the hub needs everything to be spelt EXACTLY the way their internal systems spells it** 

# Converting your Excel File into XML 

Once you are done editing our excel files, you will need to convert them into the XML format to be readable in city layers. To do this, we will use the Excel-to-XML Converter program here: (https://github.com/Djswagomega2/Converter-and-Analyizer-for-City- <u>Layers/tree/main). Once you get the GitHub page, download it by clicking on the</u> **_<u>code button</u>_** <u>(the big green button on the top right). After you click on it, a menu will appear once</u> you see it, click download as zip file and save it to your computer. 



<!-- Start of picture text -->
© Converterand-Analyizer-forCiy-Layers = = ware<br>0 ens ie<br>Add a README _—<br>ani Sepgeed waitiows<br>oa ° r " pcan .——ayers at Work  _ =e :<br><!-- End of picture text -->

Once you save it to your computer, you can extract the program using your favorite file extractor. 

One you extract the file, go into the contents of the folder by double clicking it, once you're inside, you should see a folder called **_<u>Excel Files.</u>_** 



<!-- Start of picture text -->
5 pps<br>= a2<br>e: aa Samer oasrersoos aseus<br><!-- End of picture text -->

Put all your excel files that you wish to be converted into XML files into this folder 



<!-- Start of picture text -->
. fers<br>a<br>:<br>Ls] .2*<br>i.<br>.<br>oe<br>ex aa aenme@rcoaeSBrorvo ane<br><!-- End of picture text -->

Once you're done start the program by double clicking on the Excel-XML-Converter application 



<!-- Start of picture text -->
= -<br>.<br>as<br>e a4 Samer casrrvoos me<br><!-- End of picture text -->

Wait a couple of seconds while the app is converting all the files and once it's done it will close automatically. 

After it's finished you should see all your converted files in the **_<u>Output XML Folder</u>_** 



<!-- Start of picture text -->
—<br>-<br>- *<br>.:.<br>i<br>.2<br>.<br>a<br>en ma @emevosBorsocs 3<br><!-- End of picture text -->

You can now use the XML files for whatever your needs fit. Enjoy :) 

