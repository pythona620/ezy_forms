from jinja2 import Template
import pdfkit
import frappe
from ast import literal_eval
import requests
from random import randint
import os, sys
import traceback
from frappe.utils import get_bench_path, cstr
from frappe.utils import get_bench_path, cstr, get_url
 
def rebuild_to_structured_array(flat_array):
    result = []
    current_block = None
    current_section = None
    current_row = None
    current_column = None
    child_table_row = None
    for item in reversed(flat_array):
        description = item.get("description")
        child_type = item.get("fieldtype")
        idx = item.get("idx")

        if description == "Block Break":
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
                "idx": idx,
                "sections": []
            }

        elif description == "Section Break":
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
                "idx": idx,
                "rows": []
            }

        elif description == "Row Break":
            if current_row:
                current_section["rows"].insert(0, current_row)

            current_row = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") and not item.get("label").lower().startswith("row_") else "",
                "parent": item.get("parent"),
                "idx": idx,
                "columns": []
            }

        elif description == "Column Break":
            current_column = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent"),
                "idx": idx,
                "fields": []
            }
            current_row["columns"].insert(0, current_column)

        elif child_type == 'Table':
            child_table_row = {
                "fieldtype": item.get("fieldtype"),
                "fieldname": item.get("fieldname"),
                "label": item.get("label"),
                "parent": item.get("parent"),
                "options": item.get("options"),
                "description": item.get("description"),
                "idx": idx,
                "child_table": []
            }

            current_section["rows"].insert(0, child_table_row)
            child_table_row["child_table"].insert(0, item.get("value"))

        else:  # Regular field
            if current_column:
                updated_field = {
                    "fieldname": item.get("fieldname"),
                    "fieldtype": item.get("fieldtype"),
                    "parent": item.get("parent"),
                    "label": item.get("label"),
                    "description": item.get("description"),
                    "reqd": item.get("reqd"),
                    "options": item.get("options"),
                    "values": item.get("value") if item.get("value") else "",
                    "idx": idx
                }
                current_column["fields"].insert(0, updated_field)

    # Final push for any remaining structures
    if current_row:
        current_section["rows"].insert(0, current_row)

    if current_section:
        current_block["sections"].insert(0, current_section)

    if child_table_row:
        result.insert(0, child_table_row)

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
            
   
              # height: 100vh;
        }
          .main-body{
              margin: 15px;
               border: 1px solid #000;
               padding: 10px;
               border-radius: 5px;
          }
         .row {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }

        .column {
            flex: 1;
            margin-right: 5px;
            margin-left: 5px;
            padding-left:5px;
            padding-right:5px;
            
            
        }
 
        .section h3, .section h4 {
            margin: 10px 0;
        }
        
        .section {
            margin: 10px;
            border: 0px solid #ccc;
               # border-bottom: 1px solid #000;
            # padding: 15px;
            border-radius:3px;
        }
        .section h3 {
            margin-bottom: 10px;
        }
        .field {
            display: flex;
            align-items: baseline;
            # border-bottom: 1px solid #cccccc;
            padding: 0px ;
            margin: 10px;
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
               padding-left: 50px ;
            background: transparent;
            flex: 1;
            border-bottom: 1px solid #cccccc;
            font-weight:600;
            
        }
        .block_input{
              border: none;
            outline: none;
            padding: 0px 5px;
               padding-left: 50px ;
            background: transparent;
            flex: 1;
            border-bottom: 1px solid #cccccc;
            font-weight:600;
        }
        .field select, .field textarea {
            
            outline: none;
            padding: 0px 5px;
            background: transparent;
            flex: 1;
        }
          .field textarea {
            
                
            padding: 0px 5px;
            background: transparent;
            flex: 1;
            border-bottom: 1px solid #cccccc;
            resize: none; /* Disable manual resizing */
            overflow-y: hidden; /* Hide scrollbar */ /* Allows users to resize the textarea */
}
        .field input[type="checkbox"], .field input[type="radio"] {
            flex: 0;
            width: 16px;
            height: 16px;
            margin-left: 5px;
            border: 1px solid #000;
        }
          .header-container{
              display: flex;
               justify-content: space-between;
              
              align-items: center;
               padding: 10px;
            padding-bottom: 0px;
              border-bottom: 1px solid #000;
               # background-color: #f0f0f0;
               margin: 0px 10px;
          }
/* Flex container to arrange checkboxes */
            .checkbox-container {
                display: flex;
                flex-wrap: wrap;   /* Allow items to wrap into new lines */
                gap: 10px;         /* Space between checkboxes */
                width: 100%;       /* Ensure the container uses full available width */
            }


            .checkbox-container > .checkbox-gap {
                flex: 1 0 calc(33.33% - 20px);  /* 3 per row, considering gap */
                box-sizing: border-box; 
                display: flex;
                align-items: end;
                gap: 15px; /* Space between checkbox and text */
                margin-top: 10px;  /* Space above */
                margin-bottom: 10px; /* Space below */
                min-width: 150px;  /* Prevent shrinking */
                
            }
            /* Checkbox design */
            .custom-checkbox {
                display: inline-block;
                width: 20px !important;
                height: 20px !important;
                border: 2px solid #007bff;  /* Blue border */
                border-radius: 4px;
                background-color: #007bff; /* Blue background */
                position: relative;
                margin:3px;
                margin-bottom:0px;
                
                flex-shrink: 0; 
            }

            /* White checkmark */
            .custom-checkbox::before {
                content: '✔'; 
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 16px;
                color: white;  /* White checkmark */
                font-weight: bold;
            }

            /* Disabled effect */
            .custom-checkbox.disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .custom-checkbox.checked {
                background-color: #007bff; /* Blue for checked */
                border-color: #007bff;
            }

            .custom-checkbox.unchecked {
                background-color: #fff; /* Gray for unchecked */
                border-color: #ccc;
            }


        .footer-container{
             display: flex;
             justify-content: center;
             padding: 10px;
             # background-color: #f0f0f0;
            margin: 0px 10px;
            positon: fixed;
               bottom: 0px;
               left: 0px;
               width: 100%;
               right: 0px;
        }
        
          .footer-container span{
              margin: 0px;
              padding: 0px;
              font-weight: bold;
          }
          .header-container h4{
              font-size: 25px;
              font-weight: bold;
              margin: 0px;
      
          }
          .signature-Imge{
              min-width: 80px;
              max-width: 90px;
              padding-bottom: 5px;
              border-bottom: 1px solid #cccccc;
              
          }
          .childtablename{
              font-size:16px;
              font-weight:bold;
              margin: 8px 0px 3px 12px;
          }
 
        .logo-div{
            max-width: 300px;
              min-width: 200px;
        }
         .header-left{
             display: flex;
              justify-content: center;
         }
         .header-right{
             min-width: 200px;
         }
         .description-block{
             font-size:12px;
         }
        .watermark {
            position: fixed;
            top: 50%;
            left: 30%;
            font-size: 80px;
            color: rgba(0, 0, 0, 0.1); /* Light gray with transparency */
            transform: rotate(-30deg);
            z-index: 0;
            pointer-events: none;
            user-select: none;
            white-space: nowrap;
        }
         
        @media print {
            .table, .table th, .table td {
                border: 1px solid black !important;
            }
            .table{
                width: 100% !important;
            }
            textarea {
                border: none;
                resize: none;
                overflow: visible !important;
                white-space: pre-wrap;
            }
            .watermark {
             display: block;
            }
        }
        
   
       
    </style>
    </head>
<body>
<div class="main-body">
<div class="watermark">{{business_unit}}</div>

<div class="header-container">
    <div class="logo-div"> 
    
    <img src="{{ company_logo }}" alt="logo" style="height: 70px; width: 200px; margin-bottom:0px">
    
    
     </div>
  <div class="header-left">
  
 
    <h4>{{ form_name }}</h4>
  </div>
     <div class="header-right">
    
     </div>
    
</div>
{% for block in data %}

    <div class="block">
        {% for section in block.sections %}
        
            <div class="section">
                {% if section.label %}
                    <h3>{{ section.label }}</h3>
                {% endif %}
                
                {% for row in section.rows | sort(attribute='idx') %}
                
                                            
                            {% set table_name = row.options %}

                            {% if row.description == 'true' %}
                                {% if table_name in child_data %}
                                    <h3 class="childtablename">{{ table_name.replace("_", " ").title() }}</h3>
                                    {% if child_data[table_name] %}
                                        {% for child in child_data[table_name] %}
                                            <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
                                                
                                                <div style="display: flex; flex-wrap: wrap;">
                                                    {% for key, value in child.items() %}
                                                        <div style="width: 48%; display:flex;align-items:baseline;gap:2px;  margin-right: 2%; margin-bottom: 10px;">
                                                            <label style="font-weight: 600;">{{ key }}:</label><br />
                                                            {% if value and value.endswith(('.pdf', '.jpg', '.png', '.jpeg')) %}
                                                                <a href="{{ value }}" target="_blank">View Attachment</a>
                                                            {% else %}
                                                                <input type="text" value="{{ value }}" class="block_input" readonly style="width: 100%; padding: 5px;" />
                                                            {% endif %}
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            </div>
                                        {% endfor %}
                                    {% else %}
                                        <p>No data available for {{ table_name }}</p>
                                    {% endif %}

                                {% elif table_name in child_table_data %}
                                    <h3 class="childtablename">{{ table_name.replace("_", " ").title() }}</h3>
                                    <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
                                    
                                        <div style="display: flex; flex-wrap: wrap;">
                                            {% for column in child_table_data[table_name] %}
                                                <div style="width: 48%; margin-right: 2%;display:flex;align-items:baseline;gap:2px; margin-bottom: 10px;">
                                                    <label style="font-weight: 600;">{{ column }}:</label><br />
                                                    <input type="text"  readonly class="block_input" style="width: 100%; padding: 5px; color: #ccc;" />
                                                </div>
                                            {% endfor %}
                                        </div>
                                    </div>
                                {% endif %}

                            {% else %}

                                {% if table_name in child_data %}
                                    <h3 class="childtablename">{{ table_name.replace("_", " ").title() }}</h3>
                                    {% if child_data[table_name] %}
                                        <table style="width: 100%; margin-bottom:10px; border-collapse: collapse;">
                                            <thead>
                                                <tr>
                                                    <th style="border: 1px solid #ccc;width:3%; padding: 8px; background-color: #f2f2f2;">S.no</th>
                                                    {% for key in child_data[table_name][0].keys() %}
                                                        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">{{ key }}</th>
                                                    {% endfor %}
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for child in child_data[table_name] %}
                                                    <tr>
                                                        <td style="border: 1px solid #ccc;padding: 8px;text-align:center;">{{ loop.index }}</td>
                                                        {% for value in child.values() %}
                                                            <td style="border: 1px solid #ccc; padding: 8px; word-break: break-word;">{{ value if value else '—' }}</td>
                                                        {% endfor %}
                                                    </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    {% else %}
                                        <p>No data available for {{ table_name }}</p>
                                    {% endif %}

                                {% elif table_name in child_table_data %}
                                    <h3 class="childtablename">{{ table_name.replace("_", " ").title() }}</h3>
                                    <table style="width: 100%; margin-bottom:10px; border-collapse: collapse;">
                                        <thead>
                                            <tr>
                                                <th style="border: 1px solid #ccc;width:3%; padding: 8px; background-color: #f2f2f2;">S.no</th>
                                                {% for column in child_table_data[table_name] %}
                                                    <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">{{ column }}</th>
                                                {% endfor %}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">-</td>
                                                {% for column in child_table_data[table_name] %}
                                                    <td style="border: 1px solid #ccc; padding: 8px; text-align: center; color: #ccc;">-</td>
                                                {% endfor %}
                                            </tr>
                                        </tbody>
                                    </table>
                                {% endif %}
                            {% endif %}

                    

                    <div class="row">
                        {% for column in row.columns %}
                       
                            <div class="column">
                              {% if column.label %}
                                <h3>{{ column.label }}</h3>
                                {% endif %}
                                {% for field in column.fields %}
                               
                                    <div class="field">
                                        <label for="{{ field.fieldname }}">{{ field.label }}:</label>

                                        {% if field.fieldtype in ['Check', 'radio'] %}
                                            <div class="container-fluid">
                                                <div class="row">
                                                    {% for option in field.options.split('\n') %}
                                                        <div class="form-check col-4 mb-4">
                                                            <div>
                                                            
                                                                {% if field.fieldtype == 'Check'  %}
                                                                    <input
                                                                        type="checkbox"
                                                                        class="form-check-input"
                                                                        id="{{ field.fieldname }}-{{ loop.index0 }}"
                                                                        name="{{ field.fieldname }}"
                                                                        value="{{ option }}"
                                                                        {% if option in field.values %} checked {% endif %}
                                                                        disabled
                                                                    >
                                                                {% elif field.fieldtype == 'radio' %}
                                                                    <input
                                                                        type="radio"
                                                                        class="form-check-input"
                                                                        id="{{ field.fieldname }}-{{ loop.index0 }}"
                                                                        name="{{ field.fieldname }}"
                                                                        value="{{ option }}"
                                                                        {% if option == field.values %} checked {% endif %}
                                                                        disabled
                                                                    >
                                                                {% endif %}
                                                            </div>
                                                            <div>
                                                                <label class="form-check-label m-0" for="{{ field.fieldname }}-{{ loop.index0 }}">
                                                                    {{ option }}
                                                                </label>
                                                            </div>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            </div>
 
                                        {% elif field.fieldtype == 'Data' or field.fieldtype == 'Select' %}
                                            <input type="text" id="{{ field.fieldname }}" disabled value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                       {% elif field.fieldtype == 'Small Text' %}
                                            {% set options = field.options.strip().split('\n') %}
                                            
                                            {% if field['values'] %}
                                                {% set selected_values = field['values'] | replace('["', '') | replace('"]', '') | replace('","', ',') %}
                                                {% set selected_values_list = selected_values.split(',') %}
                                                <div class="checkbox-container">
                                                    {% for value in selected_values_list if value %}
                                                        <div class="checkbox-gap">
                                                            <span class="custom-checkbox checked"></span>
                                                            <span style="margin-top:6px; margin-left:4px;">{{ value }}</span>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            {% else %}
                                                <div class="checkbox-container">
                                                    {% for option in options if option %}
                                                        <div class="checkbox-gap">
                                                            <span class="custom-checkbox unchecked"></span>
                                                           <span style="margin-top:6px; margin-left:4px;"> {{ option }}</span>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            {% endif %}


                                                                                            





                                        {% elif field.fieldtype == 'Attach' %}
                                            {% if field['values'] %}
                                                <img  id="{{ field.fieldname }}" src="{{ site_url + field['values'] or ''  }}" class="signature-Imge" name="{{ field.fieldname }}">
                                            {% else %}
                                                <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                            {% endif %}
                                        {% elif field.fieldtype == 'Phone' %}
                                            <input type="tel" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Time' %}
                                            <input type="time" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Color' %}
                                            <input type="color" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                        {% elif field.fieldtype == 'Text' %}
                                            {% set value = field['values'] %}
                                            {% set char_count = value | length %}
                                            {% set newline_count = value.count('\n') %}
                                            {% set estimated_lines = (char_count // 60) + 1 + newline_count %}
                                            {% set height = estimated_lines * 24 %}
                                            <textarea
                                                id="{{ field.fieldname }}"
                                                name="{{ field.fieldname }}"
                                                style="height: {{ height }}px; border:none;"
                                            >{{ value }}</textarea>
                                        {% elif field.fieldtype == 'Date' %}
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}" class="date-input" placeholder="__/__/____">
                                        {% elif field.fieldtype == 'Datetime' %}
                                            <input type="text" id="{{ field.fieldname }}" disabled value="{{ field['values'].strftime('%d/%m/%Y %H:%M') if field['values'] else '' }}" name="{{ field.fieldname }}">
                        
                                        {% elif field.fieldtype == 'Signature' %}
                                            <input type="text" id="{{ field.fieldname }}" name="{{ field.fieldname }}" placeholder="Signature input (future implementation)">
                                        {% endif %}
                                        
                                    </div>
                                         {% if field.description != 'Field' %}
                                            <div class="w-100 description-block mt-1">
                                                <span class="fw-semibold">Description :</span><br>
                                                <span>{{ field.description | replace('\n', '<br>') | safe }}</span>
                                            </div>
                                        {% endif %}
                                {% endfor %}
                            </div>
                        {% endfor %}
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
        
        
  
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
            document.addEventListener("DOMContentLoaded", function () {
                const textareas = document.querySelectorAll("textarea");

                textareas.forEach(textarea => {
                    // Remove any hardcoded height
                    textarea.style.height = "auto";
                    textarea.style.overflow = "hidden";

                    // Function to auto-resize based on content
                    const resizeTextarea = () => {
                        textarea.style.height = "auto"; // Reset
                        textarea.style.height = textarea.scrollHeight + "px"; // Set based on content
                    };

                    resizeTextarea(); // Initial resize on load
                    textarea.addEventListener("input", resizeTextarea); // Resize on user input
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
    
    except Exception as e:
        frappe.log_error(f"PDF generation failed: {e}")
 
def json_structure_call_for_html_view(json_obj: list, form_name: str, child_data, child_table_data,business_unit):
    if child_data is None:
        child_data = []
    site_url = frappe.utils.get_url()
    logo_of_company = site_url + "/files/Final-logo-ezyforms-removebg-preview.png"
    if child_table_data is None:
        child_table_data = []
    
    structered_data = rebuild_to_structured_array(flat_array=json_obj)
    if structered_data is None:
        structered_data = []  # Ensure it's iterable
 
    company_logo = frappe.db.get_value("Ezy Business Unit",business_unit,"bu_logo")
    if company_logo:
        logo_of_company = site_url + company_logo
  
    html_output = Template(template_str).render(
        data=structered_data, form_name=form_name, child_data=child_data, child_table_data=child_table_data,company_logo=logo_of_company,site_url=site_url,business_unit=business_unit
    )
    
    return html_output
 

@frappe.whitelist()
def preview_dynamic_form(form_short_name: str, business_unit=None, name=None):
    """Previews a dynamic form with data populated"""
    json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
    form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name")
    json_object = literal_eval(json_object)["fields"]

    # Exclude "Attach" fields except those with "approved_by" in their fieldname
    json_object = [
        field for field in json_object
        if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
    ]

    labels = {}  # Dictionary to store multiple child table fields
    data_list = {}
    if name is None:
        user_doc = frappe.get_doc("DocType", form_short_name).as_dict()

        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc.get(iteration["fieldname"], "")

            # Handling child table fields
            if iteration.get("fieldtype") == "Table":
                iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                child_table_name = str(iteration["fieldname"])  

                # Get the child table Doctype name
                child_table_doctype = frappe.get_value(
                    "DocField",
                    {"parent": form_short_name, "fieldname": child_table_name},
                    "options"
                )

                if not child_table_doctype:
                    return {"error": f"Child table '{child_table_name}' not found"}

                # Get the fields (columns) of the child table
                child_table_fields = frappe.get_all(
                    "DocField",
                    filters={"parent": child_table_doctype},
                    fields=["label"]
                )

                # Store labels for each child table
                labels[child_table_name] = [field["label"] for field in child_table_fields]

        # Call the function to generate HTML view
        html_view = json_structure_call_for_html_view(
            json_obj=json_object,
            form_name=form_name,
            child_table_data=labels,
            child_data=None,
            business_unit=business_unit
        )
        return html_view

    if name:
        user_doc = frappe.get_doc(form_short_name, name).as_dict()

        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc.get(iteration["fieldname"], "")

            # Handling child table fields
            if iteration.get("fieldtype") == "Table":
                child_table_name = str(iteration["fieldname"])
                child_table_records = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                
                # Get field names and labels dynamically
                field_names = [df.fieldname for df in frappe.get_meta(iteration["options"]).fields]
                field_labels = {df.fieldname: df.label for df in frappe.get_meta(iteration["options"]).fields}

                # Store child table data properly
                data_list[child_table_name] = [
                    {field_labels.get(field, field): record.get(field) for field in field_names}
                    for record in child_table_records
                ]



    html_view = json_structure_call_for_html_view(
        json_obj=json_object,
        form_name=form_name,
        child_data=data_list,
        child_table_data=None,
        business_unit=business_unit
    )
    
    return html_view
 
 
@frappe.whitelist()
def download_filled_form(form_short_name: str, name: str|None,business_unit=None):
    """Generates a PDF for the dynamic form with filled data"""
    try:
        
    
        if name is None:
            print_format = frappe.db.get_value("Ezy Form Definitions", form_short_name, "print_format")
            if print_format:
                html_view_ = get_html_file_data(form_short_name,None,str(print_format))
                html_view = html_view_['html']
            else:
                json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
                json_object = literal_eval(json_object)["fields"]
                json_object = [
                    field for field in json_object
                    if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
                        ]
                user_doc = frappe.get_doc("DocType", form_short_name).as_dict()
                labels={}
                for iteration in json_object:
                    if "value" in iteration:
                        iteration["value"] = user_doc.get(iteration["fieldname"], "")

                    # Handling child table fields
                    if iteration.get("fieldtype") == "Table":
                        iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                        child_table_name = str(iteration["fieldname"])  

                        # Get the child table Doctype name
                        child_table_doctype = frappe.get_value(
                            "DocField",
                            {"parent": form_short_name, "fieldname": child_table_name},
                            "options"
                        )

                        if not child_table_doctype:
                            return {"error": f"Child table '{child_table_name}' not found"}

                        # Get the fields (columns) of the child table
                        child_table_fields = frappe.get_all(
                            "DocField",
                            filters={"parent": child_table_doctype},
                            fields=["label"]
                        )

                        # Store labels for each child table
                        labels[child_table_name] = [field["label"] for field in child_table_fields]
                html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_short_name,child_table_data=labels,child_data=None,business_unit=business_unit)
            random_number = randint(111, 999)
 
            pdf_filename = f"{form_short_name}_{random_number}  .pdf"
            pdf_path = f"private/files/{pdf_filename}"
            absolute_pdf_path = os.path.join(get_bench_path(), "sites", cstr(frappe.local.site), pdf_path)
 
            convert_html_to_pdf(html_content=html_view, pdf_path=absolute_pdf_path)
 
            new_file = frappe.get_doc({
                "doctype": "File",
                "file_name": pdf_filename,
                "file_url": f"/{pdf_path}",
                "is_private": 1,
 
            })
            new_file.insert(ignore_permissions=True)
            frappe.db.commit()
 
            file_url = get_url(new_file.file_url)
 
            return file_url
        if name:
            
            print_format = frappe.db.get_value("Ezy Form Definitions", form_short_name, "print_format")
            
            if print_format:
                html_view_ = get_html_file_data(form_short_name,name,print_format)
                html_view = html_view_['html']
            else:
                json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
                json_object = literal_eval(json_object)["fields"]
                json_object = [
                    field for field in json_object
                    if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
                        ]
                user_doc = frappe.get_doc(form_short_name, name).as_dict()
                data_list ={}
                for iteration in json_object:
                    if "value" in iteration:
                        iteration["value"] = user_doc.get(iteration["fieldname"], "")

                    # Handling child table fields
                    if iteration.get("fieldtype") == "Table":
                        child_table_name = str(iteration["fieldname"])
                        child_table_records = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                        
                        # Get field names and labels dynamically
                        field_names = [df.fieldname for df in frappe.get_meta(iteration["options"]).fields]
                        field_labels = {df.fieldname: df.label for df in frappe.get_meta(iteration["options"]).fields}

                        # Store child table data properly
                        data_list[child_table_name] = [
                            {field_labels.get(field, field): record.get(field) for field in field_names}
                            for record in child_table_records
                        ]
                        
                html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_short_name,child_data=data_list,child_table_data=None,business_unit=business_unit)
                
            random_number = randint(111, 999)
    
            pdf_filename = f"{form_short_name}_{name}_{random_number}mailfiles.pdf"
            pdf_path = f"private/files/{pdf_filename}"
            absolute_pdf_path = os.path.join(get_bench_path(), "sites", cstr(frappe.local.site), pdf_path)
    
            convert_html_to_pdf(html_content=html_view, pdf_path=absolute_pdf_path)
    
            new_file = frappe.get_doc({
                "doctype": "File",
                "file_name": pdf_filename,
                "file_url": f"/{pdf_path}",
                "is_private": 1,
                "attached_to_doctype": form_short_name,
                "attached_to_name": name
            })
            new_file.insert(ignore_permissions=True)
            frappe.db.commit()
    
            file_url = get_url(new_file.file_url)
    
            return file_url
 
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error Downloading File", f"line No:{exc_tb.tb_lineno}\n{traceback.format_exc()}")
        frappe.throw(str(e))
 
 
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error Downloading File", "line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()))
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}
    
    
from frappe.www.printview import get_html_and_style

def get_html_file_data(doc=None,data=None,print_format=None):
    
    html_file = get_html_and_style(doc,name=data,print_format=print_format,no_letterhead=None,letterhead=None,trigger_print=False,style=None,settings=None)
 
    return html_file