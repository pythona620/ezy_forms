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
        child_type =  item.get("fieldtype")
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
        elif child_type == 'Table':
    
            child_table_row = {
            "fieldtype": item.get("fieldtype"),
            "fieldname": item.get("fieldname"),
            "label": item.get("label"),
            "parent": item.get("parent"),
            "child_table": []
            }
            
            child_table_row["child_table"].insert(0, item.get("value"))
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
    if  child_table_row:
        result.insert(0, child_table_row)
        child_table_row = None
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
            border: 1px solid #000;
               # border-bottom: 1px solid #000;
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
               padding-left: 50px ;
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
          .field textarea {
            border: none;
                outline: none;
            padding: 0px 5px;
            background: transparent;
            flex: 1;
            border-bottom: 1px solid #cccccc;
            min-height: 70px; /* Adjust as needed */
            resize: vertical; /* Allows users to resize the textarea */
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
        @media print {
            .table, .table th, .table td {
                border: 1px solid black !important;
            }
        }
        
   
       
    </style>
</head>
<body>
<div class="main-body">
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
                
                {% for row in section.rows %}
                    <div class="row">
                        {% for column in row.columns %}
                            <div class="column">
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
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
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
                                            <textarea id="{{ field.fieldname }}" name="{{ field.fieldname }}">{{ field['values'] }}</textarea>
                                        {% elif field.fieldtype == 'Date' %}
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}" class="date-input" placeholder="__/__/____">
                                        {% elif field.fieldtype == 'Datetime' %}
                                            <input type="text" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                        
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
 
{% if child_data %}
    {% for child in child_data %}
        {% if child is mapping %}
            <table style="width:98%; margin-left:10px; border-collapse: collapse; border: 1px solid black;">
                <thead>
                    <tr>
                        {% for key in child.keys() %}
                            <th style="border: 1px solid black; padding: 8px; background-color: #f2f2f2;">{{ key }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        {% for value in child.values() %}
                            <td style="border: 1px solid black; padding: 8px;">{{ value }}</td>
                        {% endfor %}
                    </tr>
                </tbody>
            </table>
        {% endif %}
    {% endfor %}
{% endif %}
{% if child_table_data  %}
    <table style="width:98%; margin-left:10px; border-collapse: collapse; border: 1px solid black;">
        <thead>
            <tr>
                {% for key in child_table_data %}
                    <th style="border: 1px solid black; padding: 8px; background-color: #f2f2f2;">{{ key }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
                <tr>
                    {% for value in child_table_data %}
                        <td style="border: 1px solid black; padding: 8px;">{{ '' }}</td>
                    {% endfor %}
                </tr>
        </tbody>
    </table>
    
{% endif %}
 
 

 
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
        data=structered_data, form_name=form_name, child_data=child_data, child_table_data=child_table_data,company_logo=logo_of_company,site_url=site_url
    )
    
    return html_output
 
 
# Sample nested data structure
@frappe.whitelist()
def preview_dynamic_form(form_short_name: str, business_unit=None, name=None):
    """Previews a dynamic form with data populated"""
    json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
    form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name")
    json_object = literal_eval(json_object)["fields"]
    json_object = [
        field for field in json_object
        if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
            ]
    labels = None
    data_list =None
 
    if name == None:
        user_doc = frappe.get_doc("DocType", form_short_name).as_dict()
        
        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc.get(iteration["fieldname"], "")
 
            # Handling child table fields
            if iteration.get("fieldtype") == "Table":
                iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                doc = frappe.get_doc("DocType", form_short_name)
                
                # Dynamically access the child table
                child_table_name = str(iteration["fieldname"])  
                # Get the child table Doctype name
                child_table_doctype = frappe.get_value(
                    "DocField",
                    {"parent": form_short_name, "fieldname": child_table_name},
                    "options"
                )
 
                if not child_table_doctype:
                    return {"error": "Child table not found"}
 
                # Get the fields (columns) of the child table
                child_table_fields = frappe.get_all(
                    "DocField",
                    filters={"parent": child_table_doctype},
                    fields=["label"]
                )
                labels = [field["label"] for field in child_table_fields]
        html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_name,child_table_data=labels,child_data=None,business_unit=business_unit)
        return html_view
    if name:
        user_doc = frappe.get_doc(form_short_name, name).as_dict()
        
        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc.get(iteration["fieldname"], "")
 
            # Handling child table fields
            if iteration.get("fieldtype") == "Table":
                iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                doc = frappe.get_doc(form_short_name, name)
                
                # Dynamically access the child table
                child_table_name = str(iteration["fieldname"])  
                child_table_records = getattr(doc, child_table_name, [])
 
                # Define field names dynamically
                field_names = [df.fieldname for df in frappe.get_meta(child_table_name).fields]
 
                # Define field_labels dynamically
                field_labels = {df.fieldname: df.label for df in frappe.get_meta(child_table_name).fields}
 
                # Generate the data_list with field labels
                data_list = [{field_labels.get(field, field): record.get(field) for field in field_names} for record in child_table_records]
           
    html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_name,child_data=data_list,child_table_data=None,business_unit=business_unit)
    return html_view
 
@frappe.whitelist()
def download_filled_form(form_short_name: str, name: str,business_unit=None):
    """Generates a PDF for the dynamic form with filled data"""
    try:
        
        if not name:
            json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
            json_object = literal_eval(json_object)["fields"]
            json_object = [
                field for field in json_object
                if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
                    ]
    
            user_doc = frappe.get_doc("DocType", form_short_name).as_dict()
            labels = None
            for iteration in json_object:
                if "value" in iteration:
                    iteration["value"] = user_doc.get(iteration["fieldname"], "")
 
                # Handling child table fields
                if iteration.get("fieldtype") == "Table":
                    iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                    doc = frappe.get_doc("DocType", form_short_name)
                    
                    # Dynamically access the child table
                    child_table_name = str(iteration["fieldname"])  
                    # Get the child table Doctype name
                    child_table_doctype = frappe.get_value(
                        "DocField",
                        {"parent": form_short_name, "fieldname": child_table_name},
                        "options"
                    )
 
                    if not child_table_doctype:
                        return {"error": "Child table not found"}
 
                    # Get the fields (columns) of the child table
                    child_table_fields = frappe.get_all(
                        "DocField",
                        filters={"parent": child_table_doctype},
                        fields=["fieldname", "fieldtype", "label"]
                    )
                    labels = [field["label"] for field in child_table_fields]
            html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_short_name,child_table_data=labels,child_data=None,business_unit=business_unit)
            random_number = randint(111, 999)
 
            pdf_filename = f"{form_short_name}_{random_number}.pdf"
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
        json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
        json_object = literal_eval(json_object)["fields"]
        json_object = [
            field for field in json_object
            if field.get("fieldtype") != "Attach" or ("approved_by" in field.get("fieldname", "").lower())
                ]
        user_doc = frappe.get_doc(form_short_name, name).as_dict()
        data_list = None
        for iteration in json_object:
            if "value" in iteration:
                iteration["value"] = user_doc.get(iteration["fieldname"], "")
 
            # Handling child table fields
            if iteration.get("fieldtype") == "Table":
                iteration["value"] = frappe.get_all(iteration["options"], filters={"parent": name}, fields=["*"])
                doc = frappe.get_doc(form_short_name, name)
                
                # Dynamically access the child table
                child_table_name = str(iteration["fieldname"])  
                child_table_records = getattr(doc, child_table_name, [])
 
                # Define field names dynamically
                field_names = [df.fieldname for df in frappe.get_meta(child_table_name).fields]
 
                # Define field_labels dynamically
                field_labels = {df.fieldname: df.label for df in frappe.get_meta(child_table_name).fields}
 
                # Generate the data_list with field labels
                data_list = [{field_labels.get(field, field): record.get(field) for field in field_names} for record in child_table_records]
 
        html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_short_name,child_data=data_list,child_table_data=None,business_unit=business_unit)
        random_number = randint(111, 999)
 
        pdf_filename = f"{form_short_name}_{name}_{random_number}.pdf"
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