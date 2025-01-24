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
                    "values": item.get("values")
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

# json_object = [
#         {"description": "Field","fieldname": "guest_name","fieldtype": "Data","idx": 0,"label": "Guest name","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 1,"label": ""},
#         {"description": "Field","fieldname": "company_name","fieldtype": "Data","idx": 2,"label": "Company name","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 3,"label": ""},
#         {"description": "Field","fieldname": "position","fieldtype": "Data","idx": 4,"label": "Position","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 5,"label": ""},
#         {"description": "Row Break","fieldname": "row_0_0_0","fieldtype": "Column Break","idx": 6,"label": "row_0_0_0"},
#         {"description": "Section Break","fieldname": "guest_details","fieldtype": "Section Break","label": "guest details","idx": 7},
#         {"description": "Field","fieldname": "arrival_date","fieldtype": "Date","idx": 8,"label": "Arrival date","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 9,"label": ""},
#         {"description": "Field","fieldname": "departure_date","fieldtype": "Date","idx": 10,"label": "Departure date","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 11,"label": ""},
#         {"description": "Row Break","fieldname": "row_0_1_0","fieldtype": "Column Break","idx": 12,"label": "row_0_1_0"},
#         {"description": "Section Break","fieldname": "stay_details","fieldtype": "Section Break","label": "stay details","idx": 13},
#         {"description": "Field","fieldname": "number_of_persons","fieldtype": "Data","idx": 14,"label": "Number of persons","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 15,"label": ""},
#         {"description": "Field","fieldname": "number_of_nights","fieldtype": "Data","idx": 16,"label": "Number of nights","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 17,"label": ""},
#         {"description": "Field","fieldname": "number_of_rooms","fieldtype": "Check","idx": 18,"label": "Number of rooms","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 19,"label": ""},
#         {"description": "Row Break","fieldname": "row_0_2_0","fieldtype": "Column Break","idx": 20,"label": "row_0_2_0"},
#         {"description": "Section Break","fieldname": "","fieldtype": "Section Break","label": "","idx": 21},
#         {"description": "Field","fieldname": "allocated_rooms_in_standard","fieldtype": "Data","idx": 22,"label": "Allocated rooms in standard","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Field","fieldname": "total_persons_stayed_in_standard","fieldtype": "Data","idx": 23,"label": "Total persons stayed in standard","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "standard_room","fieldtype": "Column Break","idx": 24,"label": "Standard room"},
#         {"description": "Field","fieldname": "allocated_rooms_in_premier","fieldtype": "Data","idx": 25,"label": "Allocated rooms in premier","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Field","fieldname": "total_persons_stayed_in_premier","fieldtype": "Data","idx": 26,"label": "Total persons stayed in premier","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "premier_room","fieldtype": "Column Break","idx": 27,"label": "Premier room"},
#         {"description": "Field","fieldname": "allocated_room_in_suite","fieldtype": "Data","idx": 28,"label": "Allocated room in suite","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Field","fieldname": "total_persons_stayed_in_suite","fieldtype": "Data","idx": 29,"label": "Total persons stayed in suite","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "suite_room","fieldtype": "Column Break","idx": 30,"label": "Suite room"},
#         {"description": "Row Break","fieldname": "row_0_3_0","fieldtype": "Column Break","idx": 31,"label": "row_0_3_0"},
#         {"description": "Section Break","fieldname": "room_details","fieldtype": "Section Break","label": "Room details","idx": 32},
#         {"description": "Block Break","fieldname": "requestor","fieldtype": "Section Break ","label": "Requestor","idx": 33},
#         {"description": "Field","fieldname": "reservation_number","fieldtype": "Data","idx": 34,"label": "Reservation number","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 35,"label": ""},
#         {"description": "Field","fieldname": "reservation_made_by","fieldtype": "Data","idx": 36,"label": "Reservation made by","reqd": 0,
#             "value": ""
 
#         },
 
#         {"description": "Column Break","fieldname": "","fieldtype": "Column Break","idx": 37,"label": ""},
#         {"description": "Row Break","fieldname": "row_0_0_1","fieldtype": "Column Break","idx": 38,"label": "row_0_0_1"},
#         {"description": "Section Break","fieldname": "reservtaion_details","fieldtype": "Section Break","label": "Reservtaion details","idx": 39},
#         {"description": "Block Break","fieldname": "approver1","fieldtype": "Section Break ","label": "Approver-1","idx": 40}
#     ]

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
    json_object = literal_eval(json_object)
    html_view = json_structure_call_for_html_view(json_obj=json_object)
    return html_view

@frappe.whitelist()
def download_filled_form(form_short_name:str,name:str):
    try:
        json_object = frappe.db.get_value("Ezy Form Definitions",form_short_name,"form_json")
        json_object = literal_eval(json_object)
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
        file_response = requests.post(host+"api/method/upload_file", files=files_new,
                                                data=payload_new, verify=False).json()
        frappe.db.set_value("File", file_response["message"]["name"], {"attached_to_doctype": form_short_name, "attached_to_name":"qr_code_image", "attached_to_name": name})
        return pdf_path
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            frappe.log_error("Error Downloading File","line No:{}\n{}".format(exc_tb.tb_lineno,traceback.format_exc()))
            frappe.throw(e)
            return {"success":False,"message":str(e)}