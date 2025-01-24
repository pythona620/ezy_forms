from jinja2 import Template
import pdfkit
import frappe
from ast import literal_eval
import requests
from random import randint
import os, sys
import traceback

def rebuild_to_structured_array(flat_array):
    result = []
    current_block = None
    current_section = None
    current_row = None
    current_column = None
 
    for item in reversed(flat_array):
        description = item.get("description")
 
        if description == "Block Break":
            # Push current section, row, and block if they exist
            if current_row:
                current_section["rows"].insert(0, current_row)
                current_row = None
 
            if current_section:
                current_block["sections"].insert(0, current_section)
                current_section = None
 
            if current_block:
                result.insert(0, current_block)
 
            current_block = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent"),
                "sections": []
            }
 
        elif description == "Section Break":
            # Push current row and section if they exist
            if current_row:
                current_section["rows"].insert(0, current_row)
                current_row = None
 
            if current_section:
                current_block["sections"].insert(0, current_section)
 
            current_section = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent"),
                "rows": []
            }
 
        elif description == "Row Break":
            # Push current row if it exists
            if current_row:
                current_section["rows"].insert(0, current_row)
 
            current_row = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") and not item.get("label").lower().startswith("row_") else "",
                "parent": item.get("parent"),
                "columns": []
            }
 
        elif description == "Column Break":
            # Add the column to the current row
            current_column = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent"),
                "fields": []
            }
            current_row["columns"].insert(0, current_column)
 
        else:  # Regular field
            # Add field to the current column
            if current_column:
                updated_field = {
                    "fieldname": item.get("fieldname"),
                    "fieldtype": item.get("fieldtype"),
                    "parent": item.get("parent"),
                    "label": item.get("label"),
                    "reqd": item.get("reqd"),
                    "options": item.get("options"),
                    "values": item.get("value") if item.get("value") else ""
                    }
                current_column["fields"].insert(0, updated_field)
 
    # Push the last row, section, and block (if any exist)
    if current_row:
        current_section["rows"].insert(0, current_row)
 
    if current_section:
        current_block["sections"].insert(0, current_section)
 
    if current_block:
        result.insert(0, current_block)
    return result

# Jinja2 template string
template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Form</title>
    <style>
      body {
            font-family: Arial, sans-serif;
            margin: 15px;
        }
         .row {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .column {
            flex: 1;
            margin-right: 20px;
        }

        .section h3, .section h4 {
            margin: 10px 0;
        }
        
        .section {
            margin: 10px;
            border: 1px solid #eeeeee;
            padding: 15px;
        }
        .section h3 {
            margin-bottom: 10px;
        }
        .field {
            display: flex;
            align-items: baseline;
            # border-bottom: 1px solid #cccccc; 
            padding: 0px ;
            margin: 15px;
        }
        .field label {
            font-weight: bold;
            white-space: nowrap;
            margin-right: 10px; 
            font-size: 13px;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .field input {
            border: none;
            outline: none;
            padding: 0px 5px;
            background: transparent;
            flex: 1; 
            border-bottom: 1px solid #cccccc; 
        }
        .field select, .field textarea {
            border: none;
            outline: none;
            padding: 0px 5px;
            background: transparent;
            flex: 1;
        }
        .field input[type="checkbox"], .field input[type="radio"] {
            flex: 0;
            width: 16px;
            height: 16px;
            margin-left: 5px;
            border: 1px solid #000;
        }
       
    </style>
</head>
<body>

{% for block in data %}
    <div class="block">
        {% for section in block.sections %}
            <div class="section">
                {% if section.label %}
                    <h3>{{ section.label }}</h3>
                {% endif %}
                
                {% for row in section.rows %}
                    <div class="row">
                        {% set total_columns = row.columns|length %}  <!-- Get the number of columns in the row -->

                        {% for column in row.columns %}
                            <div class="column {% if total_columns == 3 %}flex-column{% endif %}">
                                {% for field in column.fields %}
                                    <div class="field">
                                        <label for="{{ field.fieldname }}">{{ field.label }}:</label>

                                           {% if field.fieldtype == 'Data' %}
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Attach' %}
                                            <input type="file" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Phone' %}
                                            <input type="tel" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Time' %}
                                            <input type="time" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Color' %}
                                            <input type="color" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Text' %}
                                            <textarea id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}"></textarea>
                                        {% elif field.fieldtype == 'Date' %}
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}" class="date-input" placeholder="__/__/____">
                                        {% elif field.fieldtype == 'Datetime' %}
                                            <input type="datetime-local" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Check' %}
                                            <input type="checkbox" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'radio' %}
                                            <input type="radio" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Select' %}
                                            <select id="{{ field.fieldname }}" name="{{ field.fieldname }}">
                                                <option value="">Select an option</option>
                                                {% for option in field.options %}
                                                    <option value="{{ option }}">{{ option }}</option>
                                                {% endfor %}
                                            </select>
                                        {% elif field.fieldtype == 'multiselect' %}
                                            <select id="{{ field.fieldname }}" name="{{ field.fieldname }}" multiple>
                                                {% for option in field.options %}
                                                    <option value="{{ option }}">{{ option }}</option>
                                                {% endfor %}
                                            </select>
                                        {% elif field.fieldtype == 'Signature' %}
                                            <input type="text" id="{{ field.fieldname }}" name="{{ field.fieldname }}" placeholder="Signature input (future implementation)">
                                        {% endif %}
                                    </div>
                                {% endfor %}
                            </div>
                        {% endfor %}
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    </div>
{% endfor %}


<script>
    document.addEventListener("DOMContentLoaded", function () {

        const dateInputs = document.querySelectorAll(".date-input");

        dateInputs.forEach(input => {
            // If input is empty, show slashes
            if (!input.value) {
                input.value = "__/__/____";
            }

            // Handle user input
            input.addEventListener("input", function (event) {
                let value = event.target.value.replace(/\D/g, ""); // Remove non-numeric characters
                let formattedValue = "__/__/____";

                if (value.length >= 2) formattedValue = value.slice(0, 2) + "/__/____";
                if (value.length >= 4) formattedValue = value.slice(0, 2) + "/" + value.slice(2, 4) + "/____";
                if (value.length >= 8) formattedValue = value.slice(0, 2) + "/" + value.slice(2, 4) + "/" + value.slice(4, 8);

                event.target.value = formattedValue;
            });

            // Handle focus (clear placeholder slashes)
            input.addEventListener("focus", function () {
                if (input.value === "__/__/____") {
                    input.value = "";
                }
            });

            // Handle blur (restore slashes if empty)
            input.addEventListener("blur", function () {
                if (!input.value.replace(/\D/g, "")) {
                    input.value = "__/__/____";
                }
            });
        });
    });
</script>

</body>
</html>
"""
 
def convert_html_to_pdf(html_content, pdf_path):
    try:
        pdfkit.from_string(html_content, pdf_path)
        print(f"PDF generated and saved at {pdf_path}")
    except Exception as e:
        print(f"PDF generation failed: {e}")

def json_structure_call_for_html_view(json_obj:list):
    structered_data = rebuild_to_structured_array(flat_array=json_obj)
    html_output = Template(template_str).render(data=structered_data)
    return html_output

# Sample nested data structure
@frappe.whitelist()
def preview_dynamic_form(form_short_name:str):
    json_object = frappe.db.get_value("Ezy Form Definitions",form_short_name,"form_json")
    json_object = literal_eval(json_object)["fields"]
    html_view = json_structure_call_for_html_view(json_obj=json_object)
    return html_view

@frappe.whitelist()
def download_filled_form(form_short_name:str,name:str):
    try:
        json_object = frappe.db.get_value("Ezy Form Definitions",form_short_name,"form_json")
        json_object = literal_eval(json_object)["fields"]
        user_doc = frappe.get_doc(form_short_name,name).as_dict()
        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc[iteration["fieldname"]] if user_doc[iteration["fieldname"]] else ""
        html_view = json_structure_call_for_html_view(json_obj=json_object)
        random_number = randint(111,999)
        pdf_path = frappe.local.site + f"/private/files/{form_short_name}_{name}_{random_number}.pdf"
        
        # Generate PDF
        convert_html_to_pdf(html_content = html_view, pdf_path = pdf_path)

        files_new = {"file": open(pdf_path, 'rb')}
        payload_new = {'is_private': 1, 'folder': 'Home'}
        os.remove(pdf_path)
        host = frappe.get_single("Global Site Settings").site
        file_response = requests.post(host+"/api/method/upload_file", files=files_new,
                                                data=payload_new, verify=False).json()
        frappe.db.set_value("File", file_response["message"]["name"], {"attached_to_doctype": form_short_name, "attached_to_name":"qr_code_image", "attached_to_name": name})
        return pdf_path
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            frappe.log_error("Error Downloading File","line No:{}\n{}".format(exc_tb.tb_lineno,traceback.format_exc()))
            frappe.throw(e)
            return {"success":False,"message":str(e)}