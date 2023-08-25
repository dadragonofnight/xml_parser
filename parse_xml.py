

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# Create a tkinter root window (this won't actually show a window).
root = tk.Tk()
root.withdraw()  # Hide the root window

# Show a message box to prompt the user to select an XML file
messagebox.showinfo("Select XML File", "Please select your XML file.")
  
# Open a file dialog to choose the XML file
xml_file_path = filedialog.askopenfilename(
    title="Select XML File",
    filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
)

# Check if a file was selected
if xml_file_path:
    try:
        with open(xml_file_path, 'r') as xml_file:
            xml_data = xml_file.read()

        root = ET.fromstring(xml_data)
        property_elements = root.findall(".//Property")

        combined_properties = {}

        for prop in property_elements:
            ref_name_element = prop.find("RefName")
            value_element = prop.find("Value")

            if ref_name_element is not None and value_element is not None:
                property_name = ref_name_element.text
                property_value = value_element.text

                if property_name in ["iopcount", "PSvoltage"]:
                    if property_name not in combined_properties:
                        combined_properties[property_name] = []
                    combined_properties[property_name].append(property_value)

        formatted_output = "Property                 Value\n"
        formatted_output += "------------------------------------\n"

        for combined_name, values in combined_properties.items():
            formatted_output += f"{combined_name.ljust(25)}: {', '.join(values)}\n"

        with open('the_output_table.txt', 'w') as output_file:
            output_file.write(formatted_output)

        print("Table has been written to 'the_output_table.txt'")

        # Open the generated file using the default text editor
        subprocess.run(['notepad.exe', 'the_output_table.txt'])

    except FileNotFoundError:
        print("The specified XML file was not found.")
else:
    print("No XML file selected.")