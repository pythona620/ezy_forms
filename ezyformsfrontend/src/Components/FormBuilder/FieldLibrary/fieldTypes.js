/**
 * Field Types Configuration
 *
 * Defines all available field types, their properties,
 * icons, and default configurations.
 */

export const FIELD_CATEGORIES = [
  {
    id: 'basic',
    name: 'Basic Fields',
    icon: 'bi bi-input-cursor-text',
    collapsed: false,
    description: 'Essential form fields for text and numbers'
  },
  {
    id: 'choice',
    name: 'Choice Fields',
    icon: 'bi bi-ui-checks',
    collapsed: false,
    description: 'Fields for selections and options'
  },
  {
    id: 'datetime',
    name: 'Date & Time',
    icon: 'bi bi-calendar3',
    collapsed: false,
    description: 'Date, time, and datetime pickers'
  },
  {
    id: 'file',
    name: 'File & Media',
    icon: 'bi bi-file-earmark-arrow-up',
    collapsed: false,
    description: 'Upload files, images, and signatures'
  },
  {
    id: 'layout',
    name: 'Layout Elements',
    icon: 'bi bi-layout-text-sidebar',
    collapsed: false,
    description: 'Structure and organize your form'
  },
  {
    id: 'advanced',
    name: 'Advanced Fields',
    icon: 'bi bi-gear',
    collapsed: true,
    description: 'Special purpose and computed fields'
  }
];

export const FIELD_TYPES = {
  // ============================================
  // BASIC FIELDS
  // ============================================
  text: {
    id: 'text',
    category: 'basic',
    name: 'Text Input',
    icon: 'bi bi-input-cursor-text',
    description: 'Single line text input',
    frappe_fieldtype: 'Data',
    defaultProps: {
      label: 'Text Field',
      placeholder: 'Enter text...',
      required: false,
      maxLength: 255,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minLength', 'maxLength', 'pattern']
    }
  },

  textarea: {
    id: 'textarea',
    category: 'basic',
    name: 'Textarea',
    icon: 'bi bi-textarea-t',
    description: 'Multi-line text input',
    frappe_fieldtype: 'Text',
    defaultProps: {
      label: 'Text Area',
      placeholder: 'Enter text...',
      rows: 4,
      required: false,
      maxLength: 5000,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minLength', 'maxLength']
    }
  },

  number: {
    id: 'number',
    category: 'basic',
    name: 'Number',
    icon: 'bi bi-hash',
    description: 'Numeric input field',
    frappe_fieldtype: 'Int',
    defaultProps: {
      label: 'Number Field',
      placeholder: '0',
      required: false,
      min: null,
      max: null,
      step: 1,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'min', 'max']
    }
  },

  email: {
    id: 'email',
    category: 'basic',
    name: 'Email',
    icon: 'bi bi-envelope',
    description: 'Email address input',
    frappe_fieldtype: 'Data',
    defaultProps: {
      label: 'Email Address',
      placeholder: 'email@example.com',
      required: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'email']
    }
  },

  phone: {
    id: 'phone',
    category: 'basic',
    name: 'Phone',
    icon: 'bi bi-telephone',
    description: 'Phone number input',
    frappe_fieldtype: 'Data',
    defaultProps: {
      label: 'Phone Number',
      placeholder: '+1 (555) 000-0000',
      required: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'phone']
    }
  },

  url: {
    id: 'url',
    category: 'basic',
    name: 'URL',
    icon: 'bi bi-link-45deg',
    description: 'Website URL input',
    frappe_fieldtype: 'Data',
    defaultProps: {
      label: 'Website URL',
      placeholder: 'https://example.com',
      required: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'url']
    }
  },

  // ============================================
  // CHOICE FIELDS
  // ============================================
  select: {
    id: 'select',
    category: 'choice',
    name: 'Select Dropdown',
    icon: 'bi bi-chevron-down',
    description: 'Single selection dropdown',
    frappe_fieldtype: 'Select',
    defaultProps: {
      label: 'Select Field',
      placeholder: 'Choose an option...',
      required: false,
      options: ['Option 1', 'Option 2', 'Option 3'],
      width: '100%'
    },
    validation: {
      supportedRules: ['required']
    }
  },

  multiselect: {
    id: 'multiselect',
    category: 'choice',
    name: 'Multi Select',
    icon: 'bi bi-ui-checks-grid',
    description: 'Multiple selection dropdown',
    frappe_fieldtype: 'MultiSelect',
    defaultProps: {
      label: 'Multi Select Field',
      placeholder: 'Choose options...',
      required: false,
      options: ['Option 1', 'Option 2', 'Option 3'],
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minItems', 'maxItems']
    }
  },

  radio: {
    id: 'radio',
    category: 'choice',
    name: 'Radio Buttons',
    icon: 'bi bi-record-circle',
    description: 'Single choice radio buttons',
    frappe_fieldtype: 'Select',
    defaultProps: {
      label: 'Radio Field',
      required: false,
      options: ['Option 1', 'Option 2', 'Option 3'],
      layout: 'vertical',
      width: '100%'
    },
    validation: {
      supportedRules: ['required']
    }
  },

  checkbox: {
    id: 'checkbox',
    category: 'choice',
    name: 'Checkboxes',
    icon: 'bi bi-check-square',
    description: 'Multiple choice checkboxes',
    frappe_fieldtype: 'MultiSelect',
    defaultProps: {
      label: 'Checkbox Field',
      required: false,
      options: ['Option 1', 'Option 2', 'Option 3'],
      layout: 'vertical',
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minItems', 'maxItems']
    }
  },

  toggle: {
    id: 'toggle',
    category: 'choice',
    name: 'Toggle Switch',
    icon: 'bi bi-toggle-on',
    description: 'On/off switch',
    frappe_fieldtype: 'Check',
    defaultProps: {
      label: 'Toggle Field',
      required: false,
      default: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required']
    }
  },

  // ============================================
  // DATE & TIME FIELDS
  // ============================================
  date: {
    id: 'date',
    category: 'datetime',
    name: 'Date Picker',
    icon: 'bi bi-calendar-date',
    description: 'Date selection',
    frappe_fieldtype: 'Date',
    defaultProps: {
      label: 'Date Field',
      placeholder: 'Select date...',
      required: false,
      format: 'YYYY-MM-DD',
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minDate', 'maxDate']
    }
  },

  time: {
    id: 'time',
    category: 'datetime',
    name: 'Time Picker',
    icon: 'bi bi-clock',
    description: 'Time selection',
    frappe_fieldtype: 'Time',
    defaultProps: {
      label: 'Time Field',
      placeholder: 'Select time...',
      required: false,
      format: 'HH:mm:ss',
      width: '100%'
    },
    validation: {
      supportedRules: ['required']
    }
  },

  datetime: {
    id: 'datetime',
    category: 'datetime',
    name: 'DateTime Picker',
    icon: 'bi bi-calendar3',
    description: 'Date and time selection',
    frappe_fieldtype: 'Datetime',
    defaultProps: {
      label: 'DateTime Field',
      placeholder: 'Select date and time...',
      required: false,
      format: 'YYYY-MM-DD HH:mm:ss',
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minDate', 'maxDate']
    }
  },

  // ============================================
  // FILE & MEDIA FIELDS
  // ============================================
  fileupload: {
    id: 'fileupload',
    category: 'file',
    name: 'File Upload',
    icon: 'bi bi-file-earmark-arrow-up',
    description: 'Upload files',
    frappe_fieldtype: 'Attach',
    defaultProps: {
      label: 'File Upload',
      required: false,
      acceptedTypes: ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'],
      maxSize: 10485760, // 10MB in bytes
      multiple: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'fileType', 'fileSize']
    }
  },

  imageupload: {
    id: 'imageupload',
    category: 'file',
    name: 'Image Upload',
    icon: 'bi bi-image',
    description: 'Upload images',
    frappe_fieldtype: 'Attach Image',
    defaultProps: {
      label: 'Image Upload',
      required: false,
      acceptedTypes: ['jpg', 'jpeg', 'png', 'gif'],
      maxSize: 5242880, // 5MB in bytes
      multiple: false,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'fileType', 'fileSize', 'imageDimensions']
    }
  },

  signature: {
    id: 'signature',
    category: 'file',
    name: 'Signature Pad',
    icon: 'bi bi-pen',
    description: 'Digital signature capture',
    frappe_fieldtype: 'Signature',
    defaultProps: {
      label: 'Signature',
      required: false,
      width: '100%',
      height: 200
    },
    validation: {
      supportedRules: ['required']
    }
  },

  // ============================================
  // LAYOUT ELEMENTS
  // ============================================
  sectionbreak: {
    id: 'sectionbreak',
    category: 'layout',
    name: 'Section Break',
    icon: 'bi bi-layout-split',
    description: 'Divide form into sections',
    frappe_fieldtype: 'Section Break',
    defaultProps: {
      label: 'Section Break',
      collapsible: false,
      collapsed: false,
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  },

  columnbreak: {
    id: 'columnbreak',
    category: 'layout',
    name: 'Column Break',
    icon: 'bi bi-layout-three-columns',
    description: 'Create columns',
    frappe_fieldtype: 'Column Break',
    defaultProps: {
      width: '50%'
    },
    validation: {
      supportedRules: []
    }
  },

  heading: {
    id: 'heading',
    category: 'layout',
    name: 'Heading',
    icon: 'bi bi-type-h1',
    description: 'Add heading text',
    frappe_fieldtype: 'HTML',
    defaultProps: {
      label: 'Heading Text',
      level: 2, // h1, h2, h3, etc.
      text: 'Heading',
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  },

  paragraph: {
    id: 'paragraph',
    category: 'layout',
    name: 'Paragraph',
    icon: 'bi bi-paragraph',
    description: 'Add description text',
    frappe_fieldtype: 'HTML',
    defaultProps: {
      label: 'Paragraph Text',
      text: 'Your text here...',
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  },

  divider: {
    id: 'divider',
    category: 'layout',
    name: 'Divider',
    icon: 'bi bi-dash-lg',
    description: 'Horizontal divider line',
    frappe_fieldtype: 'HTML',
    defaultProps: {
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  },

  // ============================================
  // ADVANCED FIELDS
  // ============================================
  table: {
    id: 'table',
    category: 'advanced',
    name: 'Table/Grid',
    icon: 'bi bi-table',
    description: 'Child table for multiple rows',
    frappe_fieldtype: 'Table',
    defaultProps: {
      label: 'Table Field',
      required: false,
      columns: [],
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minRows', 'maxRows']
    }
  },

  link: {
    id: 'link',
    category: 'advanced',
    name: 'Link Field',
    icon: 'bi bi-box-arrow-up-right',
    description: 'Link to another DocType',
    frappe_fieldtype: 'Link',
    defaultProps: {
      label: 'Link Field',
      placeholder: 'Select...',
      required: false,
      doctype: '',
      width: '100%'
    },
    validation: {
      supportedRules: ['required']
    }
  },

  dynamiclist: {
    id: 'dynamiclist',
    category: 'advanced',
    name: 'Dynamic List',
    icon: 'bi bi-list-ul',
    description: 'Repeatable list of items',
    frappe_fieldtype: 'Dynamic Link',
    defaultProps: {
      label: 'Dynamic List',
      required: false,
      minItems: 1,
      maxItems: null,
      width: '100%'
    },
    validation: {
      supportedRules: ['required', 'minItems', 'maxItems']
    }
  },

  formula: {
    id: 'formula',
    category: 'advanced',
    name: 'Formula Field',
    icon: 'bi bi-calculator',
    description: 'Calculated field',
    frappe_fieldtype: 'Data',
    defaultProps: {
      label: 'Formula Field',
      formula: '',
      readonly: true,
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  },

  qrcode: {
    id: 'qrcode',
    category: 'advanced',
    name: 'QR Code',
    icon: 'bi bi-qr-code',
    description: 'Generate QR code',
    frappe_fieldtype: 'Barcode',
    defaultProps: {
      label: 'QR Code Field',
      data: '',
      size: 200,
      width: '100%'
    },
    validation: {
      supportedRules: []
    }
  }
};

/**
 * Get all field types for a specific category
 */
export function getFieldsByCategory(categoryId) {
  return Object.values(FIELD_TYPES).filter(
    (field) => field.category === categoryId
  );
}

/**
 * Get field type configuration by ID
 */
export function getFieldType(fieldId) {
  return FIELD_TYPES[fieldId];
}

/**
 * Search field types by name or description
 */
export function searchFieldTypes(query) {
  const lowerQuery = query.toLowerCase();
  return Object.values(FIELD_TYPES).filter(
    (field) =>
      field.name.toLowerCase().includes(lowerQuery) ||
      field.description.toLowerCase().includes(lowerQuery)
  );
}
