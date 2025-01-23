import { doctypes } from "../apiurls";

export function extractFieldsWithBreaks(data) {
  const result = [];
  let previousFieldname = null; // Track the previous fieldname
  let index = 0;


  data.forEach((block) => {
    block.sections.forEach((section) => {

      section.rows.forEach((row) => {
        row.columns.forEach((column) => {

          column.fields.forEach((field) => {
            const generatedFieldname = convertLabelToFieldName(field?.label);

            // Add the field to the result if it's not already added
            let existingField = result.find(f => f.fieldname === generatedFieldname);

            if (!existingField) {
              // If the field doesn't exist, add it to the result
              existingField = {
                description: "Field",
                fieldname: generatedFieldname,
                fieldtype: field.fieldtype,
                idx: index++, // Assign index
                label: field.label,
                reqd: field.reqd ? 1 : 0,
                value: field.value ? field.value : ""
              };
              result.push(existingField);
            }

            // Add options if the field is of type "Select" or "Check"
            if (field.fieldtype === "Select") {
              existingField.options = field.options; // Add options to the existing field
            }

            // Update previousFieldname for the next field in this column
            previousFieldname = generatedFieldname;
          });

          const columnFieldname = convertLabelToFieldName(column?.label);

          // Add "Column Break" marker after each column
          result.push({
            description: "Column Break",
            fieldname: columnFieldname,
            fieldtype: "Column Break",
            idx: index++, // Assign index
            label: column.label,
          });

          previousFieldname = columnFieldname;
        });

        const rowFieldname = convertLabelToFieldName(row?.label);

        // Add "Row Break" marker after each row
        result.push({
          description: "Row Break",
          fieldname: rowFieldname,
          fieldtype: "Column Break",
          idx: index++,
          label: rowFieldname
        });

        previousFieldname = rowFieldname;
      });

      const sectionFieldname = convertLabelToFieldName(section?.label);

      // Add "Section Break" marker after each section
      result.push({
        description: "Section Break",
        fieldname: sectionFieldname,
        fieldtype: "Section Break",
        label: section.label,
        idx: index++
      });

      previousFieldname = sectionFieldname;
    });

    const blockFieldname = convertLabelToFieldName(block?.label);

    result.push({
      description: "Block Break",
      fieldname: blockFieldname,
      fieldtype: "Section Break",
      label: block.label,
      idx: index++
    });

    previousFieldname = blockFieldname;
  });

  return result;


  return result;
}

// Usage
// const flattenedFieldsWithBreaks = extractFieldsWithBreaks(dataObj);
// console.log(flattenedFieldsWithBreaks);


export function rebuildToStructuredArray(flatArray) {
  console.log(" Flat Array === ", flatArray)
  const result = [];
  let currentBlock = null;
  let currentSection = null;
  let currentRow = null;
  let currentColumn = null;

  for (let i = flatArray.length - 1; i >= 0; i--) {
    const item = flatArray[i];

    switch (item.description) {
      case "Block Break":
        // Push current section, row, and block if they exist
        if (currentRow) {
          currentSection.rows.unshift(currentRow);
          currentRow = null;
        }
        if (currentSection) {
          currentBlock.sections.unshift(currentSection);
          currentSection = null;
        }
        if (currentBlock) {
          result.unshift(currentBlock);
        }
        currentBlock = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
          sections: []
        };
        break;

      case "Section Break":
        // Push current row and section if they exist
        if (currentRow) {
          currentSection.rows.unshift(currentRow);
          currentRow = null;
        }
        if (currentSection) {
          currentBlock.sections.unshift(currentSection);
        }
        currentSection = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
          rows: []
        };
        break;

      case "Row Break":
        // Push current row if it exists
        if (currentRow) {
          currentSection.rows.unshift(currentRow);
        }
        currentRow = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
          columns: []
        };
        break;

      case "Column Break":
        // Add the column to the current row
        currentColumn = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
          fields: []
        };
        currentRow.columns.unshift(currentColumn);
        break;

      default: // Regular field
        // Add field to the current column
        if (currentColumn) {
          currentColumn.fields.unshift({
            fieldname: item.fieldname,
            fieldtype: item.fieldtype,
            parent: item.parent,
            label: item.label,
            reqd: item.reqd,
            options: item.options
          });
        }
        break;
    }
  }

  // Push the last row, section, and block (if any exist)
  if (currentRow) {
    currentSection.rows.unshift(currentRow);
  }
  if (currentSection) {
    currentBlock.sections.unshift(currentSection);
  }
  if (currentBlock) {
    result.unshift(currentBlock);
  }

  return result;
}


// Example flat array input
const flatArray = [
  {
    "description": "Field",
    "fieldname": "piufvhd",
    "fieldtype": "Data",
    "idx": 0,
    "label": "piufvhd",
    "reqd": 0
  },
  {
    "description": "Field",
    "fieldname": "gfgf",
    "fieldtype": "Data",
    "idx": 1,
    "label": "gfgf",
    "reqd": 0
  },
  {
    "description": "Column Break",
    "fieldname": "",
    "fieldtype": "Column Break",
    "idx": 2,
    "label": "",
    "doctype": "DocField"
  },
  {
    "description": "Row Break",
    "fieldname": "row_0_0",
    "fieldtype": "Row Break",  // Corrected to "Row Break"
    "idx": 3,
    "label": "row_0_0"
  },
  {
    "description": "Section Break",
    "fieldname": "",
    "fieldtype": "Section Break",
    "label": "",
    "idx": 4,
    "doctype": "DocField"
  },
  {
    "description": "Block Break",
    "fieldname": "block1",
    "fieldtype": "Block Break",  // Corrected to "Block Break"
    "label": "block-1",
    "idx": 5
  },
  {
    "description": "Field",
    "fieldname": "fdgdfhdf",
    "fieldtype": "Data",
    "idx": 6,
    "label": "fdgdfhdf",
    "reqd": 0,
    "doctype": "DocField"
  },
  {
    "description": "Column Break",
    "fieldname": "fdgdfh",
    "fieldtype": "Column Break",
    "idx": 7,
    "label": "fdgdfh",
    "doctype": "DocField"
  },
  {
    "description": "Row Break",
    "fieldname": "row_0_0_1",
    "fieldtype": "Row Break",  // Corrected to "Row Break"
    "idx": 8,
    "label": "row_0_0_1",
    "doctype": "DocField"
  },
  {
    "description": "Section Break",
    "fieldname": "dfsdgksfg",
    "fieldtype": "Section Break",
    "label": "dfsdgksfg",
    "idx": 9,
    "doctype": "DocField"
  },
  {
    "description": "Block Break",
    "fieldname": "block2",
    "fieldtype": "Block Break",  // Corrected to "Block Break"
    "label": "block-2",
    "idx": 10,
    "doctype": "DocField"
  }
];

// Usage
// const structuredArray = rebuildToStructuredArray(flatArray);
// console.log(" field format === ", structuredArray);


// deleted sec, rows,columns, fields
export function deletedFieldsExtraction(data) {
  const result = [];
  let previousFieldname = null; // Track the previous fieldname
  let index = 0;


  data.forEach((block) => {
    block.sections.forEach((section) => {
      section.rows.forEach((row) => {
        row.columns.forEach((column) => {

          column.fields.forEach((field) => {
            // Add the "insert_after" key to the current field
            console.log(" field === ", field)
            result.push({
              ...field,
              doctype: "DocField",
              parent: section.parent,
              description: "Field",
              fieldname: generatedFieldname,
              // insert_after: previousFieldname,
              idx: index++, // Assign index
              "parentfield": "fields",
              "parenttype": "DocType",
            });

            // Update previousFieldname for the next field in this column
            previousFieldname = generatedFieldname;
          });
          const columnFieldname = convertLabelToFieldName(column?.label);

          // Add "Column Break" marker after each column
          result.push({
            fieldtype: "Column Break",
            doctype: "DocField",
            parent: section.parent,
            fieldname: columnFieldname,
            label: column.label,
            description: "Column Break",
            // insert_after: previousFieldname, // Track the break
            idx: index++, // Assign index
            "parentfield": "fields",
            "parenttype": "DocType",
          });

          // Update previousFieldname to the column break
          previousFieldname = columnFieldname;
        });
        const rowFieldname = convertLabelToFieldName(row?.label);
        // Add "Row Break" marker after each row
        result.push({
          fieldtype: "Column Break", description: "Row Break", doctype: "DocField", fieldname: rowFieldname, parent: section.parent,
          // insert_after: previousFieldname, 
          idx: index++, "parentfield": "fields",
          "parenttype": "DocType",
        });
        // Update previousFieldname to the row break
        previousFieldname = rowFieldname;
      });
      const sectionFieldname = convertLabelToFieldName(section?.label);
      // Add "Section Break" marker after each section
      result.push({
        fieldtype: "Section Break", description: "Section Break", doctype: "DocField", label: section.label, parent: section.parent, fieldname: sectionFieldname,
        // insert_after: previousFieldname, 
        idx: index++, "parentfield": "fields",
        "parenttype": "DocType",
      });
      // Update previousFieldname to the section break
      previousFieldname = sectionFieldname;
    });

    const blockFieldname = convertLabelToFieldName(block?.label);

    result.push({
      fieldtype: "Section Break", description: "Block Break", doctype: "DocField", label: block.label, parent: block.parent, fieldname: blockFieldname,
      idx: index++
    })
    previousFieldname = blockFieldname;

  });

  return result;
}



export function extractFieldnames(obj) {
  let fieldnames = [];
  if (obj.fieldname) fieldnames.push(obj.fieldname);
  if (obj.sections) obj.sections.forEach(section => fieldnames.push(...extractFieldnames(section)));
  if (obj.rows) obj.rows.forEach(row => fieldnames.push(...extractFieldnames(row)));
  if (obj.columns) obj.columns.forEach(column => fieldnames.push(...extractFieldnames(column)));
  if (obj.fields) obj.fields.forEach(field => fieldnames.push(...extractFieldnames(field)));
  return fieldnames;
}

export function extractfieldlabels(obj) {
  let fieldlabels = [];
  if (obj.label) fieldlabels.push(obj.label);
  if (obj.sections) obj.sections.forEach(section => fieldlabels.push(...extractfieldlabels(section)));
  if (obj.rows) obj.rows.forEach(row => fieldlabels.push(...extractfieldlabels(row)));
  if (obj.columns) obj.columns.forEach(column => fieldlabels.push(...extractfieldlabels(column)));
  if (obj.fields) obj.fields.forEach(field => fieldlabels.push(...extractfieldlabels(field)));
  return fieldlabels;
}

export function validateFields(flatArray) {
  console.log(" flat Array == ", flatArray)
  const invalidFields = [];
  flatArray.forEach((item, index) => {
    // Check if label exists but fieldtype is missing or invalid
    if (item.label && (!item.fieldtype || item.fieldtype.trim() === "")) {
      invalidFields.push({
        index: index,
        label: item.label,
        message: `Field "${item.label}" at index ${index} has no valid fieldtype. Please select a fieldtype.`
      });
    }
  });

  return invalidFields;
}


export function addErrorMessagesToStructuredArray(structuredArray) {
  structuredArray.forEach((block, blockIndex) => {
    // Traverse sections in each block
    block.sections.forEach((section, sectionIndex) => {
      // Traverse rows in each section
      section.rows.forEach((row, rowIndex) => {
        // Traverse columns in each row
        row.columns.forEach((column, columnIndex) => {
          // Traverse fields in each column
          column.fields.forEach((field, fieldIndex) => {


            // if (!field.fieldtype || field.fieldtype.trim() === "") {
            //   // Add an error message for missing fieldtype
            //   field.error = `Field "${field.label}" has no valid fieldtype. Please select a fieldtype.`;
            // } else {
            //   // Clear the error if fieldtype is valid
            //   field.error = "";
            // }
            let errors = [];

            // Check for empty Field label
            if (!field.label || field.label.trim() === "") {
              errors.push("Field label is required.");
            }

            // Check for empty field type
            if (!field.fieldtype || field.fieldtype.trim() === "") {
              errors.push(`Field "${field.label || 'unnamed'}" has no valid fieldtype. Please select a fieldtype.`);
            }

            // Combine errors into a single error property
            field.error = errors.length ? errors.join(" ") : "";

          });
        });
      });
    });
  });
  return structuredArray;
}
// export function addErrorMessagesToStructuredArray(structuredArray) {
//   structuredArray.forEach((block) => {
//     // Traverse sections in each block
//     block.sections.forEach((section) => {
//       // Traverse rows in each section
//       section.rows.forEach((row) => {
//         // Traverse columns in each row
//         row.columns.forEach((column) => {
//           // Traverse fields in each column
//           column.fields.forEach((field) => {
//             // Check for empty Field label
//             if (!field.label) {
//               field.errorMessage = 'Field label is required.';
//             } else {
//               field.errorMessage = '';
//             }

//             // Check for missing or empty Field Type
//             if (!field.fieldtype || field.fieldtype.trim() === '') {
//               field.errorTypeMessage = `Field "${field.label}" has no valid fieldtype. Please select a fieldtype.`;
//             } else {
//               field.errorTypeMessage = ''; // Clear error if fieldtype is valid
//             }
//           });
//         });
//       });
//     });
//   });

//   return structuredArray;
// }


// Example structured array usage
// const updatedArray = addErrorMessagesToStructuredArray(structuredArray);
// console.log(JSON.stringify(updatedArray, null, 2));



function convertLabelToFieldName(label) {
  return label
    .trim()                     // Remove leading/trailing spaces
    .toLowerCase()               // Convert to lowercase
    .replace(/\s+/g, '_')        // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, ''); // Remove non-alphanumeric characters except underscores
}