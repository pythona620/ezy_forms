export function extractFieldsWithBreaks(data) {
  const result = [];
  let previousFieldname = null; // Track the previous fieldname
  let index = 0;


  data.forEach((section) => {
    section.rows.forEach((row) => {
      row.columns.forEach((column) => {

        column.fields.forEach((field) => {
          // Add the "insert_after" key to the current field
          const generatedFieldname = convertLabelToFieldName(field.label);
          result.push({
            ...field,
            fieldname: generatedFieldname,
            insert_after: previousFieldname,
            idx: index++, // Assign index
          });

          // Update previousFieldname for the next field in this column
          previousFieldname = generatedFieldname;
        });
        const columnFieldname = convertLabelToFieldName(column.label);

        // Add "Column Break" marker after each column
        result.push({
          fieldtype: "Column Break",
          doctype: "Custom Field",
          dt: column.dt,
          fieldname: columnFieldname,
          label: column.label,
          insert_after: previousFieldname, // Track the break
          idx: index++, // Assign index
        });

        // Update previousFieldname to the column break
        previousFieldname = columnFieldname;
      });
      const rowFieldname = convertLabelToFieldName(row.label);
      // Add "Row Break" marker after each row
      result.push({ fieldtype: "Column Break", doctype: "Custom Field", fieldname: rowFieldname, dt: row.dt, insert_after: previousFieldname, idx: index++ });
      // Update previousFieldname to the row break
      previousFieldname = rowFieldname;
    });
    const sectionFieldname = convertLabelToFieldName(section.label);
    // Add "Section Break" marker after each section
    result.push({ fieldtype: "Section Break", doctype: "Custom Field", label: section.label, dt: section.dt, fieldname: sectionFieldname, insert_after: previousFieldname, idx: index++ });
    // Update previousFieldname to the section break
    previousFieldname = sectionFieldname;
  });

  return result;
}

// Usage
// const flattenedFieldsWithBreaks = extractFieldsWithBreaks(dataObj);
// console.log(flattenedFieldsWithBreaks);



export function rebuildOriginalStructure(flatArray) {
  const result = [];
  let currentSection = null;
  let currentRow = null;
  let currentColumn = null;

  flatArray.forEach((item) => {
    if (item.type === "Section Break") {
      // Start a new section
      currentSection = {
        fieldtype: "Section Break",
        fieldname: item.fieldname,
        rows: []
      };
      result.push(currentSection);
    } else if (item.type === "Row Break") {
      // Start a new row
      currentRow = {
        fieldtype: "Row Break",
        fieldname: item.fieldname,
        columns: []
      };
      currentSection.rows.push(currentRow);
    } else if (item.type === "Column Break") {
      // Start a new column
      currentColumn = {
        fieldtype: "Column Break",
        fieldname: item.fieldname,
        label: item.label,
        fields: []
      };
      currentRow.columns.push(currentColumn);
    } else {
      // Add a field to the current column
      const { insert_after, ...fieldData } = item; // Remove the helper key
      currentColumn.fields.push(fieldData);
    }
  });

  return result;
}

// Usage
// const flatArray = [
//   { fieldname: "user_name", fieldtype: "data", label: "User Name", insert_after: null },
//   { fieldname: "user_id", fieldtype: "data", label: "User ID", insert_after: "user_name" },
//   { type: "Column Break", fieldname: "col_tac", label: "User Info" },
//   { fieldname: "user_mobile", fieldtype: "data", label: "User Mobile", insert_after: null },
//   { fieldname: "user_email", fieldtype: "data", label: "User Email", insert_after: "user_mobile" },
//   { type: "Column Break", fieldname: "col_tac", label: "User Data" },
//   { type: "Row Break", fieldname: "row_tac" },
//   { fieldname: "user_father_name", fieldtype: "data", label: "User Father Name", insert_after: null },
//   { fieldname: "user_mother_name", fieldtype: "data", label: "User Mother Name", insert_after: "user_father_name" },
//   { type: "Column Break", fieldname: "col_tac", label: "User Info1" },
//   { fieldname: "user_address", fieldtype: "data", label: "User House No", insert_after: null },
//   { type: "Column Break", fieldname: "col_tac", label: "User Data" },
//   { type: "Row Break", fieldname: "row_tac" },
//   { type: "Section Break", fieldname: "proprty_tac" }
// ];

// const originalStructure = rebuildOriginalStructure(flatArray);
// console.log(JSON.stringify(originalStructure, null, 2));

function convertLabelToFieldName(label) {
  return label
    .trim()                     // Remove leading/trailing spaces
    .toLowerCase()               // Convert to lowercase
    .replace(/\s+/g, '_')        // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, ''); // Remove non-alphanumeric characters except underscores
}