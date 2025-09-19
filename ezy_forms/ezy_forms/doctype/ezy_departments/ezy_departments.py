# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EzyDepartments(Document):
    pass



@frappe.whitelist()
def side_nav_department_and_forms(business_unit):
    departments_raw = frappe.db.sql(
        """SELECT DISTINCT owner_of_the_form,business_unit FROM `tabEzy Form Definitions` WHERE owner_of_the_form IS NOT NULL AND business_unit = %s""",
        (business_unit,),
        as_list=True
    )
    departments = [d[0] for d in departments_raw if d[0]]

    if not departments:
        return []
    placeholders = ', '.join(['%s'] * len(departments))
    query = f"""SELECT name, department_name 
                FROM `tabEzy Departments` 
                WHERE name IN ({placeholders}) AND business_unit = %s"""
    params = tuple(departments) + (business_unit,)
    department_names = frappe.db.sql(query, params, as_dict=True)

    return department_names