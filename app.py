from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])


def index():

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            xml_data = uploaded_file.read().decode('utf-8')

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

            # Open the generated file using the default text editor
            subprocess.run(['notepad.exe', 'the_output_table.txt'])

            return send_file('the_output_table.txt', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)