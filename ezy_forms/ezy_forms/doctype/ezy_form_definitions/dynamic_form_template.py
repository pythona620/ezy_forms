from jinja2 import Template
import pdfkit
import frappe
from ast import literal_eval
import requests
from random import randint
import os, sys
import traceback
from frappe.utils import get_bench_path, cstr,get_url,now_datetime,get_site_path, get_url
from pdf2image import convert_from_path
import zipfile
from frappe.utils.file_manager import get_file_path
import shutil
from datetime import date, datetime


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
                "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent")if item.get("parent") else "",
                "idx": idx or '',
                "sections": []
            }

        elif description == "Section Break":
            if current_row:
                current_section["rows"].insert(0, current_row)
                current_row = None

            if current_section:
                current_block["sections"].insert(0, current_section)

            current_section = {
                "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent") if item.get("parent") else "",
                "idx": idx or '',
                "rows": []
            }

        elif description == "Row Break":
            if current_row:
                current_section["rows"].insert(0, current_row)

            current_row = {
                "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                "label": item.get("label") if item.get("label") and not item.get("label").lower().startswith("row_") else "",
                "parent": item.get("parent")if item.get("parent") else "",
                "idx": idx or '',
                "columns": []
            }

        elif description == "Column Break":
            current_column = {
                "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent")if item.get("parent") else "",
                "idx": idx or '',
                "fields": []
            }
            current_row["columns"].insert(0, current_column)

        elif child_type == 'Table':
            child_table_row = {
                "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                "label": item.get("label") if item.get("label") else "",
                "parent": item.get("parent")if item.get("parent") else "",
                "options": item.get("options") if item.get("options") else [],
                "description": item.get("description") if item.get("description") else "",
                "idx": idx or '',
                "child_table": []
            }

            current_section["rows"].insert(0, child_table_row)
            child_table_row["child_table"].insert(0, item.get("value"))

        else:  # Regular field
            if current_column:
                updated_field = {
                    "fieldname": item.get("fieldname") if item.get("fieldname") else '',
                    "fieldtype": item.get("fieldtype") if item.get("fieldtype") else '',
                    "parent": item.get("parent")if item.get("parent") else "",
                    "label": item.get("label") if item.get("label") else "",
                    "description": item.get("description") if item.get("description") else "",
                    "reqd": item.get("reqd"),
                    "options": item.get("options") if item.get("options") else [],
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
        }
        .main-body{
            margin: 5px;
            border: 1px solid #000;
            padding: 15px;
            border-radius: 5px;
        }
        .row {
            display: flex;
              align-items: start;
            margin-bottom: 5px;
        }
        .column {
            flex: 1;
            padding:0px 15px;
        }
        .section h3 {
            margin: 5px 0;
            font-size:13px;
        }
        .section h4 {
            margin: 5px 0;
            font-size:13px;
        }
        .section {
            border: 0px solid #ccc;
            border-radius:3px;
            margin-bottom:3px;
            margin-top: 5px;
        }
        .section h3 {
            margin-bottom: 10px;
            font-size: 15px;
            font-weight:700;
        }
        .column .columnlabel {
            margin: 5px 0;
            font-size:14px;
            padding: 0px 4px;
            font-weight:600;
        }
        .field {
            display: flex;
            padding: 2px 0px;
            margin: 8px 4px;
        }
        .field label {
            font-weight: bold;
            white-space: nowrap;
            margin-right: 2px;
            font-size: 13px;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .field input {
            border: none;
            outline: none;
            padding: 0px 5px;
            padding-left: 4px ;
            background: transparent;
            flex: 1;
            font-weight:500;
            color:#000;
            font-size: 13px;
        }
        .block_input{
            border: none;
            outline: none;
            padding: 0px 5px;
            padding-left: 50px ;
            background: transparent;
            flex: 1;
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
            resize: none;
            overflow-y: hidden;
        }
        .field input[type="checkbox"], .field input[type="radio"] {
            flex: 0;
            width: 16px;
            height: 16px;
            margin-left: 5px;
            border: 1px solid #000;
        }
        .field-textarea {
            display: block;
        }
        .header-container{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #000;
        }
        .checkbox-container {
            display: flex;
            justify-content: flex-start;
            flex-wrap: wrap;
            gap: 10px;
            width: 100%;
        }
        .checkbox-container > .checkbox-gap {
            flex: 1 0 calc(33.33% - 20px);
            box-sizing: border-box;
            display: flex;
            gap: 15px;
            margin-top: 10px;
            margin-bottom: 10px;
            min-width: 150px;
        }
        .custom-checkbox {
            display: inline-block;
            width: 20px !important;
            height: 20px !important;
            border: 2px solid #007bff;
            border-radius: 4px;
            background-color: #007bff;
            position: relative;
            margin:3px;
            margin-bottom:0px;
            flex-shrink: 0;
        }
        .custom-checkbox::before {
            content: '✔';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 16px;
            color: white;
            font-weight: bold;
        }
        .custom-checkbox.disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .custom-checkbox.checked {
            background-color: #007bff;
            border-color: #007bff;
        }
        .custom-checkbox.unchecked {
            background-color: #fff;
            border-color: #ccc;
        }
        .footer-container{
            display: flex;
            justify-content: center;
            padding: 10px;
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
            min-width: 40px;
            max-width: 40px;
        }
        .childtablename{
            font-size:13px;
            font-weight:600 !important;
            margin-bottom: 3px !important;
        }
        .Form_name_div{
            display: flex;
            justify-content: center;
            text-align: center;
            margin: 0px 10px;
        }
        .form-title {
            font-size: 20px;
            max-width: 600px;
            word-wrap: break-word;
        }
        .header-right{
            min-width: 280px;
        }
        .description-block{
            font-size:12px;
        }
        .watermark {
            position: fixed;
            top: 50%;
            left: 30%;
            font-size: 80px;
            color: rgba(0, 0, 0, 0.1);
            transform: rotate(-30deg);
            z-index: 0;
            pointer-events: none;
            user-select: none;
            white-space: nowrap;
        }
        .requestId{
            display: flex;
            justify-content: start;
            align-items: center;
            padding-top:5px;
            padding-bottom:5px;
            padding-left:4px;
        }
        .requestId strong {
            margin-right: 8px;
        }
        .rounded-table {
            width: 100%;
            margin-bottom: 5px;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 3px;
            overflow: hidden;
        }
        .attachments {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            object-fit: contain;
            background-color: #f9f9f9;
        }
        @media print {
            body {
                background: #fff !important;
                color: #000 !important; 
                font-family: Arial, sans-serif;
            }
            .main-body {
                border: 1px solid #000 !important;
                box-shadow: none !important;
                margin: 0 !important;
                padding: 10px !important;
            }
            .header-container {
                border-bottom: 1px solid #000 !important;
                padding-bottom: 8px !important;
                margin-bottom: 10px !important;
            }
            .form-title, .header-container h4 {
                font-size: 22px !important;
                font-weight: bold !important;
                color: #000 !important;
            }
            .section {
                border: 0px solid #ccc !important;
                border-radius: 3px !important;
                margin-bottom: 10px !important;
                page-break-inside: avoid;
            }
            .section h3, .columnlabel, .childtablename {
                color: #000 !important;
                font-weight: 700 !important;
                font-size: 15px !important;
                margin-bottom: 6px !important;
            }
            .rounded-table, .rounded-table th, .rounded-table td {
                
                font-size: 13px !important;
                color: #000 !important;
            }
            .rounded-table th {
                background: #f2f2f2 !important;
                font-weight: bold !important;
            }
            .rounded-table td {
                background: #fff !important;
            }
            .field label {
                color: #000 !important;
                font-weight: bold !important;
                font-size: 13px !important;
            }
            .field input, .field textarea, .field select {
                color: #000 !important;
                background: transparent !important;
                border: none !important;
                font-size: 13px !important;
            }
            .custom-checkbox.checked {
                background-color: #007bff !important;
                border-color: #007bff !important;
            }
            .custom-checkbox.unchecked {
                background-color: #fff !important;
                border-color: #ccc !important;
            }
            .custom-checkbox::before {
                color: #fff !important;
            }
            .checkbox-gap {
                margin: 10px 0px !important;
            }
            .attachments {
                border: 1px solid #ccc !important;
                border-radius: 4px !important;
                background: #f9f9f9 !important;
                box-shadow: none !important;
            }
            .watermark {
                display: block !important;
                color: rgba(0, 0, 0, 0.1) !important;
            }
            .footer-container {
                border-top: 1px solid #000 !important;
                margin-top: 10px !important;
                padding-top: 8px !important;
                background: none !important;
            }
            .description-block {
                color: #000 !important;
                font-size: 12px !important;
            }
            .requestId {
                color: #000 !important;
                font-size: 13px !important;
                font-weight: bold !important;
            }
            .logo-div img {
                height: 45px !important;
                margin-bottom: 0px !important;
            }
            .signature-Imge {
                min-width: 40px !important;
                max-width: 40px !important;
            }
            .column {
                padding: 0px 0px !important;
            }
            .row {
                margin-bottom: 5px !important;
            }
            .field {
               
                padding: 4px 0px !important;
            }
            .Form_name_div {
                margin: 0px 10px !important;
            }
            .header-right {
                min-width: 200px !important;
            }
            .childtablename {
                font-size: 13px !important;
                font-weight: 600 !important;
            }
            .rounded-table th, .rounded-table td {
                page-break-inside: avoid !important;
            }
            
        }
    </style>
    </head>
<body>
<div class="main-body">

<div class="watermark">{{bu_name}}</div>

<div class="header-container">
  <div class="header-right">
    {% set value = letter_head %}
    {% set char_count = value | length %}
    {% set newline_count = value.count('\n') %}
    {% set est_line_length = 100 %}
    {% set wrapped_lines = (char_count // est_line_length) %}
    {% set estimated_lines = wrapped_lines + newline_count + 1 %}
    {% set line_height = 16 %}
    {% set height = estimated_lines * line_height %}

    {% if value %}
        {% set lines = value.split('\n') %}
    {% else %}
        {% set lines = [] %}
    {% endif %}

    <div style="height: {{ height }}px; border: none; width: 100%; margin-bottom: 0px; padding-bottom: 0px; line-height: {{ line_height }}px;">
        <div style="font-weight: bold;font-size: 15px;">{{ lines[0] }}</div>
        {% for line in lines[1:] %}
            <div style="font-size: 13px;">{{ line }}</div>
        {% endfor %}
    </div>
</div>

    <div class="Form_name_div">
        <h4 class="form-title" style="font-size:20px;">{{ form_name }}</h4>
    </div>
    
    <div class="logo-div"> 
        <img class="img-fluid " src="{{ company_logo }}" alt="logo" style="height: 55px; margin-bottom:0px">
     </div>
    
</div>
{% if wf_generated_request_id %}
<div class="requestId"><strong>Request ID:</strong><span>{{wf_generated_request_id}}</span></div>
{% endif %}
{% for block in data %}
    <div class="block">
        {% for section in block.sections %}
        
            <div class="section">
                {% if section.label %}
                    <h3 style="padding-left:3px;">{{ section.label }}</h3>
                {% endif %}
                
                {% for row in section.rows | sort(attribute='idx') %}
                
                                            
                            {% set table_name = row.fieldname %}

                            {% if row.description == 'true' %}
                                {% if table_name in child_data %}
                                
                                    <h3 class="childtablename" style="font-size: 14px;">{{ row.label.replace("_", " ").title() }}</h3>
                                    {% if child_data[table_name] %}
                                 
                                        {% for child in child_data[table_name] %}
                                            <div style="border:1px solid #ccc; padding:10px; margin-bottom:5px;">
                                                
                                                <div style="display: flex; flex-wrap: wrap;">
                                                    {% for key, value in child.items() %}
                                                       <div style="width: 48%; display:flex;gap:2px; margin-right: 2%; margin-bottom: 10px;">
                                                            <label style="font-weight: 600;font-size: 13px;">{{ key }}:</label><br />
                                                            <span style="font-size:13px; font-weight:500; margin-left: 2%;">
                                                            {{ value}}
                                                            </span>
                                                           
                                                        </div>

                                                    {% endfor %}
                                                </div>
                                            </div>
                                        {% endfor %}

                                    {% endif %}

                                {% elif table_name in child_table_data %}
                                    <h3 class="childtablename" style="font-size: 14px;">{{ row.label.replace("_", " ") }}</h3>
                                    <div style="border:1px solid #ccc; padding:10px; margin-bottom:5px;font-size: 13px;">
                                    
                                        <div style="display: flex; flex-wrap: wrap;">
                                            {% for column in child_table_data[table_name] %}
                                                <div style="width: 48%; margin-right: 2%;display:flex;align-items:baseline;gap:2px; margin-bottom: 10px;">
                                                    <label style="font-weight: 600;font-size: 13px;">{{ column }}:</label><br />
                                                    <input type="text"  readonly class="block_input" style="width: 100%;  color: #ccc;font-size: 13px;" />
                                                </div>
                                            {% endfor %}
                                        </div>
                                    </div>
                                {% endif %}

                            {% else %}
                            

                                {% if table_name in child_data %}
                                
                                
                                    <h3 class="childtablename" style=margin-left:3px;margin-right:3px;font-size: 14px;>{{ row.label.replace("_", " ").title() }}</h3>
                                        {% if child_data[table_name] %}
                                            <table class="rounded-table" style="width: 100%;border-collapse: collapse; border-radius: 3px; margin-left:3px; margin-right:3px;">
                                                <thead>
                                                    <tr>
                                                        
                                                        {% for key in child_data[table_name][0].keys() %}
                                                            <th style="border: 1px solid #ccc;text-align:center; padding: 8px; background-color: #f2f2f2; font-size: 13px;">{{ key }}</th>
                                                        {% endfor %}
                                                    </tr>
                                                </thead>
                                               
                                                {% set keywords = ['total', 'amount', 'total cost', 'sub total'] %}
                                                <tbody>
                                                    {% for child in child_data[table_name] %}
                                                        {% set is_summary_row = child.values() | select('string') | map('lower') | select('in', keywords) | list | length > 0 %}
                                                        <tr>
                                                            {% for value in child.values() %}
                                                                 <td style="
                                                                    {% if is_summary_row %}
                                                                        border-bottom: 1px solid #ccc;
                                                                        {% if loop.first %}border-left: 1px solid #ccc;{% endif %}
                                                                        {% if loop.last %}border-right: 1px solid #ccc;{% endif %}
                                                                    {% else %}
                                                                        border: 1px solid #ccc;
                                                                    {% endif %}
                                                                    text-align: center;
                                                                    padding: 8px;
                                                                    word-break: break-word;
                                                                    font-size: 13px;
                                                                ">
                                                                    {% if value %}
                                                                        {% if "/" in value %}
                                                                            {{ value.replace('/files/', '') }}
                                                                        {% else %}
                                                                            {{ value }}
                                                                        {% endif %}
                                                                    {% else %}
                                                                        {{ ' ' }}
                                                                    {% endif %}
                                                                </td>
                                                            {% endfor %}
                                                        </tr>
                                                    {% endfor %}
                                                </tbody>


                                            </table>
                                        {% endif %}




                                    {% elif table_name in child_table_data %}
                                
                                    <h3 class="childtablename" style="font-size: 14px;">{{ row.label.replace("_", " ").title() }}</h3>
                                    <table class="rounded-table" style="width: 100%; margin-bottom:10px; border-collapse: collapse; border-radius: 3px;">
                                        <thead>
                                            <tr>
                                                <th style="border: 1px solid #ccc;width:3%; padding: 8px; background-color: #f2f2f2;font-size: 13px;">S.no</th>
                                                {% for column in child_table_data[table_name] %}
                                                    <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2; font-size: 13px;">{{ column }}</th>
                                                {% endfor %}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td style="border: 1px solid #ccc; padding: 8px; text-align: center;font-size: 13px;">-</td>
                                                {% for column in child_table_data[table_name] %}
                                                    <td style="border: 1px solid #ccc; padding: 8px; text-align: center; color: #ccc;font-size: 13px;">-</td>
                                                {% endfor %}
                                            </tr>
                                        </tbody>
                                    </table>
                                   
                                {% endif %}
                            {% endif %}

                    

                    <div class="row" style="display: flex;">
                        {% for column in row.columns %}
                       
                            <div class="column">
                              {% if column.label %}
                                <h3 class="columnlabel">{{ column.label }}</h3>
                                {% endif %}
                                {% for field in column.fields %}
                                    
                                    <div class="field {% if field.fieldtype == 'Text' or field.fieldtype == 'Small Text' %}field-textarea{% endif %}">
                                    
                                     {% if field.fieldtype == 'Check' and field.fieldname != 'auto_calculations' %}
                                            <div class="checkbox-gap" style="display: flex; align-items: start; gap: 8px;">
                                                <!-- Checkbox -->
                                                <span class="custom-checkbox {% if field['values'] %}checked{% else %}unchecked{% endif %}" style="margin-top:-10px;"></span>
                                                <!-- Label -->
                                                <label style="margin-top:-7px;" for="{{ field.fieldname }}">
                                                    {{ field.label }} <span style="padding-left:2px; font-size: 13px;"></span>
                                                </label>
                                            </div>
                                        {% elif field.fieldname != 'auto_calculations' %}
                                            <label for="{{ field.fieldname }}">
                                                {{ field.label }} <span style="padding-left:2px; font-size: 13px;">:</span>
                                            </label>
                                        {% endif %}
                                        {% if field.fieldtype in ['radio'] %}
                                            <div class="container-fluid">
                                                <div class="row">
                                                    {% if field.options is string %}
                                                        {% set options = field.options.split('\n') %}
                                                    {% else %}
                                                        {% set options = field.options %}
                                                    {% endif %}
                                                    {% for option in options %}
                                                        <div class="form-check col-4 mb-4">
                                                            <div>
                                                            
                                                                {% if field.fieldtype == 'Check'  %}
                                                                 {{option}}
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
                                     

                                        {% elif field.fieldtype == 'Data' or field.fieldtype == 'Int' or field.fieldtype =='Link' and field.fieldname != 'auto_calculations' %}
                                            <span id="{{ field.fieldname }}"
                                                style="font-size:13px; font-weight:500; word-break: break-all;">
                                                {{ field['values'] }}
                                            </span>
                                        {% elif field.fieldtype == 'Select' %}
                                        
                                        {% if field['values'] %}
                                         <span id="{{ field.fieldname }}"
                                                style="font-size:13px; font-weight:500;">
                                                {{ field['values'] }}
                                            </span>
                                            
                                        {% else %}
                                            {% set options = field.options.strip().split('\n') if field.options else [] %}
                                            <div class="checkbox-container">
                                                {% for option in options if option %}
                                                    <div class="checkbox-gap">
                                                        <span class="custom-checkbox unchecked"></span>
                                                        <span style="margin-top:4px; margin-left:4px;">{{ option }}</span>
                                                    </div>
                                                {% endfor %}
                                            </div>
                                        {% endif %}

                                        
                                       {% elif field.fieldtype == 'Small Text' %}
                                        {% if field.options %}
                                            {% set options = field.options.strip().split('\n') %}
                                        {% else %}
                                            {% set options = field.options %}
                                        {% endif %}
                                            {% if field['values'] %}
                                                {% set selected_values = field['values'] | replace('["', '') | replace('"]', '') | replace('","', ',') %}
                                                {% set selected_values_list = selected_values.split(',') %}
                                                <div class="checkbox-container">
                                                    {% for value in selected_values_list if value %}
                                                        <div class="checkbox-gap">
                                                            <span class="custom-checkbox checked"></span>
                                                            <span style="margin-left:3px; margin-top:3px;" >{{ value }}</span>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            {% else %}
                                                <div class="checkbox-container">
                                                    {% for option in options if option %}
                                                        <div class="checkbox-gap">
                                                            <span class="custom-checkbox unchecked"></span>
                                                           <span style="margin-top:4px; margin-left:4px;"> {{ option }}</span>
                                                        </div>
                                                    {% endfor %}
                                                </div>
                                            {% endif %}
                                        {% elif field.fieldtype == 'Attach' %}
                                            {% if field['values'] %}
                                                {% if field.fieldtype == 'Attach' and (field.fieldname.startswith('approved_by') or field.fieldname.startswith('requestor')or field.fieldname.startswith('acknowle')) %}
                                                    <img  
                                                        id="{{ field.fieldname }}" 
                                                        src="{{ site_url + field['values'] or '' }}" 
                                                        style="max-width: 60px; max-height: 50px; object-fit: contain;margin-top:-10px;"  
                                                        name="{{ field.fieldname }}"
                                                    >
                                                {% else %}
                                                    <ul style="padding-left: 20px; margin: 0px 0;">
                                                        {% for file in field['values'].split(',') %}
                                                            <li style="font-size:12px;">
                                                                {{ file.strip().split('@')[-1] if '@' in file else file.strip().split('/')[-1] }}
                                                            </li>
                                                        {% endfor %}
                                                    </ul>
                                                {% endif %}
                                            {% else %}
                                                <input 
                                                    type="text" 
                                                    id="{{ field.fieldname }}" 
                                                    value="{{ field['values'] }}" 
                                                    name="{{ field.fieldname }}"
                                                >
                                            {% endif %}

                                        {% elif field.fieldtype == 'Phone' %}
                                             <span id="{{ field.fieldname }}" style="font-size:13px; font-weight:500;" name="{{ field.fieldname }}" class="date-span">
                                                {{ field['values'] }}
                                            </span>
                                        {% elif field.fieldtype == 'Time' %}
                                             <span id="{{ field.fieldname }}" style="font-size:13px; font-weight:500;" name="{{ field.fieldname }}" class="date-span">
                                                {{ field['values'] }}
                                            </span>
                                        {% elif field.fieldtype == 'Color' %}
                                            <input type="color" id="{{ field.fieldname }}" value="{{ field['values'] }}" name="{{ field.fieldname }}">
                                         {% elif field.fieldtype == 'Text' %}
                                                {% set value = field['values'] %}
                                                {% set char_count = value | length %}
                                                {% set newline_count = value.count('\n') %}
                                                {% set est_line_length = 60 %}
                                                {% set wrapped_lines = (char_count // est_line_length) %}
                                                {% set estimated_lines = newline_count + wrapped_lines %}
                                                {% if estimated_lines < 2 %}
                                                    {% set estimated_lines = 2 %}
                                                {% endif %}
                                                {% set line_height = 18 %}
                                                {% set height = estimated_lines * line_height %}
                                            <div
                                                id="{{ field.fieldname }}"
                                                name="{{ field.fieldname }}"
                                                style="white-space: pre-wrap; border: none; width: 100%; font-size:13px;"
                                            >{{ field['values'] | e }}</div>



                                        {% elif field.fieldtype == 'Date' %}
                                            <span id="{{ field.fieldname }}" style="font-size:13px; font-weight:500;" name="{{ field.fieldname }}" class="date-span">
                                                {{ field['values'] }}
                                            </span>

                                        {% elif field.fieldtype == 'Datetime' %}
                                            <span id="{{ field.fieldname }}"
                                                style="font-size:13px; font-weight:500;">
                                                {{ field['values'] }}
                                            </span>
                        
                                        {% elif field.fieldtype == 'Signature' %}
                                            <input type="text" id="{{ field.fieldname }}" name="{{ field.fieldname }}" placeholder="Signature input (future implementation)">
                                        {% endif %}
                                        
                                    </div>
                                         {% if field.description != 'Field' and field.fieldname != 'auto_calculations' and field.description != 'Disable' %}
                                            <div class="w-100 description-block mt-1">
                                               
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
activate_log_table = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Activity Log</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 2rem;
      background-color: #f9f9f9;
    }
    h1 {
      margin-bottom: 1rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: #fff;
      box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    th, td {
      padding: 0.75rem;
      text-align: left;
      border-bottom: 1px solid #e0e0e0;
    }
    th {
      background-color: #f0f0f0;
    }
    tr:nth-child(even) {
      background-color: #fcfcfc;
    }
  </style>
</head>
<body>
  <h1>Activity Log</h1>
  <table>
    <thead>
      <tr>
        <th>Designation</th>
        <th>Employee</th>
        <th>Action</th>
        <th>Time</th>
        <th>Comments</th>
      </tr> 
    </thead>
    <tbody>
      {% for entry in filtered_reasons %}
      <tr>
        <td>{{ entry.role }}</td>
        <td>{{ entry.user_name }}</td>
        <td>{{ entry.action }}</td>
        <td>{{ entry.time.rsplit(':', 1)[0] }}</td>
        <td>{{ entry.reason }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>"""

def convert_html_to_pdf(html_content, pdf_path,options=None):

    try:
        pdfkit.from_string(html_content, pdf_path,options=options)
    except Exception as e:
        frappe.log_error(f"PDF generation failed: {e}")
 
def json_structure_call_for_html_view(json_obj: list, form_name: str, child_data, child_table_data,business_unit,wf_generated_request_id=None,mail_attachment=None):
   
    if wf_generated_request_id:
        wf_generated_request_id=wf_generated_request_id
    else:
        wf_generated_request_id = None
    if child_data is None:
        child_data = []
    site_url = frappe.utils.get_url()
    logo_of_company = site_url + "/files/company.png"
    if child_table_data is None:
        child_table_data = []
    
    structered_data = rebuild_to_structured_array(flat_array=json_obj)
    if structered_data is None:
        structered_data = []  # Ensure it's iterable
 
    business_unit = frappe.get_doc("Ezy Business Unit",business_unit)
    
    company_logo = business_unit.bu_logo 
    letter_head = ''
    bu_name =''

    
    if business_unit.letter_head:
        letter_head = business_unit.letter_head
        
    if company_logo:
        
        logo_of_company = site_url + company_logo
        
    if business_unit.water_mark:
       
        if business_unit.bu_name:
            bu_name = business_unit.bu_name


    html_output = Template(template_str).render(
        data=structered_data, form_name=form_name, child_data=child_data,letter_head=letter_head, child_table_data=child_table_data,company_logo=logo_of_company,site_url=site_url,bu_name=bu_name,wf_generated_request_id=wf_generated_request_id,mail_attachment=mail_attachment or ''
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
        
        site = frappe.local.site
        bench_path = frappe.utils.get_bench_path()
        public_files_folder = os.path.join(bench_path, "sites", site, "public", "files")
        attachment_folder = os.path.join(public_files_folder, "Attachment_folder")
        os.makedirs(attachment_folder, exist_ok=True)

        print_format = frappe.db.get_value("Ezy Form Definitions", form_short_name, "print_format")
        wf_generated_request_id = frappe.get_value(form_short_name, name, "wf_generated_request_id")
        activate_log = frappe.get_doc('WF Activity Log', wf_generated_request_id).as_dict()

        filtered_reasons = [
            {
                'level': entry['level'],
                'role': entry['role'],
                'user': entry['user'],
                'user_name': entry['user_name'],
                'reason': entry['reason'],
                'action': entry['action'],
                'time': entry['time'],
                'random_string': entry['random_string']
            }
            for entry in activate_log.get('reason', [])
        ]

        html_table_output = ""
        if filtered_reasons:
            html_table_output = Template(activate_log_table).render(filtered_reasons=filtered_reasons)

        mail_attachment = []
        html_view = ""

        if print_format:
            html_view_ = get_html_file_data(form_short_name, name, print_format)
            html_view = html_view_['html']
        else:
            json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
            json_object = literal_eval(json_object)["fields"]
            user_doc = frappe.get_doc(form_short_name, name).as_dict()
            data_list = {}

            for iteration in json_object:
                if "value" in iteration:
                    iteration["value"] = user_doc.get(iteration["fieldname"], "")

                # Main form attachments
                if iteration.get("fieldtype") == "Attach" and iteration.get("value"):
                    # Split by comma and strip whitespace
                    file_urls = [url.strip() for url in iteration["value"].split(",") if url.strip()]
                    
                    for file_url in file_urls:
                        
                        attachment_info = {
                            "label": 'Form Attachments',
                            "file_url": file_url,
                            "file_path": os.path.join(public_files_folder, file_url.replace("/files/", ""))
                        }

                        if iteration.get("fieldname") and not iteration.get("fieldname").lower().startswith(
                                ("approved_by", "requestor", "acknowle")):
                            mail_attachment.append(attachment_info)

                # Child table attachments
                if iteration.get("fieldtype") == "Table":
                    child_table_name = str(iteration["fieldname"])
                    child_table_records = frappe.get_all(
                        iteration["options"],
                        filters={"parent": name},
                        fields=["*"],
                        order_by="idx asc"
                    ) 
                    meta_fields = frappe.get_meta(iteration["options"]).fields
                    field_names = [df.fieldname for df in meta_fields]
                    field_labels = {df.fieldname: df.label for df in meta_fields}
                    field_types = {df.fieldname: df.fieldtype for df in meta_fields}

                    for record in child_table_records:
                        for field in field_names:
                            value = record.get(field)
                            fieldtype = field_types.get(field)
                            # if fieldtype =='int':
                            if fieldtype == "Attach" and value:
                                file_urls = [url.strip() for url in value.split(',') if url.strip()]
                                for file_url in file_urls:
                                    mail_attachment.append({
                                        "label": "Form Attachments",
                                        "file_url": file_url,
                                        "file_path": os.path.join(public_files_folder, file_url.replace("/files/", ""))
                                    })
                                    

                    data_list[child_table_name] = [
                                    {field_labels.get(field, field): record.get(field) for field in field_names}
                                    for record in child_table_records
                                ]
                    data_list[child_table_name] = [
                        {
                            k: (
                                v.isoformat() if isinstance(v, (date, datetime)) 
                                else str(v) if isinstance(v, int) 
                                else v
                            )
                            for k, v in item.items()
                        }
                        for item in data_list[child_table_name]
]
                    ######
                    

            # Remove empty "approved"/"approver" fields
            json_object = list(filter(lambda d: not (
                ('value' in d and not d.get('value')) and
                (d.get('fieldname').startswith('approved') or d.get('fieldname').startswith('approver'))
            ), json_object))

            form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name") or "Form"
            html_view = json_structure_call_for_html_view(
                json_obj=json_object,
                form_name=form_name,
                child_data=data_list,
                child_table_data=None,
                business_unit=business_unit
            )
    
    return html_view
 
 
 


def add_file_to_zip(item, zipf, zip_folder_name="Attachments"):
    """Add file to zip under a folder if file_path exists."""
    if os.path.exists(item["file_path"]):
        zipf.write(
            item["file_path"],
            arcname=os.path.join(zip_folder_name, os.path.basename(item["file_path"]))
        )
    else:
        frappe.log_error(f"File not found: {item['file_path']}")

        
        
@frappe.whitelist()
def download_filled_form(form_short_name: str, name: str|None,business_unit=None,from_raise_request=None):
    """Generates a PDF for the dynamic form with filled data"""
    try:
        bench_path         = get_bench_path()
        site               = frappe.local.site
        folder_path = get_site_path("public", "files", "Attachment_folder")
        form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name")
        delete = lambda path: os.unlink(path) if os.path.isfile(path) or os.path.islink(path) else shutil.rmtree(path)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            [delete(os.path.join(folder_path, f)) for f in os.listdir(folder_path)]
        attachment_info =None
        is_landscape = frappe.db.get_value("Ezy Form Definitions", form_short_name, "is_landscape")
        if name is None:
            print_format = frappe.db.get_value("Ezy Form Definitions", form_short_name, "print_format")
            if print_format:
                html_view_ = get_html_file_data("DocType",form_short_name,str(print_format))
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
                            fields=["label"],
                            order_by="idx asc"
                        )
 
                        # Store labels for each child table
                        labels[child_table_name] = [field["label"] for field in child_table_fields]
                form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name")
                html_view = json_structure_call_for_html_view(json_obj=json_object, form_name=form_name,child_table_data=labels,child_data=None,business_unit=business_unit,wf_generated_request_id='',mail_attachment=None)
            random_number = randint(111, 999)
 
            pdf_filename = f"{form_short_name}_{random_number}  .pdf"
            pdf_path = f"private/files/{pdf_filename}"
            absolute_pdf_path = os.path.join(get_bench_path(), "sites", cstr(frappe.local.site), pdf_path)
            opts={"orientation":"Landscape"if is_landscape else"Portrait"}
            convert_html_to_pdf(html_content=html_view,pdf_path=absolute_pdf_path,options=opts)
 
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
            
            site = frappe.local.site
            bench_path = frappe.utils.get_bench_path()
            public_files_folder = os.path.join(bench_path, "sites", site, "public", "files")
            attachment_folder = os.path.join(public_files_folder, "Attachment_folder")
            os.makedirs(attachment_folder, exist_ok=True)

            print_format = frappe.db.get_value("Ezy Form Definitions", form_short_name, "print_format")
            wf_generated_request_id = frappe.get_value(form_short_name, name, "wf_generated_request_id")
            activate_log = frappe.get_doc('WF Activity Log', wf_generated_request_id).as_dict()

            filtered_reasons = sorted([{ 'level': entry['level'],'role': entry['role'], 'user': entry['user'], 'user_name': entry['user_name'], 'reason': entry['reason'], 'action': entry['action'], 'time': entry['time'], 'random_string': entry['random_string']  }  for entry in activate_log.get('reason', [])  ],key=lambda x: datetime.strptime(x['time'], "%Y/%m/%d %H:%M:%S:%f") if x.get('time') else datetime.min )
            html_table_output = ""
            if filtered_reasons:
                html_table_output = Template(activate_log_table).render(filtered_reasons=filtered_reasons)

            mail_attachment = []
            html_view = ""

            if print_format:
                html_view_ = get_html_file_data(form_short_name, name, print_format)
                html_view = html_view_['html']
            else:
                json_object = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_json")
                json_object = literal_eval(json_object)["fields"]
                user_doc = frappe.get_doc(form_short_name, name).as_dict()
                data_list = {}

                for iteration in json_object:
                    if "value" in iteration:
                        iteration["value"] = user_doc.get(iteration["fieldname"], "")

                    # Main form attachments
                    if iteration.get("fieldtype") == "Attach" and iteration.get("value"):
                        # Split by comma and strip whitespace
                        file_urls = [url.strip() for url in iteration["value"].split(",") if url.strip()]
                        
                        for file_url in file_urls:
                            
                            attachment_info = {
                                "label": 'Form Attachments',
                                "file_url": file_url,
                                "file_path": os.path.join(public_files_folder, file_url.replace("/files/", ""))
                            }

                            if iteration.get("fieldname") and not iteration.get("fieldname").lower().startswith(
                                    ("approved_by", "requestor", "acknowle")):
                                mail_attachment.append(attachment_info)

                    # Child table attachments
                    if iteration.get("fieldtype") == "Table":
                        child_table_name = str(iteration["fieldname"])
                        child_table_records = frappe.get_all(
                            iteration["options"],
                            filters={"parent": name},
                            fields=["*"],
                            order_by="idx asc"
                        ) 
                        meta_fields = frappe.get_meta(iteration["options"]).fields
                        field_names = [df.fieldname for df in meta_fields]
                        field_labels = {df.fieldname: df.label for df in meta_fields}
                        field_types = {df.fieldname: df.fieldtype for df in meta_fields}

                        for record in child_table_records:
                            for field in field_names:
                                value = record.get(field)
                                fieldtype = field_types.get(field)
                                # if fieldtype =='int':
                                if fieldtype == "Attach" and value:
                                    file_urls = [url.strip() for url in value.split(',') if url.strip()]
                                    for file_url in file_urls:
                                        mail_attachment.append({
                                            "label": "Form Attachments",
                                            "file_url": file_url,
                                            "file_path": os.path.join(public_files_folder, file_url.replace("/files/", ""))
                                        })
                                        

                        data_list[child_table_name] = [
                                        {field_labels.get(field, field): record.get(field) for field in field_names}
                                        for record in child_table_records
                                    ]
                        data_list[child_table_name] = [
                            {
                                k: (
                                    v.isoformat() if isinstance(v, (date, datetime)) 
                                    else str(v) if isinstance(v, int) 
                                    else v
                                )
                                for k, v in item.items()
                            }
                            for item in data_list[child_table_name]
]
                        ######
                        

                # Remove empty "approved"/"approver" fields
                json_object = list(filter(lambda d: not (
                    ('value' in d and not d.get('value')) and
                    (d.get('fieldname').startswith('approved') or d.get('fieldname').startswith('approver'))
                ), json_object))

                form_name = frappe.db.get_value("Ezy Form Definitions", form_short_name, "form_name") or "Form"
                html_view = json_structure_call_for_html_view(
                    json_obj=json_object,
                    form_name=form_name,
                    child_data=data_list,
                    child_table_data=None,
                    business_unit=business_unit,
                    wf_generated_request_id=wf_generated_request_id,
                    mail_attachment=mail_attachment
                )

            # Generate PDFs
            pdf_filename = f"{form_short_name or 'form'}.pdf"
            absolute_pdf_path = os.path.join(attachment_folder, pdf_filename)

            activate_pdf_name = "Activity Log .pdf"
            activate_pdf_path = os.path.join(attachment_folder, activate_pdf_name)

            opts = {"orientation": "Landscape" if is_landscape else "Portrait"}

            convert_html_to_pdf(html_content=html_view, pdf_path=absolute_pdf_path, options=opts)
            convert_html_to_pdf(html_content=html_table_output, pdf_path=activate_pdf_path)

            # Add generated PDFs to attachments
            mail_attachment.append({
                "label": "Attachment_folder",
                "file_url": f"/files/Attachment_folder/{activate_pdf_name}",
                "file_path": activate_pdf_path
            })
            mail_attachment.append({
                "label": "Attachment_folder",
                "file_url": f"/files/Attachment_folder/{pdf_filename}",
                "file_path": absolute_pdf_path
            })

            # Remove any files that do not exist
            mail_attachment = [item for item in mail_attachment if os.path.exists(item["file_path"])]

            # Create ZIP
            zip_folder_name = "Attachments"
            zip_filename = f"{form_name or 'form'}.zip"
            zip_path = os.path.join(attachment_folder, zip_filename)

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for item in mail_attachment:
                    add_file_to_zip(item, zipf, zip_folder_name=zip_folder_name)

            site_url = get_url()
            full_download_url = f"{site_url}/files/Attachment_folder/{zip_filename}"
            return full_download_url





    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error Downloading File", f"line No:{exc_tb.tb_lineno}\n{traceback.format_exc()}")
        frappe.throw(str(e))
        

from frappe.www.printview import get_html_and_style

def get_html_file_data(doc=None,data=None,print_format=None):
    
    html_file = get_html_and_style(doc,name=data,print_format=print_format,no_letterhead=None,letterhead=None,trigger_print=False,style=None,settings=None)
 
    return html_file




frappe.whitelist()
def get_wf_activate_log(wf_generated_request_id):
    """Fetches the activity log for a given workflow request ID."""
    try:
        activate_log = frappe.get_doc('WF Activity Log', wf_generated_request_id).as_dict()
        filtered_reasons = sorted(
            [
                {
                    'level': entry['level'],
                    'role': entry['role'],
                    'user': entry['user'],
                    'user_name': entry['user_name'],
                    'reason': entry['reason'],
                    'action': entry['action'],
                    'time': entry['time'],
                    'random_string': entry['random_string']
                }
                for entry in activate_log.get('reason', [])
            ],
            key=lambda x: x['time']
        )
        return filtered_reasons
    except Exception as e:
        frappe.log_error(f"Error fetching activity log: {e}")
        return []