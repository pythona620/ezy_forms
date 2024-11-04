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
            // Add the "insert_after" key to the current field
            // console.log(" field === ", field)
            field['reqd'] = field.reqd ? 1 : 0
            const generatedFieldname = convertLabelToFieldName(field?.label);
            result.push({
              ...field,
              description: "Field",
              fieldname: generatedFieldname,
              idx: index++, // Assign index
            });

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
            // doctype: "DocField",
            // parent: section.parent,
            // insert_after: previousFieldname, // Track the break
            // "parentfield": "fields",
            // "parenttype": "DocType",
          });

          // Update previousFieldname to the column break
          previousFieldname = columnFieldname;
        });
        const rowFieldname = convertLabelToFieldName(row?.label);
        // Add "Row Break" marker after each row
        result.push({
          description: "Row Break", 
          fieldname: rowFieldname,
          fieldtype: "Column Break", 
          idx: index++
        });
        // Update previousFieldname to the row break
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
      // Update previousFieldname to the section break
      previousFieldname = sectionFieldname;
    });

    const blockFieldname = convertLabelToFieldName(block?.label || `block_${index}`);

    result.push({
      description: "Block Break", 
      fieldname: blockFieldname,
      fieldtype: "Section Break ", 
      label: block.label, 
      idx: index++
    })
    previousFieldname = blockFieldname;
  });

  return result;
}

// Usage
// const flattenedFieldsWithBreaks = extractFieldsWithBreaks(dataObj);
// console.log(flattenedFieldsWithBreaks);


export function rebuildToStructuredArray(flatArray) {
  const result = [];
  let currentBlock = null;
  let currentSection = null;
  let currentRow = null;
  let currentColumn = null;

  for (let i = flatArray.length - 1; i >= 0; i--) {
    const item = flatArray[i];

    switch (item.description) {
      case "Block Break":
        // If there's an existing block, push it to the result before starting a new one
        if (currentBlock) {
          result.unshift(currentBlock); // Add to the beginning for correct order
        }
        currentBlock = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
          sections: [] // Initialize sections for the new block
        };
        currentSection = null; // Reset currentSection for new block
        break;

      case "Section Break":
        // If there's an existing section, push it to the current block before starting a new one
        if (currentSection) {
          if (currentBlock) {
            currentBlock.sections.unshift(currentSection); // Add section to the block
          } else {
            result.unshift(currentSection); // If no block, add section to result
          }
        }
        currentSection = {
          fieldtype: item.fieldtype,
          fieldname: item.fieldname,
          label: item.label,
          parent: item.parent,
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
            label: item.fieldname,
            parent: item.parent,
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
            parent: item.parent,
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
            parent: item.parent,
            label: item.label
          });
        }
        break;
    }
  }

  // After the loop, push the last row, section, and block if they exist
  if (currentRow) {
    currentSection.rows.unshift(currentRow);
  }
  if (currentSection) {
    if (currentBlock) {
      currentBlock.sections.unshift(currentSection);
    } else {
      result.unshift(currentSection);
    }
  }
  if (currentBlock) {
    result.unshift(currentBlock);
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

    const blockFieldname = convertLabelToFieldName(block?.label || `block_${index}`);

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



function convertLabelToFieldName(label) {
  return label
    .trim()                     // Remove leading/trailing spaces
    .toLowerCase()               // Convert to lowercase
    .replace(/\s+/g, '_')        // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, ''); // Remove non-alphanumeric characters except underscores
}