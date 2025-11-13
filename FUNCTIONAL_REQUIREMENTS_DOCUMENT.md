# Functional Requirements Document (FRD)
## EzyForms - Workflow Management System

**Version:** 1.0
**Date:** November 13, 2025
**Document Status:** Draft
**Prepared By:** System Analysis

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Stakeholders](#3-stakeholders)
4. [System Architecture](#4-system-architecture)
5. [Functional Requirements](#5-functional-requirements)
6. [User Roles and Permissions](#6-user-roles-and-permissions)
7. [Data Requirements](#7-data-requirements)
8. [Integration Requirements](#8-integration-requirements)
9. [Security Requirements](#9-security-requirements)
10. [Performance Requirements](#10-performance-requirements)
11. [User Interface Requirements](#11-user-interface-requirements)
12. [Business Rules](#12-business-rules)
13. [Workflow Specifications](#13-workflow-specifications)
14. [API Specifications](#14-api-specifications)
15. [Reporting Requirements](#15-reporting-requirements)
16. [Non-Functional Requirements](#16-non-functional-requirements)

---

## 1. Executive Summary

### 1.1 Purpose
EzyForms is a comprehensive workflow management system built on the Frappe framework that enables organizations to create, manage, and process dynamic forms with multi-level approval workflows. The system provides a flexible platform for digitizing business processes with built-in security, audit trails, and notification capabilities.

### 1.2 Scope
This document outlines the functional requirements for EzyForms, a dual-architecture application consisting of:
- **Backend:** Python-based Frappe framework with 35+ API endpoints
- **Frontend:** Vue.js 3 Single Page Application (SPA) with modern UI components

### 1.3 Key Features
- Dynamic form creation and management
- Multi-level approval workflows
- QR code-based form submissions
- Email-based approvals
- Real-time notifications via Socket.io
- Comprehensive reporting and analytics
- Role-based access control
- Audit trail and activity logging
- File attachment management
- Bulk data import/export

---

## 2. System Overview

### 2.1 Business Context
EzyForms addresses the need for organizations to digitize and automate their approval-based business processes. It eliminates paper-based forms and manual routing of approval requests by providing a centralized, automated workflow system.

### 2.2 System Objectives
1. Enable non-technical users to create custom forms without coding
2. Automate multi-level approval processes
3. Provide audit trails for compliance and accountability
4. Reduce processing time for approval-based workflows
5. Enable mobile access via QR codes
6. Integrate with existing email systems for seamless communication

### 2.3 System Boundaries
**In Scope:**
- Form creation and management
- Workflow configuration and execution
- User management and authentication
- Reporting and analytics
- Email notifications
- File attachments

**Out of Scope:**
- Payment processing
- Third-party CRM integration (beyond email)
- Mobile native applications (uses responsive web design)

---

## 3. Stakeholders

### 3.1 Primary Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| System Administrator | Manages system configuration, users, and business units | System stability, security, maintainability |
| Department Managers | Create forms and workflows for their departments | Ease of form creation, workflow flexibility |
| Employees | Submit form requests | Simple submission process, status visibility |
| Approvers | Review and approve/reject requests | Clear request information, quick approval process |
| Business Unit Managers | Configure business unit settings | Customization options, branding |

### 3.2 Secondary Stakeholders
- IT Support Team
- Compliance/Audit Team
- End Users (external via QR codes)

---

## 4. System Architecture

### 4.1 Technology Stack

**Backend:**
- Framework: Frappe Framework
- Language: Python 3.x
- Database: MariaDB/MySQL
- Web Server: Nginx
- Application Server: Gunicorn

**Frontend:**
- Framework: Vue.js 3.5.10
- Build Tool: Vite 5.4.8
- UI Library: PrimeVue
- HTTP Client: Axios
- State Management: Vue 3 Composition API
- Routing: Vue Router

### 4.2 Architecture Pattern
- **Backend:** MVC (Model-View-Controller) pattern via Frappe
- **Frontend:** Component-based SPA architecture
- **Communication:** RESTful API
- **Real-time:** Socket.io for live notifications

### 4.3 Directory Structure

**Backend:**
```
ezy_forms/
├── api/v1/              # API endpoints (35+ files)
├── ezy_forms/doctype/   # Data models (24+ DocTypes)
├── utils/               # Utility functions including security
├── hooks.py             # Application hooks and event handlers
└── www/                 # Web pages
```

**Frontend:**
```
ezyformsfrontend/
├── src/
│   ├── Components/      # 72+ reusable components
│   ├── Pages/           # Main page modules
│   ├── shared/
│   │   ├── apiurls.js   # Centralized API definitions
│   │   ├── services/    # HTTP interceptor, API wrappers
│   │   └── utils/       # Sanitization utilities
│   ├── router.js        # Route configuration
│   └── main.js          # Entry point
└── vite.config.js       # Build configuration
```

---

## 5. Functional Requirements

### 5.1 User Management

#### FR-UM-001: User Registration
**Priority:** High
**Description:** System shall allow administrators to register new employees.

**Acceptance Criteria:**
- User registration form captures: name, email, employee ID, department, designation, business unit
- Email validation must be performed
- Unique employee ID enforcement
- Welcome email sent upon successful registration (configurable per business unit)

**API Endpoint:** `/method/ezy_forms.api.v1.sign_up.sign_up`

#### FR-UM-002: User Authentication
**Priority:** High
**Description:** System shall authenticate users using email and password.

**Acceptance Criteria:**
- Secure password storage (hashed)
- Session management
- Failed login attempt tracking
- First-time login password change requirement
- Remember me functionality

**API Endpoint:** `/method/login`

#### FR-UM-003: First Login Management
**Priority:** Medium
**Description:** System shall detect first-time logins and require password change.

**Acceptance Criteria:**
- Automatic detection of first login
- Forced password change flow
- Password complexity requirements
- Cannot reuse old password

**API Endpoints:**
- `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.check_is_first_time_or_not`
- `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_password`

**Related DocType:** Login Check

#### FR-UM-004: Role Management
**Priority:** High
**Description:** System shall manage user roles with custom permissions.

**Acceptance Criteria:**
- Assignment of multiple roles to users
- Custom role creation
- Role-based menu visibility
- Permission inheritance

**Related DocTypes:** Role, Custom Modules Permissions, Doctype Permissions

### 5.2 Business Unit Management

#### FR-BU-001: Business Unit Configuration
**Priority:** High
**Description:** System shall support multiple business units with independent configurations.

**Acceptance Criteria:**
- Business unit creation with unique code
- Logo upload capability
- Letterhead configuration
- Email notification settings per business unit
- File attachment limits per business unit (default: 30)

**Related DocType:** Ezy Business Unit

**Fields:**
- BU Name
- BU Code (unique)
- BU Logo
- Letter Head
- Acknowledge Required (checkbox)
- Signature Required (checkbox)
- Attachment View Required (checkbox)
- Water Mark (checkbox)
- Send Form in Mail Message Body (checkbox)
- Send Form as Attachment Through Mail (checkbox)
- Send Daily Alerts (checkbox)
- Welcome Mail to Employee (checkbox)
- Allow Approver to Edit Form (checkbox)
- File Attachment Limit For Forms (integer, default: 30)

### 5.3 Department Management

#### FR-DM-001: Department Configuration
**Priority:** High
**Description:** System shall manage organizational departments.

**Acceptance Criteria:**
- Department creation and management
- Hierarchical department structure
- Department-to-business unit mapping
- Department-specific form access control

**Related DocType:** Ezy Departments

### 5.4 Dynamic Form Creation

#### FR-FC-001: Form Builder
**Priority:** High
**Description:** System shall provide a visual form builder for creating dynamic forms.

**Acceptance Criteria:**
- Drag-and-drop form builder interface
- Support for multiple field types: Text, Number, Date, Select, Multi-select, Table, File Upload, Signature, HTML, Link
- Field properties configuration: label, placeholder, required, default value, validation rules
- Form preview before publication
- Form versioning

**Related DocType:** Ezy Form Definitions

**Frontend Components:**
- `FormBuilder/` (multiple components)
- `FormPreview.vue`
- `FormFields.vue`

#### FR-FC-002: Form Definition Storage
**Priority:** High
**Description:** System shall store form definitions in JSON format.

**Acceptance Criteria:**
- Form structure stored as JSON
- Field metadata preservation
- Form schema validation
- Support for child tables (nested forms)

**Related DocType Fields:**
- form_json (Small Text)
- form_name (Data)
- form_short_name (Data, unique)
- form_category (Data)
- form_status (Select: Draft/Created)

#### FR-FC-003: Form Categories
**Priority:** Medium
**Description:** System shall categorize forms for easy discovery.

**Acceptance Criteria:**
- Category assignment to forms
- Category-based filtering
- Category management interface

**Related DocType:** Ezy Category

#### FR-FC-004: Form Access Control
**Priority:** High
**Description:** System shall control form access by department.

**Acceptance Criteria:**
- Owner department assignment
- Accessible departments configuration (comma-separated list)
- Department-based form visibility
- Business unit-based form isolation

**Related DocType Fields:**
- owner_of_the_form (Link to Ezy Departments)
- accessible_departments (Small Text)
- business_unit (Link to Ezy Business Unit)

#### FR-FC-005: Form Activation/Deactivation
**Priority:** Medium
**Description:** System shall allow forms to be enabled or disabled.

**Acceptance Criteria:**
- Enable/disable toggle
- Active checkbox
- Disabled forms hidden from users
- Activity logging for form status changes

**Related DocType Fields:**
- enable (Check, default: 1)
- active (Check, default: 0)

**Related DocType:** Ezy Dynamic Activate Log

### 5.5 Form Submission

#### FR-FS-001: Request Raising
**Priority:** High
**Description:** Users shall be able to submit form requests.

**Acceptance Criteria:**
- Form filling with validation
- Required field enforcement
- File attachment support (multiple files)
- Draft saving capability
- Submission confirmation
- Bulk submission support

**API Endpoint:** `/method/ezy_forms.api.v1.ezy_form_rasie_request.raising_requests_to_enqueue`

**Frontend Component:** `RaiseRequest.vue`

#### FR-FS-002: QR Code Submission
**Priority:** Medium
**Description:** System shall support form submission via QR code.

**Acceptance Criteria:**
- Unique QR code generation per form
- Public access via QR code (guest user)
- QR code URL generation
- Mobile-responsive form interface
- Guest submission tracking

**Related DocType Fields:**
- qr_code (Attach)
- qr_url (Small Text)
- public_form_response (Long Text)
- as_web_view (Check)

**Related DocType:** Ezyform QR Code

**API Endpoint:** `/method/ezy_forms.api.v1.ezy_web_forms.*`

**Frontend Component:** `QrRaiseRequest.vue`

#### FR-FS-003: File Attachments
**Priority:** High
**Description:** System shall support file uploads with validation.

**Acceptance Criteria:**
- Maximum file size: 10MB per file
- Allowed file types: PDF, JPG, JPEG, PNG, GIF, DOC, DOCX, XLS, XLSX, CSV, TXT, MP4, MOV, ODT, ODS
- Blocked file types: ZIP, SQL, P12, executables
- Multiple file upload support
- File preview capability
- Automatic conversion from private to public files

**API Endpoint:** `/method/ezy_forms.api.v1.ezy_file_uploads.custom_upload_file`

**Related DocType:** Ezy File Extensions

**Hook:** File after_insert event converts private files to public

#### FR-FS-004: Request on Behalf Of
**Priority:** Medium
**Description:** Authorized users shall be able to submit requests on behalf of others.

**Acceptance Criteria:**
- Be-half-of user selection
- Permission validation
- Audit trail capture of actual submitter and be-half-of user

### 5.6 Workflow Management

#### FR-WF-001: Workflow Configuration
**Priority:** High
**Description:** System shall support configurable multi-level approval workflows.

**Acceptance Criteria:**
- Workflow roadmap creation
- Multiple approval levels (unlimited)
- Role-based approver assignment
- Conditional routing based on form data
- Workflow roadmap naming convention: `{BUSINESS_UNIT}_{FORM_NAME}`

**Integration:** Managed by ezy_flow app

**Related DocTypes (from ezy_flow):**
- WF Roadmap
- WF Level Setup
- WF Role Matrix

#### FR-WF-002: Request Approval
**Priority:** High
**Description:** Approvers shall be able to approve or reject requests.

**Acceptance Criteria:**
- Approval/rejection with comments
- Reason required for rejection
- Email notification to requester
- Automatic routing to next level upon approval
- Final completion notification

**API Endpoint:** `/method/ezy_forms.api.v1.ezy_form_update_worflow.updating_wf_workflow_requests`

**Frontend Component:** `ApproveRequest.vue`

#### FR-WF-003: Email-based Approval
**Priority:** Medium
**Description:** Approvers shall be able to approve/reject via email links.

**Acceptance Criteria:**
- Unique token generation per approval request (secure alphanumeric, 16 characters)
- Email with Approve/Reject links
- Token validation and expiration
- IP address logging for security audit
- One-time token usage
- Guest access allowed for this endpoint only

**API Endpoint:** `/method/ezy_forms.ezy_forms.doctype.email_approval.custom_email_approval.email_approval`

**Related DocType:** Email Approval

**Security Feature:** Uses `generate_secure_alphanumeric_token()` from security utils

#### FR-WF-004: Form Editing During Approval
**Priority:** Medium
**Description:** Approvers shall be able to edit forms before approval (if enabled).

**Acceptance Criteria:**
- Business unit setting to enable/disable approver editing
- Edit mode in approval interface
- Change tracking for edited fields
- Audit trail of modifications

**API Endpoint:** `/method/ezy_forms.api.v1.ezy_form_update.edit_the_form_before_approve`

**Related Business Unit Field:** allow_approver_to_edit_form

#### FR-WF-005: Request Cancellation
**Priority:** Medium
**Description:** Requesters and authorized users shall be able to cancel pending requests.

**Acceptance Criteria:**
- Cancellation before first approval
- Cancellation reason required
- Notification to all pending approvers
- Status update to "Cancelled"

**API Endpoint:** `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_cancelling_request`

#### FR-WF-006: Activity Logging
**Priority:** High
**Description:** System shall maintain comprehensive activity logs for all workflow actions.

**Acceptance Criteria:**
- Log entry for each action: submit, approve, reject, cancel, edit
- Timestamp and user capture
- Comments storage
- Field-level change tracking
- IP address logging

**Related DocTypes (from ezy_flow):**
- WF Activity Log
- WF Comments (child table)

**API Endpoints:**
- `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.save_button_commite_update`
- `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.get_doc_changes`

#### FR-WF-007: Reverse Workflow
**Priority:** Low
**Description:** System shall support reverse approval workflows.

**Acceptance Criteria:**
- Reverse workflow flag on form definition
- Approval starts from highest level
- Sequential approval from top to bottom

**Related DocType Field:** workflow_check

### 5.7 Dashboard and Reporting

#### FR-DR-001: Dashboard
**Priority:** High
**Description:** System shall provide a comprehensive dashboard with key metrics.

**Acceptance Criteria:**
- Total forms count
- Pending approvals count (role-based)
- Approved requests count
- Rejected requests count
- Forms raised by user
- Department-wise statistics
- Business unit-wise statistics
- Visual charts using ECharts

**API Endpoint:** `/method/ezy_forms.api.v1.dashboard_api.dashboard_counts`

**Frontend Page:** `Dashboard/DashBoardComp.vue`

#### FR-DR-002: Form Reports
**Priority:** High
**Description:** System shall generate reports from form data.

**Acceptance Criteria:**
- Custom report field selection
- Filter by date range, status, department, business unit
- Export to Excel/CSV
- PDF generation with print format
- Landscape/Portrait orientation support

**API Endpoints:**
- `/method/ezy_forms.api.v1.generate_report.*`
- `/method/ezy_forms.api.v1.export_report.export_report_data`

**Related DocType Field:**
- report_fields (Long Text)
- is_landscape (Check)
- print_format (Data)

#### FR-DR-003: Request Listing
**Priority:** High
**Description:** System shall provide various request list views.

**Acceptance Criteria:**
- My Requests (raised by user)
- Pending Approvals (assigned to user)
- Approved by Me
- Rejected by Me
- All Requests (with permissions)
- Advanced filtering and sorting
- Pagination
- Search functionality

**API Endpoints:**
- `/method/ezy_forms.api.v1.get_doc_list.*`
- `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.approval_by_me`

**Frontend Components:** `GlobalTable.vue`, `GlobalCard.vue`

### 5.8 Notification System

#### FR-NS-001: Email Notifications
**Priority:** High
**Description:** System shall send email notifications for workflow events.

**Acceptance Criteria:**
- Notification on request submission
- Notification to next approver
- Notification on approval/rejection
- Notification to requester on status change
- Daily pending approval reminders (scheduled)
- Configurable email templates
- Business unit-specific email settings

**API Endpoint:** `/method/ezy_forms.api.v1.send_an_email.sending_mail_api`

**Scheduled Task:** Daily email alerts at configured time

**Related DocType:** Email Template

#### FR-NS-002: Email Templates
**Priority:** Medium
**Description:** System shall support customizable email templates.

**Acceptance Criteria:**
- Default templates created on installation
- Template variables for dynamic content
- HTML email support
- Template management interface
- Template preview

**Hook:** `after_install` creates default email templates

**API Module:** `default_mail_templates.py`

#### FR-NS-003: Real-time Notifications
**Priority:** Medium
**Description:** System shall provide real-time browser notifications.

**Acceptance Criteria:**
- Socket.io integration
- Toast notifications for new approvals
- Badge count updates
- Connection status indicator

**Frontend Service:** `socketService.js`

### 5.9 Settings Management

#### FR-SM-001: Global Site Settings
**Priority:** High
**Description:** System shall provide global configuration settings.

**Acceptance Criteria:**
- System-wide settings management
- Email account configuration
- Default values configuration
- Feature toggles

**Related DocType:** Global Site Settings

**Frontend Page:** `Settings/`

#### FR-SM-002: Permission Management
**Priority:** High
**Description:** System shall manage fine-grained permissions.

**Acceptance Criteria:**
- DocType-level permissions
- Role-based access control
- Custom permission rules
- Permission inheritance

**Related DocTypes:**
- Doctype Permissions
- Ezy Doctype Permissions
- Custom Modules Permissions

**API Module:** `custom_role_permission.py`

### 5.10 Data Management

#### FR-DM-001: Bulk Data Import
**Priority:** Medium
**Description:** System shall support bulk employee data import.

**Acceptance Criteria:**
- Excel/CSV file upload
- Field mapping interface
- Validation before import
- Error reporting for failed records
- Success summary

**API Endpoint:** `/method/ezy_forms.api.v1.bulk_import_data.import_bulk_data`

#### FR-DM-002: Data Export
**Priority:** Medium
**Description:** System shall support data export.

**Acceptance Criteria:**
- Export to Excel, CSV, PDF
- Filtered data export
- Bulk export of form responses
- Report export

#### FR-DM-003: Data Archival
**Priority:** Low
**Description:** System shall support archiving of old requests.

**Acceptance Criteria:**
- Manual archival
- Archived requests in separate view
- Restore from archive
- Archive based on age/status

**Frontend Page:** `Archived/`

### 5.11 Acknowledgement System

#### FR-AS-001: Form Acknowledgement
**Priority:** Medium
**Description:** System shall support form acknowledgements if enabled for business unit.

**Acceptance Criteria:**
- Acknowledgement requirement setting per business unit
- Acknowledgement capture with signature
- Timestamp and user recording
- Acknowledgement PDF generation

**Related DocType:** Acknowledgement

**Business Unit Field:** is_acknowledge

### 5.12 Database Logging

#### FR-DL-001: DocType Database Logs
**Priority:** Low
**Description:** System shall log database statistics for all doctypes.

**Acceptance Criteria:**
- Daily scheduled task to capture record counts
- Historical data retention
- Trend analysis capability

**Related DocTypes:**
- Doctypes Database Logs
- Daily Doctypes DB Logs

**Scheduled Task:** Daily at 1:00 AM

---

## 6. User Roles and Permissions

### 6.1 Role Definitions

#### R-001: System Manager
**Permissions:**
- Full system access
- User management
- Business unit configuration
- Global settings management
- DocType management
- Database operations

#### R-002: Form Creator
**Permissions:**
- Create/edit forms
- Configure workflows
- Publish forms
- Generate QR codes
- View department forms
- Manage form permissions

#### R-003: Department Manager
**Permissions:**
- Create forms for department
- View department requests
- Assign form owners
- Configure department settings
- View department reports

#### R-004: Employee
**Permissions:**
- View accessible forms
- Raise requests
- View own requests
- Upload attachments
- Cancel own pending requests
- Submit on behalf of reportees (if authorized)

#### R-005: Approver
**Permissions:**
- View assigned approvals
- Approve/reject requests
- Add comments
- Edit forms during approval (if enabled)
- View request history
- View activity log

#### R-006: Report Viewer
**Permissions:**
- View reports
- Export data
- Filter and search
- View dashboards

#### R-007: Guest (QR Code Users)
**Permissions:**
- Submit forms via QR code
- Upload attachments
- View submission confirmation
- No login required

### 6.2 Permission Matrix

| Function | System Manager | Form Creator | Dept Manager | Employee | Approver | Report Viewer | Guest |
|----------|----------------|--------------|--------------|----------|----------|---------------|-------|
| Create Forms | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Edit Forms | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Delete Forms | ✓ | ✓ | Limited | ✗ | ✗ | ✗ | ✗ |
| Raise Request | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓* |
| Approve Request | ✓ | ✗ | ✓* | ✗ | ✓ | ✗ | ✗ |
| View All Requests | ✓ | ✗ | Limited | ✗ | Limited | ✓ | ✗ |
| View Own Requests | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Generate Reports | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| User Management | ✓ | ✗ | Limited | ✗ | ✗ | ✗ | ✗ |
| System Settings | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

*Limited = Restricted to own department/business unit
*✓* = Only via QR code

---

## 7. Data Requirements

### 7.1 Core Data Models

#### 7.1.1 Ezy Form Definitions
**Purpose:** Store form structure and metadata

**Key Fields:**
- form_short_name (Primary Key, unique)
- form_name
- form_json (form structure)
- business_unit (Foreign Key)
- owner_of_the_form (Foreign Key to Ezy Departments)
- form_category
- series (auto-numbering)
- form_status (Draft/Created)
- active (boolean)
- enable (boolean)
- accessible_departments (comma-separated)
- has_workflow
- workflow_check (reverse workflow)
- qr_code (file)
- qr_url
- report_fields (JSON)
- print_format
- is_landscape (boolean)
- send_mail_for_frist_approval (boolean)
- mail_id
- as_web_view (boolean)
- public_form_response (JSON)

**Relationships:**
- Many-to-One with Ezy Business Unit
- Many-to-One with Ezy Departments
- One-to-Many with dynamically created DocTypes

#### 7.1.2 Ezy Business Unit
**Purpose:** Multi-tenant business unit configuration

**Key Fields:**
- bu_code (Primary Key, unique)
- bu_name
- bu_logo (file)
- letter_head (HTML)
- is_acknowledge (boolean)
- signature_required (boolean)
- attachment_view_required (boolean)
- water_mark (boolean)
- allow_approver_to_edit_form (boolean)
- send_form_in_email (boolean)
- welcome_mail_to_employee (boolean)
- send_form_as_a_attach_through_mail (boolean)
- send_daily_alerts (boolean)
- file_attachment_limit_for_form (integer, default: 30)

#### 7.1.3 Ezy Departments
**Purpose:** Organizational structure

**Key Fields:**
- department_name (Primary Key)
- business_unit (Foreign Key)
- parent_department (Self-referencing FK)
- department_head (Foreign Key to User)

#### 7.1.4 Ezy Employee (from ezy_flow)
**Purpose:** Extended user profile

**Key Fields:**
- name (Primary Key, linked to User)
- employee_name
- email
- designation (Foreign Key to WF Roles)
- department (Foreign Key to Ezy Departments)
- business_unit (Foreign Key to Ezy Business Unit)
- reporting_to (Foreign Key to Ezy Employee)
- employee_id (unique)
- is_active (boolean)

#### 7.1.5 WF Workflow Requests (from ezy_flow)
**Purpose:** Store workflow request instances

**Key Fields:**
- name (Primary Key, auto-generated)
- form_name (Foreign Key to Ezy Form Definitions)
- request_id (unique)
- requester (Foreign Key to User)
- current_level (integer)
- workflow_status (Pending/Approved/Rejected/Cancelled)
- creation_date
- completion_date
- form_data (JSON)
- business_unit (Foreign Key)
- property/cluster
- reason (Long Text)
- be_half_of (Foreign Key to User)
- is_bulk (boolean)

**Child Table:** WF Comments

#### 7.1.6 WF Activity Log (from ezy_flow)
**Purpose:** Audit trail of all workflow actions

**Key Fields:**
- name (Primary Key)
- workflow_request (Foreign Key)
- action (Submit/Approve/Reject/Cancel/Edit)
- performed_by (Foreign Key to User)
- timestamp
- comments
- level (integer)
- ip_address

**Child Table:** WF Comments

#### 7.1.7 Email Approval
**Purpose:** Email-based approval tracking

**Key Fields:**
- name (Primary Key)
- token (unique, secure alphanumeric)
- workflow_request (Foreign Key)
- approver (Foreign Key to User)
- status (Pending/Used/Expired)
- expiry_date
- action_taken
- ip_address_used
- action_timestamp

#### 7.1.8 Login Check
**Purpose:** First login tracking

**Key Fields:**
- name (Primary Key, linked to User)
- is_first_login (boolean)
- last_password_change
- password_change_required (boolean)

#### 7.1.9 Doctypes Database Logs
**Purpose:** Database statistics tracking

**Key Fields:**
- name (Primary Key)
- doctype_name
- record_count
- log_date
- business_unit

### 7.2 Data Relationships Diagram

```
Ezy Business Unit
    │
    ├── Ezy Departments (Many)
    │   │
    │   ├── Ezy Employee (Many)
    │   │
    │   └── Ezy Form Definitions (Many)
    │       │
    │       └── WF Workflow Requests (Many)
    │           │
    │           ├── WF Activity Log (Many)
    │           │
    │           └── Email Approval (Many)
    │
    └── Global Site Settings (One)
```

### 7.3 Data Validation Rules

#### Email Validation
- Format: RFC 5322 compliant
- Domain validation
- Unique per user

#### Password Validation
- Minimum length: 8 characters
- Must contain: uppercase, lowercase, number, special character
- Cannot be same as previous password

#### File Validation
- Maximum size: 10MB per file
- Allowed extensions: See FR-FS-003
- MIME type verification

#### Form Field Validation
- Required field enforcement
- Data type validation (number, date, email, etc.)
- Pattern matching for regex fields
- Range validation for numeric fields
- Length limits for text fields

### 7.4 Data Retention

#### Active Data
- Form definitions: Indefinite
- Active requests: Until completion
- User data: Until deactivation

#### Archived Data
- Completed requests: 7 years (configurable)
- Activity logs: 7 years (configurable)
- Email queue: 90 days
- Database logs: 2 years

#### Purge Policy
- Failed email queue: 30 days
- Temporary files: 24 hours
- Session data: 7 days

---

## 8. Integration Requirements

### 8.1 ezy_flow Integration
**Type:** Internal App Integration

**Purpose:** Workflow engine integration

**Integration Points:**
- WF Roadmap configuration
- WF Level Setup
- WF Role Matrix
- WF Workflow Requests
- WF Activity Log
- Ezy Employee management

**Data Flow:**
- ezy_forms creates form definitions
- ezy_flow manages workflow execution
- Bi-directional data sync for request status

### 8.2 Email Integration
**Type:** SMTP Integration

**Purpose:** Email notifications

**Configuration:**
- SMTP server details
- Authentication credentials
- From email address
- Email templates

**Capabilities:**
- Send approval notifications
- Send status updates
- Daily reminders
- Bulk email sending
- Email queueing

### 8.3 File Storage Integration
**Type:** Local/Cloud Storage

**Purpose:** File attachment storage

**Configuration:**
- Storage path
- Maximum file size
- Allowed file types

**Capabilities:**
- File upload
- File download
- File preview
- Public/private file management

### 8.4 Real-time Integration
**Type:** Socket.io

**Purpose:** Real-time notifications

**Events:**
- New approval assigned
- Request status changed
- Comment added
- Form updated

---

## 9. Security Requirements

### 9.1 Authentication Security

#### SR-AUTH-001: Password Security
**Requirement:** Strong password enforcement

**Implementation:**
- Bcrypt hashing
- Salt generation per user
- Minimum 8 characters
- Complexity requirements
- Password history (prevent reuse)

#### SR-AUTH-002: Session Management
**Requirement:** Secure session handling

**Implementation:**
- HTTP-only cookies
- Secure flag for HTTPS
- Session timeout: 8 hours (configurable)
- Automatic logout on inactivity
- Concurrent session limit

#### SR-AUTH-003: First Login Security
**Requirement:** Forced password change on first login

**Implementation:**
- Detection via Login Check DocType
- Redirect to password change page
- Cannot access system without password change

### 9.2 Authorization Security

#### SR-AUTHZ-001: Role-Based Access Control
**Requirement:** Granular permission control

**Implementation:**
- Role assignment per user
- Permission matrix per DocType
- Field-level permissions
- Record-level permissions (department, business unit)

#### SR-AUTHZ-002: API Endpoint Security
**Requirement:** All API endpoints must be secured

**Implementation:**
- `@frappe.whitelist()` decorator required
- Guest access explicitly allowed only where needed (email approval, QR code submission)
- Session validation on each request
- Permission checks before data access

**Security Pattern:**
```python
@frappe.whitelist()
def sensitive_function():
    if frappe.session.user == "Guest":
        frappe.throw("Authentication required", frappe.AuthenticationError)
    # Function logic
```

### 9.3 Input Validation Security

#### SR-INPUT-001: SQL Injection Prevention
**Requirement:** Parameterized queries mandatory

**Implementation:**
- Frappe ORM usage preferred
- Parameterized queries for raw SQL
- No string concatenation in queries
- Input sanitization

**Security Pattern:**
```python
# CORRECT
query = "SELECT * FROM `tabUser` WHERE name = %s"
frappe.db.sql(query, (user_name,), as_dict=True)

# INCORRECT - NEVER DO THIS
query = f"SELECT * FROM `tabUser` WHERE name = '{user_name}'"
```

**API Module:** All 35+ API endpoints follow this pattern

#### SR-INPUT-002: XSS Prevention
**Requirement:** HTML sanitization before rendering

**Implementation:**
- DOMPurify library in frontend
- Sanitization utility functions
- v-html directive usage with sanitization
- CSP headers

**Security Module:** `shared/utils/sanitize.js`

**Functions:**
- `sanitizeHtml(html)` - Allows safe HTML tags
- `sanitizeHtmlStrict(html)` - Minimal tags only
- `stripHtml(html)` - Remove all HTML

**Security Pattern:**
```vue
<script setup>
import { sanitizeHtml } from '@/shared/utils/sanitize';
const safeHtml = computed(() => sanitizeHtml(userInput.value));
</script>
<template>
  <div v-html="safeHtml"></div>
</template>
```

#### SR-INPUT-003: File Upload Security
**Requirement:** Strict file upload validation

**Implementation:**
- File extension whitelist
- MIME type verification
- File size limit: 10MB
- Dangerous file type blocking (executables, scripts, archives)
- Malware scanning (recommended)

**API Module:** `ezy_file_uploads.py`

**Blocked Extensions:**
- .exe, .bat, .cmd, .sh
- .zip, .rar, .7z
- .sql, .db
- .p12, .pfx
- .js, .vbs, .ps1

### 9.4 Cryptographic Security

#### SR-CRYPTO-001: Secure Token Generation
**Requirement:** Cryptographically secure token generation

**Implementation:**
- Python `secrets` module
- Token length: 16 characters (95 bits entropy)
- Alphanumeric character set
- Unique token per approval request

**Security Module:** `utils/security.py`

**Function:** `generate_secure_alphanumeric_token(length)`

**Usage:**
```python
from ezy_forms.utils.security import generate_secure_alphanumeric_token
token = generate_secure_alphanumeric_token(16)
```

**NEVER USE:**
- `random.choices()` ❌
- `random.sample()` ❌
- `random.randint()` ❌

### 9.5 Data Privacy

#### SR-PRIVACY-001: Personal Data Protection
**Requirement:** Protect personally identifiable information (PII)

**Implementation:**
- Encryption at rest for sensitive fields
- Encryption in transit (HTTPS)
- Access logging for PII
- Right to deletion (GDPR compliance)

#### SR-PRIVACY-002: Audit Trail
**Requirement:** Comprehensive activity logging

**Implementation:**
- User action logging (WF Activity Log)
- IP address capture
- Timestamp recording
- Immutable log entries

### 9.6 Error Handling Security

#### SR-ERROR-001: Secure Error Messages
**Requirement:** No technical details in user-facing errors

**Implementation:**
- Generic error messages to users
- Technical details logged server-side
- HTTP interceptor standardizes error messages
- Debug info only in console (development mode)

**Frontend Module:** `shared/services/interceptor.js`

**Error Handling Pattern:**
```javascript
case 403:
  showError("Access forbidden. You don't have permission.");
case 500:
  showError("An internal error occurred. Please try again.");
  console.error('Server Error:', error.response.data); // Debug only
```

### 9.7 Email Security

#### SR-EMAIL-001: Email Approval Security
**Requirement:** Secure email-based approval mechanism

**Implementation:**
- One-time use tokens
- Token expiration
- IP address logging
- Token format validation
- Approval status verification

**API Module:** `custom_email_approval.py`

**Security Measures:**
- Token: 16-character secure alphanumeric
- Expiry: Configurable (default: 7 days)
- IP logging: For audit trail
- Status check: Ensure token not already used

---

## 10. Performance Requirements

### 10.1 Response Time Requirements

| Operation | Target Response Time | Maximum Acceptable |
|-----------|---------------------|-------------------|
| User Login | < 2 seconds | 5 seconds |
| Form Load | < 1 second | 3 seconds |
| Form Submission | < 3 seconds | 10 seconds |
| Approval Action | < 2 seconds | 5 seconds |
| Report Generation | < 5 seconds | 15 seconds |
| Dashboard Load | < 2 seconds | 5 seconds |
| Search Query | < 1 second | 3 seconds |

### 10.2 Throughput Requirements

| Metric | Target | Peak Capacity |
|--------|--------|--------------|
| Concurrent Users | 100 | 500 |
| Requests per Second | 50 | 200 |
| Form Submissions/Hour | 500 | 2000 |
| Email Notifications/Hour | 1000 | 5000 |

### 10.3 Scalability Requirements

- **Horizontal Scaling:** Support for multiple application servers
- **Database Scaling:** Database replication and sharding support
- **File Storage Scaling:** Cloud storage integration capability
- **Load Balancing:** Support for load balancer configuration

### 10.4 Resource Requirements

**Server Requirements (Minimum):**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 100 GB SSD
- Network: 100 Mbps

**Server Requirements (Recommended):**
- CPU: 8 cores
- RAM: 16 GB
- Storage: 500 GB SSD
- Network: 1 Gbps

**Client Requirements:**
- Modern browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- JavaScript enabled
- Minimum 2 Mbps internet connection
- Screen resolution: 1024x768 minimum

---

## 11. User Interface Requirements

### 11.1 UI Architecture

**Framework:** Vue.js 3 with Composition API
**UI Library:** PrimeVue
**Design Pattern:** Component-based architecture
**Responsive Design:** Mobile-first approach

### 11.2 Page Modules

#### PM-001: Dashboard
**Location:** `Pages/Dashboard/DashBoardComp.vue`

**Components:**
- Summary cards (total forms, pending, approved, rejected)
- Charts (ECharts integration)
  - Requests by department
  - Requests by status
  - Requests by business unit
  - Monthly trends
- Quick actions
- Recent activity feed

#### PM-002: Forms Management
**Location:** `Pages/Forms/`

**Components:**
- Form list with filters
- Form categories
- Search and sort
- Quick actions (view, edit, delete, QR code)
- Status indicators

#### PM-003: Form Creator
**Location:** `Pages/Formscreator/`

**Components:**
- Drag-and-drop form builder
- Field palette
- Properties panel
- Preview mode
- Save/publish options
- Workflow configuration

**Sub-components:**
- `FormBuilder/DragAndDrop.vue`
- `FormBuilder/FieldPalette.vue`
- `FormBuilder/PropertiesPanel.vue`
- `FormBuilder/FormPreview.vue`

#### PM-004: Request Management
**Location:** `Pages/ToDo/`

**Components:**
- Request list (multiple views)
  - Pending approvals
  - My requests
  - Approved by me
  - Rejected by me
- Request detail view
- Approval interface
- Activity timeline
- Comments section

#### PM-005: Settings
**Location:** `Pages/Settings/`

**Components:**
- Business unit settings
- Department management
- User management
- Role management
- Email configuration
- System settings

#### PM-006: Archived
**Location:** `Pages/Archived/`

**Components:**
- Archived request list
- Filters and search
- Restore functionality
- Purge options

### 11.3 Shared Components

#### High-Priority Components

**SC-001: ApproveRequest.vue**
- Purpose: Request approval interface
- Size: 81 KB (complex component)
- Features: Form display, approve/reject buttons, comments, activity log

**SC-002: RaiseRequest.vue**
- Purpose: Form submission interface
- Size: 43 KB
- Features: Dynamic form rendering, file uploads, validation, submission

**SC-003: RequestPreview.vue**
- Purpose: Read-only request display
- Size: 151 KB (most complex component)
- Features: Full request details, activity log, print view

**SC-004: QrRaiseRequest.vue**
- Purpose: QR code form submission
- Size: 28 KB
- Features: Guest submission, simplified interface, mobile-optimized

**SC-005: GlobalTable.vue**
- Purpose: Reusable data table
- Size: 42 KB
- Features: Sorting, filtering, pagination, row actions

**SC-006: HeaderComp.vue**
- Purpose: Application header
- Size: 46 KB
- Features: Navigation, user menu, notifications, search

**SC-007: SideBar.vue**
- Purpose: Navigation sidebar
- Size: 26 KB
- Features: Menu items, role-based visibility, collapsible

#### Utility Components

- **ButtonComp.vue:** Reusable button component
- **CardComp.vue:** Card container
- **ModalComp.vue:** Modal dialog
- **InputComp.vue:** Form input wrapper
- **TabsComp.vue:** Tabbed interface
- **PaginationComp.vue:** Pagination controls
- **FormFields.vue:** Dynamic field renderer

### 11.4 UI/UX Requirements

#### UX-001: Responsiveness
- Mobile-first design
- Breakpoints: 320px, 768px, 1024px, 1440px
- Touch-friendly controls
- Adaptive layouts

#### UX-002: Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast
- ARIA labels

#### UX-003: User Feedback
- Loading indicators for async operations
- Success/error toast notifications
- Confirmation dialogs for destructive actions
- Inline validation messages
- Progress indicators for multi-step processes

#### UX-004: Navigation
- Breadcrumb navigation
- Clear menu structure
- Back button support
- Search functionality
- Keyboard shortcuts

#### UX-005: Error Handling
- Friendly error messages
- Recovery suggestions
- Contact support option
- Error boundary implementation

---

## 12. Business Rules

### 12.1 Form Management Rules

#### BR-FM-001: Form Uniqueness
- Form short name must be unique across system
- Form name can be duplicated (display name)
- Form short name used as DocType name in database

#### BR-FM-002: Form Status Workflow
- New form created in "Draft" status
- Draft forms not visible to users
- Form must be marked "Created" to become active
- "enable" checkbox must be checked for form to appear

#### BR-FM-003: Form Deletion
- Forms with existing requests cannot be deleted
- Forms can be disabled instead of deleted
- Deletion requires confirmation
- Deletion removes associated DocType (permanent)

#### BR-FM-004: Series Numbering
- Each form can have custom series prefix
- Auto-increment format: {series}-{number}
- Example: REQ-00001, REQ-00002
- Numbers never reset

### 12.2 Workflow Rules

#### BR-WF-001: Approval Level Rules
- Workflow must have at least one approval level
- Maximum approval levels: Unlimited
- Each level must have at least one approver role
- All approvers at current level must approve before moving to next level

#### BR-WF-002: Approval Routing
- Requests route to next level automatically on approval
- All approvers at a level must approve
- Any rejection sends request back to requester
- Rejected requests can be resubmitted

#### BR-WF-003: Approval Permissions
- Approvers can only approve requests assigned to their role
- Approvers cannot approve their own requests
- Approvers can delegate approvals (if enabled)
- Approvers must provide comments for rejection

#### BR-WF-004: Request Cancellation Rules
- Requests can be cancelled before first approval
- Requests cannot be cancelled after any approval
- Only requester or system admin can cancel
- Cancelled requests cannot be reopened

#### BR-WF-005: Email Approval Rules
- Email approval links valid for 7 days (default, configurable)
- One-time use tokens
- Token becomes invalid after use
- IP address logged for security

### 12.3 File Attachment Rules

#### BR-FA-001: File Size Limits
- Maximum file size per upload: 10 MB
- Maximum total attachments per form: Defined by business unit (default: 30)
- Large files rejected with error message

#### BR-FA-002: File Type Restrictions
- Only whitelisted file types allowed
- Executable files blocked
- Compressed files blocked
- Database files blocked

#### BR-FA-003: File Visibility
- Files uploaded in private mode
- Automatically converted to public after upload
- Public files accessible via URL
- File permissions inherit from parent request

### 12.4 Access Control Rules

#### BR-AC-001: Department Access
- Users can only access forms assigned to their department
- "Accessible departments" field controls multi-department access
- Form owner department always has access
- System Manager has access to all forms

#### BR-AC-002: Business Unit Isolation
- Business units are isolated by default
- Users cannot access forms from other business units
- System Manager can access all business units
- Cross-business unit forms not supported

#### BR-AC-003: Request Visibility
- Users can view their own requests
- Approvers can view requests assigned to them
- Department managers can view department requests
- System Manager can view all requests

### 12.5 Notification Rules

#### BR-NOT-001: Approval Notification
- Notification sent immediately when request reaches approver's level
- Notification sent to all approvers at current level
- Notification includes request link
- Notification includes requester details

#### BR-NOT-002: Status Change Notification
- Requester notified on approval
- Requester notified on rejection
- Requester notified on completion
- Requester notified on cancellation

#### BR-NOT-003: Daily Reminder
- Daily reminder sent for pending approvals (if enabled in BU)
- Reminder sent only on weekdays (configurable)
- Reminder includes pending request count
- Reminder includes direct approval links

### 12.6 Data Validation Rules

#### BR-DV-001: Required Fields
- Required fields must be filled before submission
- Required field validation on client and server side
- Empty submission rejected with error message

#### BR-DV-002: Data Type Validation
- Numeric fields accept only numbers
- Date fields accept valid dates only
- Email fields validated for format
- URL fields validated for format

#### BR-DV-003: Business Validation
- Custom validation rules per form
- Conditional validation based on other fields
- Cross-field validation support

---

## 13. Workflow Specifications

### 13.1 Request Submission Workflow

```
[User Selects Form]
        ↓
[Fill Form Fields]
        ↓
[Attach Files (Optional)]
        ↓
[Client-side Validation]
        ↓
[Submit Request]
        ↓
[Server-side Validation]
        ↓
[Create WF Workflow Request]
        ↓
[Generate Unique Request ID]
        ↓
[Generate Approval Tokens]
        ↓
[Determine First Level Approvers]
        ↓
[Send Email Notifications]
        ↓
[Create Todo Items for Approvers]
        ↓
[Log Activity]
        ↓
[Return Success to User]
```

**API Endpoint:** `raising_requests_to_enqueue()`

**Key Functions:**
- `get_workflow_configuration()` - Get workflow roadmap
- `get_next_level_roles()` - Determine approvers
- `validate_account_ids()` - Validate request data
- `process_individual_requests()` - Process single request
- `process_bulk_request()` - Process multiple requests

### 13.2 Approval Workflow

```
[Approver Receives Notification]
        ↓
[Approver Opens Request]
        ↓
[View Request Details]
        ↓
[Review Attachments]
        ↓
[View Activity Log]
        ↓
[Edit Form (if allowed)]
        ↓
[Decision: Approve or Reject]
        ↓
        ├─[Approve]
        │       ↓
        │   [Add Comments (Optional)]
        │       ↓
        │   [Update Request Status]
        │       ↓
        │   [Check if More Levels]
        │       ↓
        │       ├─[Yes] → [Route to Next Level]
        │       │              ↓
        │       │          [Send Notifications]
        │       │
        │       └─[No] → [Mark as Completed]
        │                     ↓
        │                 [Send Completion Notification]
        │
        └─[Reject]
                ↓
            [Enter Rejection Reason]
                ↓
            [Update Request Status]
                ↓
            [Notify Requester]
                ↓
            [Log Activity]
```

**API Endpoint:** `updating_wf_workflow_requests()`

### 13.3 Email Approval Workflow

```
[Approver Receives Email]
        ↓
[Click Approve/Reject Link]
        ↓
[Browser Opens with Token]
        ↓
[System Validates Token]
        ↓
        ├─[Valid]
        │       ↓
        │   [Check Token Status]
        │       ↓
        │       ├─[Not Used]
        │       │       ↓
        │       │   [Show Approval Form]
        │       │       ↓
        │       │   [User Confirms Action]
        │       │       ↓
        │       │   [Process Approval]
        │       │       ↓
        │       │   [Mark Token as Used]
        │       │       ↓
        │       │   [Log IP Address]
        │       │       ↓
        │       │   [Show Success Message]
        │       │
        │       └─[Already Used]
        │               ↓
        │           [Show Error: Token Already Used]
        │
        └─[Invalid]
                ↓
            [Show Error: Invalid Token]
```

**API Endpoint:** `email_approval()`

**Security Measures:**
- Token format validation (16 chars, alphanumeric)
- One-time use enforcement
- IP address logging
- Expiry check
- Status verification

### 13.4 QR Code Submission Workflow

```
[User Scans QR Code]
        ↓
[Mobile Browser Opens Form URL]
        ↓
[Guest Access Allowed]
        ↓
[Form Loads with QR Parameters]
        ↓
[User Fills Form]
        ↓
[Upload Attachments (Optional)]
        ↓
[Submit Request]
        ↓
[Create WF Workflow Request]
        ↓
[Link to QR Code Record]
        ↓
[Start Workflow]
        ↓
[Send Notifications]
        ↓
[Show Confirmation to User]
        ↓
[Store Submission in public_form_response]
```

**Key Characteristics:**
- No login required
- Limited to specific form
- Cannot view request status
- One-way submission only
- Stored separately in public_form_response field

### 13.5 Bulk Request Workflow

```
[User Selects Multiple Records]
        ↓
[Fills Single Form for All]
        ↓
[Submits Bulk Request]
        ↓
[System Creates Single WF Request]
        ↓
[Link All Records to Request]
        ↓
[Single Approval for All Records]
        ↓
[On Approval: All Records Updated]
        ↓
[Single Notification Sent]
```

**Difference from Individual:**
- One request for multiple records
- Single approval process
- Bulk status update
- Consolidated notification

---

## 14. API Specifications

### 14.1 API Architecture

**Base URL:** `/api/method/`
**Authentication:** Session-based (cookies)
**Format:** JSON
**Error Handling:** Standardized error responses

### 14.2 Core API Endpoints

#### Category: Authentication

##### POST /method/login
**Purpose:** User authentication

**Request:**
```json
{
  "usr": "user@example.com",
  "pwd": "password"
}
```

**Response (Success):**
```json
{
  "message": "Logged In",
  "home_page": "/app",
  "full_name": "John Doe"
}
```

**Response (Error):**
```json
{
  "exc": "Incorrect password"
}
```

##### POST /method/logout
**Purpose:** User logout

**Response:**
```json
{
  "message": "Logged Out"
}
```

#### Category: Form Management

##### POST /method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_dynamic_doctype
**Purpose:** Create dynamic form/DocType

**Request:**
```json
{
  "form_name": "Leave Request",
  "form_short_name": "leave_request",
  "business_unit": "HQ",
  "form_json": "[{...field definitions...}]",
  "has_workflow": "WF_LEAVE",
  "accessible_departments": "HR,Admin"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Form created successfully",
  "doctype_name": "leave_request"
}
```

##### POST /method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_child_doctype
**Purpose:** Add child table to form

**Request:**
```json
{
  "parent_doctype": "leave_request",
  "child_fields": "[{...child field definitions...}]"
}
```

##### POST /method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.deleting_customized_field_from_custom_dynamic_doc
**Purpose:** Delete form field

**Request:**
```json
{
  "doctype_name": "leave_request",
  "fieldname": "old_field"
}
```

#### Category: Request Management

##### POST /method/ezy_forms.api.v1.ezy_form_rasie_request.raising_requests_to_enqueue
**Purpose:** Submit form request

**Request:**
```json
{
  "module_name": "HR",
  "doctype_name": "leave_request",
  "ids": ["rec_001"],
  "reason": "Annual leave",
  "url_for_request_id": "/request/",
  "files": ["file1.pdf", "file2.jpg"],
  "property": "HQ",
  "ip_address": "192.168.1.1",
  "employee_id": "EMP001",
  "be_half_of": null,
  "bulk": null
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request submitted successfully",
  "request_id": "REQ-00001"
}
```

##### POST /method/ezy_forms.api.v1.ezy_form_update_worflow.updating_wf_workflow_requests
**Purpose:** Approve/reject request

**Request:**
```json
{
  "request_id": "REQ-00001",
  "action": "Approved",
  "comments": "Looks good",
  "approver": "manager@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request approved successfully",
  "next_level": 2,
  "status": "Pending"
}
```

##### POST /method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.wf_cancelling_request
**Purpose:** Cancel pending request

**Request:**
```json
{
  "request_id": "REQ-00001",
  "cancellation_reason": "No longer needed"
}
```

#### Category: Email Approval

##### GET /method/ezy_forms.ezy_forms.doctype.email_approval.custom_email_approval.email_approval
**Purpose:** Approve/reject via email link

**Authentication:** Guest allowed (token-based)

**Request:**
```json
{
  "token": "abc123xyz456",
  "action": "Approved",
  "reason": "Approved via email"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request approved successfully"
}
```

#### Category: Dashboard

##### GET /method/ezy_forms.api.v1.dashboard_api.dashboard_counts
**Purpose:** Get dashboard statistics

**Response:**
```json
{
  "total_forms": 25,
  "pending_approvals": 12,
  "approved_requests": 150,
  "rejected_requests": 8,
  "my_requests": 45,
  "department_stats": {...},
  "monthly_trends": [...]
}
```

#### Category: File Management

##### POST /method/ezy_forms.api.v1.ezy_file_uploads.custom_upload_file
**Purpose:** Upload file attachment

**Request:** multipart/form-data
```
file: [binary]
doctype: "leave_request"
docname: "REQ-00001"
```

**Response:**
```json
{
  "message": {
    "file_url": "/files/document.pdf",
    "file_name": "document.pdf"
  }
}
```

#### Category: Reports

##### POST /method/ezy_forms.api.v1.generate_report.*
**Purpose:** Generate form data report

**Request:**
```json
{
  "form_name": "leave_request",
  "filters": {
    "from_date": "2025-01-01",
    "to_date": "2025-01-31",
    "status": "Approved"
  },
  "fields": ["employee", "leave_type", "from_date", "to_date"]
}
```

**Response:**
```json
{
  "data": [...],
  "count": 45
}
```

##### POST /method/ezy_forms.api.v1.export_report.export_report_data
**Purpose:** Export report to Excel/CSV

**Request:**
```json
{
  "form_name": "leave_request",
  "filters": {...},
  "export_format": "xlsx"
}
```

**Response:** File download

#### Category: User Management

##### POST /method/ezy_forms.api.v1.sign_up.sign_up
**Purpose:** User registration

**Request:**
```json
{
  "email": "newuser@example.com",
  "full_name": "New User",
  "employee_id": "EMP999",
  "department": "IT",
  "business_unit": "HQ"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully"
}
```

##### POST /method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_password
**Purpose:** Update user password

**Request:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

#### Category: Bulk Operations

##### POST /method/ezy_forms.api.v1.bulk_import_data.import_bulk_data
**Purpose:** Bulk import employee data

**Request:** multipart/form-data
```
file: [Excel file]
import_type: "employee"
```

**Response:**
```json
{
  "success": true,
  "imported": 50,
  "failed": 2,
  "errors": [...]
}
```

### 14.3 API Error Codes

| HTTP Code | Meaning | Example |
|-----------|---------|---------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Not logged in |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

### 14.4 API Rate Limiting

- **Limit:** 100 requests per minute per user
- **Burst:** 20 requests per second
- **Headers:** X-RateLimit-Limit, X-RateLimit-Remaining

---

## 15. Reporting Requirements

### 15.1 Standard Reports

#### REP-001: My Requests Report
**Description:** List of all requests raised by the user

**Fields:**
- Request ID
- Form Name
- Submission Date
- Current Status
- Current Approver
- Last Action Date

**Filters:**
- Date range
- Status
- Form type

#### REP-002: Pending Approvals Report
**Description:** All requests pending approval by the user

**Fields:**
- Request ID
- Form Name
- Requester
- Submission Date
- Days Pending
- Priority

**Filters:**
- Date range
- Form type
- Days pending threshold

#### REP-003: Approved Requests Report
**Description:** All approved requests

**Fields:**
- Request ID
- Form Name
- Requester
- Approved By
- Approval Date
- Processing Time

**Filters:**
- Date range
- Approver
- Department
- Business unit

#### REP-004: Rejected Requests Report
**Description:** All rejected requests with reasons

**Fields:**
- Request ID
- Form Name
- Requester
- Rejected By
- Rejection Date
- Rejection Reason

**Filters:**
- Date range
- Rejector
- Department

#### REP-005: Form Usage Report
**Description:** Statistics on form usage

**Fields:**
- Form Name
- Total Submissions
- Approved Count
- Rejected Count
- Pending Count
- Average Processing Time

**Filters:**
- Date range
- Business unit
- Department

#### REP-006: User Activity Report
**Description:** User activity summary

**Fields:**
- User Name
- Requests Raised
- Requests Approved
- Requests Rejected
- Average Response Time

**Filters:**
- Date range
- Department
- Role

#### REP-007: Department Performance Report
**Description:** Department-wise workflow performance

**Fields:**
- Department
- Total Requests
- Approval Rate
- Average Processing Time
- Pending Requests

**Filters:**
- Date range
- Business unit

### 15.2 Custom Reports

**Capability:** Users can create custom reports by:
- Selecting form
- Choosing fields to display
- Applying filters
- Saving report configuration

**Storage:** Custom report configurations saved per user

### 15.3 Export Formats

- **Excel (XLSX):** All data with formatting
- **CSV:** Raw data for further processing
- **PDF:** Formatted printable report

### 15.4 Report Scheduling

- **Daily Reports:** Scheduled email delivery
- **Weekly Summaries:** Sent every Monday
- **Monthly Reports:** Sent on 1st of month

---

## 16. Non-Functional Requirements

### 16.1 Availability

**Target:** 99.5% uptime (excluding planned maintenance)

**Planned Maintenance Window:** Sundays, 2:00 AM - 4:00 AM

**Backup Strategy:**
- Daily full database backup
- Hourly incremental backups
- File storage backup daily
- 30-day backup retention

### 16.2 Disaster Recovery

**Recovery Time Objective (RTO):** 4 hours
**Recovery Point Objective (RPO):** 1 hour

**Disaster Recovery Plan:**
- Off-site backup storage
- Hot standby server (recommended)
- Documented recovery procedures
- Quarterly DR drills

### 16.3 Maintainability

**Code Standards:**
- PEP 8 for Python code
- ESLint for JavaScript code
- Vue.js style guide compliance
- Comprehensive inline documentation

**Version Control:**
- Git-based version control
- Feature branch workflow
- Code review mandatory for all changes
- Automated testing before merge

**Logging:**
- Application logs: /var/log/ezy_forms/
- Error logs: Frappe error log
- Access logs: Nginx access log
- Retention: 90 days

### 16.4 Compatibility

**Browser Support:**
- Chrome 90+ (primary)
- Firefox 88+
- Safari 14+
- Edge 90+

**Not Supported:**
- Internet Explorer (any version)
- Opera Mini
- UC Browser

**Mobile Support:**
- Responsive design for all pages
- Touch-optimized controls
- Minimum screen width: 320px

**Database Compatibility:**
- MariaDB 10.3+
- MySQL 8.0+

**Python Version:**
- Python 3.8+

**Node.js Version:**
- Node.js 16+ (for frontend build)

### 16.5 Localization

**Current Support:** English

**Future Support:**
- Multi-language UI
- Date format localization
- Currency format localization
- Time zone support

### 16.6 Compliance

**Data Protection:**
- GDPR compliance
- Data encryption at rest and in transit
- Right to access
- Right to deletion
- Data portability

**Audit Compliance:**
- SOX compliance for financial workflows
- Comprehensive audit trails
- Immutable log entries
- Retention policies

**Security Compliance:**
- OWASP Top 10 mitigation
- Regular security audits
- Penetration testing (annually)
- Vulnerability scanning

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| Business Unit | Organizational entity with independent configuration |
| DocType | Frappe framework term for data model/table |
| Dynamic Form | User-created form stored as JSON |
| Roadmap | Workflow configuration defining approval levels |
| Whitelist | Frappe decorator making API endpoint publicly accessible |
| Series | Auto-numbering prefix for requests |
| Child Table | Nested table within a form (one-to-many) |
| WF | Workflow (prefix used in ezy_flow app) |
| QR Code Submission | Guest form submission via QR code |
| Email Approval | Approval via email link with token |
| Activity Log | Audit trail of all workflow actions |

---

## Appendix B: Related Documentation

- **CLAUDE.md:** Developer guide and coding standards
- **SECURITY_FIXES_APPLIED.md:** Security improvements documentation
- **FRONTEND_TESTING_REPORT.md:** Build and testing information
- **QUICK_START_GUIDE.md:** Developer quick start
- **REGRESSION_TEST_RESULTS.md:** Test results

---

## Appendix C: API Endpoint Summary

**Total API Endpoints:** 35+

**Categories:**
- Authentication: 2 endpoints
- Form Management: 8 endpoints
- Request Management: 6 endpoints
- Approval Management: 5 endpoints
- Email Operations: 3 endpoints
- Dashboard/Reports: 4 endpoints
- File Management: 2 endpoints
- User Management: 3 endpoints
- Bulk Operations: 2 endpoints

**Complete List:** See `src/shared/apiurls.js` in frontend codebase

---

## Appendix D: DocType Summary

**Total DocTypes:** 24+

**Core DocTypes:**
- Ezy Form Definitions
- Ezy Business Unit
- Ezy Departments
- Ezy Employee (from ezy_flow)
- WF Workflow Requests (from ezy_flow)
- WF Activity Log (from ezy_flow)
- Email Approval
- Login Check

**Supporting DocTypes:**
- Ezy Category
- Ezy File Extensions
- Ezy Doctype Permissions
- Custom Modules Permissions
- Doctype Permissions
- Doctypes Database Logs
- Daily Doctypes DB Logs
- Ezyform QR Code
- Form Requests
- Global Site Settings
- Responsible Unit
- Signup Employee
- Acknowledgement
- Ezy Insights
- Ezydashboards
- Predefined Doctype

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Business Analyst | | | |
| Technical Lead | | | |
| Project Manager | | | |
| Stakeholder | | | |

---

**Document Version:** 1.0
**Last Updated:** November 13, 2025
**Next Review Date:** February 13, 2026

---

*This Functional Requirements Document is a comprehensive specification of the EzyForms workflow management system. It serves as the primary reference for development, testing, and implementation activities.*
