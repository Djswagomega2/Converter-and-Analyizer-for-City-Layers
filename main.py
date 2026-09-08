from pathlib import Path
import sys
from Converter import Converter

def main():
    """This function is the main function that runs the converter"""
    if getattr(sys, 'frozen', False): #we check if the program is running as a frozen executable
        program_folder = Path(sys.executable).resolve().parent #we define the program folder as the folder where the executable is located
    else:
        program_folder = Path(__file__).resolve().parent #we define the program folder as the folder where the main.py file is located

    input_folder = program_folder / "Excel Files" #we define the input folder where the excel files are located
    output_folder = program_folder / "Output XML Files" #we define the output folder where the xml files
    output_folder.mkdir(exist_ok=True) #we create the output folder if it doesn't exist
    excel_files = list(input_folder.glob("*.xlsx")) #we get a list of all the excel files in the input folder

    for excel_file in excel_files: #we loop through all the excel files
        input_file = excel_file #we define the input file as the current excel file
        output_file = output_folder / (excel_file.stem + ".xml") #we define the output file as the current excel file name with .xml extension
        xml_key_sheet = "Data_Key" #we define the xml key sheet name
        print(f"Converting {input_file} to {output_file}") #we print the current excel file being converted
        converter = Converter(input_file, output_file, xml_key_sheet) #we create a converter object
        converter.convert() #we convert the excel sheet to an xml file

    

if __name__ == "__main__":
    main()
