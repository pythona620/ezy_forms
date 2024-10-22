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
            doctype: "Custom Field",
            dt: section.dt,
            description: "Field",
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
          dt: section.dt,
          fieldname: columnFieldname,
          label: column.label,
          description: "Column Break",
          insert_after: previousFieldname, // Track the break
          idx: index++, // Assign index
        });

        // Update previousFieldname to the column break
        previousFieldname = columnFieldname;
      });
      const rowFieldname = convertLabelToFieldName(row.label);
      // Add "Row Break" marker after each row
      result.push({ fieldtype: "Column Break", description: "Row Break", doctype: "Custom Field", fieldname: rowFieldname, dt: section.dt, insert_after: previousFieldname, idx: index++ });
      // Update previousFieldname to the row break
      previousFieldname = rowFieldname;
    });
    const sectionFieldname = convertLabelToFieldName(section.label);
    // Add "Section Break" marker after each section
    result.push({ fieldtype: "Section Break", description: "Section Break", doctype: "Custom Field", label: section.label, dt: section.dt, fieldname: sectionFieldname, insert_after: previousFieldname, idx: index++ });
    // Update previousFieldname to the section break
    previousFieldname = sectionFieldname;
  });

  return result;
}

// Usage
// const flattenedFieldsWithBreaks = extractFieldsWithBreaks(dataObj);
// console.log(flattenedFieldsWithBreaks);


export function rebuildToStructuredArray(flatArray) {
  const result = [];
  let currentSection = null;
  let currentRow = null;
  let currentColumn = null;

  for (let i = flatArray.length - 1; i >= 0; i--) {
    const item = flatArray[i];

    switch (item.description) {
      case "Section Break":
        // If there's an existing section, push it to the result before starting a new one
        if (currentSection) {
          result.unshift(currentSection); // Add to the beginning for correct order
        }
        currentSection = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          rows: [] // Initialize rows for the new section
        };
        currentRow = null; // Reset currentRow for new section
        break;

      case "Row Break":
        if (currentSection) {
          if (currentRow) {
            currentSection.rows.unshift(currentRow); // Push previous row into the section
          }
          currentRow = {
            fieldtype: "Row Break",
            fieldname: item.fieldname,
            columns: [] // Initialize columns for the new row
          };
        }
        break;

      case "Column Break":
        if (currentRow) {
          currentColumn = {
            fieldtype: item.fieldtype,
            fieldname: item.fieldname,
            label: item.label,
            fields: [] // Initialize fields for the new column
          };
          currentRow.columns.unshift(currentColumn); // Add new column to the current row
        }
        break;

      default: // Regular field
        if (currentColumn) {
          currentColumn.fields.unshift({
            fieldname: item.fieldname,
            fieldtype: item.fieldtype,
            label: item.label
          });
        }
        break;
    }
  }

  // After the loop, push the last row and section if they exist
  if (currentRow) {
    currentSection.rows.unshift(currentRow);
  }
  if (currentSection) {
    result.unshift(currentSection);
  }

  return result;
}

// Example flat array input
const flatArray = [
  { "fieldtype": "data", "fieldname": "tr", "label": "tr", "description": "Field" },
  { "fieldtype": "data", "fieldname": "uioer", "label": "uioer", "description": "Field" },
  { "fieldtype": "Column Break", "fieldname": "diort", "label": "diort", "description": "Column Break" },
  { "fieldtype": "data", "fieldname": "yuio", "label": "yuio", "description": "Field" },
  { "fieldtype": "Column Break", "fieldname": "test_colm2", "label": "test colm2", "description": "Column Break" },
  { "fieldtype": "Row Break", "fieldname": "1st_row", "label": "", "description": "Row Break" },
  { "fieldtype": "Section Break", "fieldname": "fdgfd", "label": "", "description": "Section Break" },
];

// Usage
// const structuredArray = rebuildToStructuredArray(flatArray);
// console.log(JSON.stringify(structuredArray, null, 2));



function convertLabelToFieldName(label) {
  return label
    .trim()                     // Remove leading/trailing spaces
    .toLowerCase()               // Convert to lowercase
    .replace(/\s+/g, '_')        // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, ''); // Remove non-alphanumeric characters except underscores
}