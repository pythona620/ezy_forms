// Copyright (c) 2024, bharath and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ezy Employee", {
    refresh: function(frm) {
        frm.fields_dict["responsible_units"].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ["name", "!=", frm.doc.company_field]  // Exclude company_field value
                ]
            };
        };
    },

    company_field: function(frm) {
        // Refresh responsible_units when company changes
        frm.refresh_field("responsible_units");
    }
});
