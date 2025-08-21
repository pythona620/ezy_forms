import frappe
from jinja2 import Template
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template import *





template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work Order</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .container { width: 100%; max-width: 1000px; margin: 20px auto; border: 1px solid #000; padding: 0; }
        .header-text { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-bottom: 1px solid black; }
        .header-text h2 { font-size: 16px; text-align: center; flex-grow: 1; }
        .form-section { padding: 15px; }
        .form-section table { width: 100%; border-collapse: collapse; }
        .form-section table td { padding: 5px; font-size: 14px; border: none; }
        .form-section table td .value { display: inline-block;  border-bottom: 0px solid black; font-size: 15px; padding: 2px 0; }
        .details-table { margin: 10px; margin-bottom: 20px; }
        .details-table table { width: 100%; border-collapse: collapse; }
        .details-table th, .details-table td { border: 1px solid #000; padding: 8px; font-size: 14px; text-align: left; }
        .details-table th { background-color: #f2f2f2; text-align: center; }
        .footer { padding: 10px; border-top: 1px solid #000; font-size: 14px; border-bottom: 1px solid black; }
        .authorization-section { margin-top: 20px; padding: 10px; }
         .header-right {
                min-width: 200px !important;
            }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-text">
                <div>
                    {% set value = doc.letter_head %}
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
                            <div style="font-size: 12px;">{{ line }}</div>
                        {% endfor %}
                        </div>
                </div>
                <div>
                <span style="font-weight: bold; font-size: 20px;">Work Order</span>
                </div>
                <div>
                    <img src={{doc.company_logo}} alt="Logo 2" style="height: 55px; margin-bottom:0px">
                </div>
           
        </div>

        <!-- Form Section -->
        <div class="form-section">
            <table>
                <tr>
                 <td>Request ID:</td>
                    <td><div class="value">{{ doc.wf_generated_request_id }}</div></td>
                </tr>
                <tr>
                     <td>Requested by:</td>
                    <td><div class="value">{{ doc.requested_by }}</div></td>
                    <td>Requested On:</td>
                    <td><div class="value">{{ doc.requested_on }}</div></td>
                </tr>
                <tr>
                   
                    <td>Vendor Name:</td>
                    <td><div class="value">{{ doc.vendor_name }}</div></td>
                    <td>GST Number:</td>
                    <td><div class="value">{{ doc.gst_number }}</div></td>
                </tr>
                <tr>
                    <td>Vendor Address:</td>
                    <td><div class="value">{{ doc.address }}</div></td>
                    <td>Phone:</td>
                    <td><div class="value">{{ doc.phone_number }}</div></td>
                </tr>
                
            </table>
        </div>

        <!-- Details Table -->
        <div class="details-table">
            <table>
                <thead>
                    <tr>
                        <th>ITEM NAME</th>
                        <th>UNIT</th>
                        <th>QUANTITY</th>
                        <th>UNIT PRICE</th>
                        <th>TOTAL PRICE</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in doc.pricing_details %}
                    <tr>
                        <td>{{ item.item_name }}</td>
                        <td>{{ item.item_unit_of_measure }}</td>
                        <td style="text-align: center;">{{ item.item_quantity }}</td>
                        <td style="text-align: center;">{{ item.unitPrice }}</td>
                        <td style="text-align: center;">{{ item.totalPrice }}</td>
                    </tr>
                    {% endfor %}
                    <tr>
                        <td colspan="4" style="text-align: right; font-weight: bold;">TOTAL:</td>
                        <td style="text-align: center;">{{ doc.total_value }}/-</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Footer -->
        <div class="footer"> 
           <div class="form-section">
               <table>
                    <tr>
                        <td>Delivery Time:</td>
                        <td><div class="value">{{ doc.delivery_time }}</div></td>
                        <td>CGST ({{ doc.cgst_percent }}%):</td>
                        <td><div class="value">{{ doc.cgst_amount }}</div></td>
                    </tr>

                    <tr>
                        <td>Payment Terms:</td>
                        <td><div class="value">{{ doc.payment_terms }}</div></td>
                        <td>UTGST ({{ doc.utgst_percent }}%):</td>
                        <td><div class="value">{{ doc.utgst_amount }}</div></td>
                    </tr>

                    <tr>
                        <td colspan="2" rowspan="4">
                        Note: At Hyatt, we view our suppliers as business<br>
                        partners who are committed to legal compliance<br>
                        and ethical conduct. By executing this Work Order,<br>
                        you acknowledge that your company abides by<br>
                        CGST@ Hyatt's Supplier Code of Conduct,<br>
                        which is available at Hyatt.com/supplier-code-of-conduct.<br>
                        Please contact your point person should you<br>
                        require this Code in your language.
                        </td>
                        <td>IGST ({{ doc.igst_percent }}%):</td>
                        <td><div class="value">{{ doc.igst_amount }}</div></td>
                    </tr>

                    <tr>
                        <td>Freight:<br>
                        <div> <span style="font-size: smaller;">
                        (Transportation/Shipping)
                        </span></div>
                        </td>
                        <td><div class="value">{{ doc.transportation_gst_amount }}</div></td>
                    </tr>

                    <tr>
                        <td>Additional Charges:</td>
                        <td><div class="value">{{ doc.additional_charges }}/-</div></td>
                    </tr>

                    <tr>
                        <td style="font-weight: bold;">Grand Total:</td>
                        <td><div class="value">{{ doc.grand_total }}/-</div></td>
                    </tr>
                </table>

            </div>
 
        </div>

        <!-- Authorization Section -->
       <div class="authorization-section">
            <div style="display: flex; justify-content: space-between; margin: 20px 0;">

                <div style="text-align: center; width: 20%;">
                <img src={{doc.approved_by_2}} alt="Received By" style="max-height: 50px; display:block; margin:0 auto; border-bottom:1px solid black;" />

                <span>Requested By</span>
                </div>

                <div style="text-align: center; width: 20%;">
                <img src={{doc.approved_by}} alt="Approved By" style="max-height: 50px; display:block; margin:0 auto; border-bottom:1px solid black;" />
                <p > Approved by</p>
                
                </div>

                <div style="text-align: center; width: 20%;">
                <img src={{doc.approved_by_1}} alt="Director Of Finance" style="max-height: 50px; display:block; margin:0 auto; border-bottom:1px solid black;" />
                <p >Approved by</p>
                </div>

                <div style="text-align: center; width: 20%;">
                <img src={{doc.approved_by_2}} alt="Received By" style="max-height: 50px; display:block; margin:0 auto; border-bottom:1px solid black;" />
                <p >Approved by</p>
                </div>

            </div>
        </div>

    </div>
</body>
</html>


"""
def preview_dynamic_form(form_data, form_short_name):
    site = frappe.local.site
    form_short_name ="Work Order"
    bench_path = frappe.utils.get_bench_path()
    public_files_folder = os.path.join(bench_path, "sites", site, "public", "files")
    attachment_folder = os.path.join(public_files_folder, "Attachment_folder")
    os.makedirs(attachment_folder, exist_ok=True)
    fields = form_data
    html = Template(template).render({"doc": form_data})
    opts = {"orientation": "Portrait"}
    pdf_filename = f"{form_short_name}.pdf"
    
    absolute_pdf_path = os.path.join(attachment_folder, pdf_filename)
    convert_html_to_pdf(html_content=html, pdf_path=absolute_pdf_path, options=opts)
    site_url = get_url()
    full_download_url = f"{site_url}/files/Attachment_folder/{pdf_filename}"
    return full_download_url


