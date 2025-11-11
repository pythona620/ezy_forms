# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EzyForms is a **Frappe-based workflow management system** with dynamic form creation, multi-level approvals, and QR code submissions. It consists of a **Python/Frappe backend** and a **Vue.js 3 frontend**.

**Key Dependencies**:
- Backend: Frappe Framework, Python 3
- Frontend: Vue 3.5.10, Vite 5.4.8, PrimeVue, Axios
- Related: Works alongside `ezy_flow` app for workflow engine

---

## Development Commands

### Backend (Frappe)

```bash
# From bench directory (parent of apps/ezy_forms)
bench --site [site-name] migrate          # Run database migrations
bench --site [site-name] clear-cache      # Clear all caches
bench restart                             # Restart Frappe server
bench console                             # Python REPL with Frappe context

# Install/update app
bench --site [site-name] install-app ezy_forms
bench --site [site-name] uninstall-app ezy_forms

# Database backup
bench --site [site-name] backup
```

### Frontend (Vue.js)

```bash
# Navigate to frontend directory
cd apps/ezy_forms/ezyformsfrontend

# Development
npm install                               # Install dependencies
npm run dev                               # Start dev server (port 8080)

# Production build
npm run build                             # Build for production
# Output: ../ezy_forms/public/ezyformsfrontend/
# Also copies index.html to ../ezy_forms/www/ezyformsfrontend.html

npm run preview                           # Preview production build
```

### Build Process Details

The frontend build command does two things:
1. `vite build --base=/assets/ezy_forms/ezyformsfrontend/` - Builds static assets
2. `yarn copy-html-entry` - Copies index.html to www directory for Frappe serving

**Critical**: Always use `npm run build` (not `vite build` alone) to ensure the HTML entry point is copied correctly.

---

## Architecture & Code Organization

### Backend Structure

```
ezy_forms/
├── ezy_forms/              # Main app module
│   ├── api/
│   │   └── v1/            # ~35 API endpoint files (whitelisted methods)
│   ├── ezy_forms/         # Core doctypes module
│   │   └── doctype/       # ~24 DocTypes (Frappe data models)
│   ├── ezy_custom_forms/  # Custom form implementations
│   ├── user_forms/        # User-defined forms
│   ├── utils/             # Utilities including security.py
│   ├── hooks.py           # Frappe app hooks configuration
│   └── www/               # Web pages (including ezyformsfrontend.html)
├── ezyformsfrontend/      # Vue.js 3 SPA
│   ├── src/
│   │   ├── Components/    # 72 reusable Vue components
│   │   ├── Pages/         # Page modules (Dashboard, Forms, Settings, etc.)
│   │   ├── shared/
│   │   │   ├── apiurls.js        # ⭐ Central API endpoint definitions
│   │   │   ├── services/
│   │   │   │   ├── interceptor.js   # Axios HTTP interceptor
│   │   │   │   └── api_req_data.js  # API request wrappers
│   │   │   └── utils/
│   │   │       └── sanitize.js      # HTML sanitization (DOMPurify)
│   │   ├── router.js      # Vue Router configuration
│   │   └── main.js        # Application entry point
│   └── vite.config.js     # Build configuration
└── public/                # Static assets (post-build)
```

### Key Backend Patterns

#### 1. Whitelisted API Endpoints

All API methods must be decorated with `@frappe.whitelist()`:

```python
@frappe.whitelist()
def my_api_function(param1, param2):
    """
    Accessible via: /api/method/ezy_forms.api.v1.module_name.my_api_function
    """
    # Always validate user authentication
    if frappe.session.user == "Guest":
        frappe.throw("Authentication required", frappe.AuthenticationError)

    # Use parameterized queries to prevent SQL injection
    query = "SELECT * FROM `tabDocType` WHERE name = %s"
    result = frappe.db.sql(query, (param1,), as_dict=True)

    return {"success": True, "data": result}
```

#### 2. Security Utilities (CRITICAL)

**Always use secure token generation**:

```python
from ezy_forms.utils.security import generate_secure_alphanumeric_token

# Generate cryptographically secure tokens (16 chars = ~95 bits entropy)
token = generate_secure_alphanumeric_token(16)

# NEVER use:
# random.choices()  ❌
# random.sample()   ❌
```

#### 3. SQL Query Safety

**Parameterized queries are mandatory**:

```python
# CORRECT ✅
query = "SELECT * FROM `tabUser` WHERE name = %s AND role = %s"
frappe.db.sql(query, (user_name, role), as_dict=True)

# WRONG ❌ - SQL Injection vulnerability
query = f"SELECT * FROM `tabUser` WHERE name = '{user_name}'"
```

#### 4. Document Events (hooks.py)

The app uses Frappe's document event hooks:

```python
doc_events = {
    "Ezy Employee": {
        "after_insert": "ezy_flow.ezy_flow.doctype.ezy_employee.ezy_employee.set_reporting_to_and_designation"
    },
    "File": {
        "after_insert": "ezy_forms.api.v1.make_private_file_to_public.make_file_public_after_insert"
    },
    "Role": {
        "before_insert": "ezy_forms.api.v1.custom_role_permission.restrict_spical_characters_in_role",
        "after_insert": "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions"
    }
}
```

#### 5. Scheduled Tasks

```python
scheduler_events = {
    "daily": [
        "ezy_forms.api.v1.daily_email_alert.send_daily_alerts"
    ],
    "cron": {
        "0 1 * * *": ["ezy_forms.ezy_forms.doctype.doctypes_database_logs.doctypes_database_logs.create_doctypes_db_log"]
    }
}
```

---

### Frontend Architecture

#### 1. API Integration Pattern

All API endpoints are centralized in `src/shared/apiurls.js`:

```javascript
export const apis = {
  login: domain + `/method/login`,
  savedata: domain + `/method/ezy_forms.api.v1.add_dynamic_doctype.add_dynamic_doctype`,
  raising_request: domain + `/method/ezy_forms.api.v1.ezy_form_rasie_request.raising_requests_to_enqueue`,
  // ... 50+ endpoints
};

// Usage in components:
import { apis } from '@/shared/apiurls';
import { api_req_data } from '@/shared/services/api_req_data';

const data = await api_req_data(apis.dashboard_counts);
```

#### 2. HTTP Interceptor (`interceptor.js`)

**Handles all API requests/responses globally**:
- Adds authentication headers
- Processes server error messages
- Shows user-friendly error notifications
- Prevents exposure of technical error details

```javascript
// Error handling is centralized here
case 403:
  showError("Access forbidden. You don't have permission to perform this action.");
case 500:
  showError("An internal error occurred. Please try again later.");
  console.error('Server Error:', error.response.data); // Debug only
```

#### 3. XSS Prevention (CRITICAL)

**Always sanitize HTML before rendering with v-html**:

```vue
<script setup>
import { sanitizeHtml } from '@/shared/utils/sanitize';
import { computed } from 'vue';

const unsafeHtml = ref('');
const safeHtml = computed(() => sanitizeHtml(unsafeHtml.value));
</script>

<template>
  <!-- CORRECT ✅ -->
  <div v-html="safeHtml"></div>

  <!-- WRONG ❌ - XSS vulnerability -->
  <div v-html="unsafeHtml"></div>
</template>
```

**Utility functions available**:
- `sanitizeHtml(html)` - Allows safe HTML tags (b, i, p, etc.)
- `sanitizeHtmlStrict(html)` - Minimal tags only
- `stripHtml(html)` - Remove all HTML

#### 4. Component Structure

**Page Modules**:
- `Dashboard/` - Analytics and charts (ECharts)
- `Forms/` - Form browsing and management
- `Formscreator/` - Dynamic form builder
- `Settings/` - System configuration
- `ToDo/` - Workflow tasks and approvals
- `Archived/` - Historical records

**Shared Components** (72 total):
- `ApproveRequest.vue` - Workflow approval interface
- `RaiseRequest.vue` - Form submission
- `FormPreview.vue` - Read-only form display
- `QrRaiseRequest.vue` - QR code form submission
- `EmailApprove.vue` - Email-based approvals
- Plus many utility components (buttons, tables, cards, etc.)

#### 5. Router Configuration

Routes are defined in `src/router.js`:

```javascript
{
  path: '/dashboard/maindash',
  component: () => import('./Pages/Dashboard/DashBoardComp.vue'),
  meta: { LoginRequire: true, title: 'Dashboard - Ezy Forms' }
}
```

**Meta fields**:
- `LoginRequire: true` - Route requires authentication
- `title` - Browser tab title

---

## Critical Security Patterns

### Backend Security Checklist

1. **Authentication Required**:
   ```python
   @frappe.whitelist()  # NOT allow_guest=True
   def sensitive_function():
       if frappe.session.user == "Guest":
           frappe.throw("Authentication required", frappe.AuthenticationError)
   ```

2. **Permission Checks**:
   ```python
   if not frappe.has_permission(doctype, "read", docname):
       frappe.throw("You don't have permission", frappe.PermissionError)
   ```

3. **SQL Injection Prevention**:
   ```python
   # Use parameterized queries ALWAYS
   query = "SELECT * FROM `tab{doctype}` WHERE name = %s"
   result = frappe.db.sql(query, (value,), as_dict=True)
   ```

4. **Secure Token Generation**:
   ```python
   from ezy_forms.utils.security import generate_secure_alphanumeric_token
   token = generate_secure_alphanumeric_token(16)  # 95 bits entropy
   ```

5. **Input Validation**:
   ```python
   import re
   if not re.match(r'^[a-zA-Z0-9_]+$', field_name):
       frappe.throw("Invalid field name")
   ```

### Frontend Security Checklist

1. **HTML Sanitization**:
   ```javascript
   import { sanitizeHtml } from '@/shared/utils/sanitize';
   const safe = computed(() => sanitizeHtml(userInput.value));
   ```

2. **No Technical Error Exposure**:
   - Error handling in `interceptor.js` shows user-friendly messages
   - Technical details logged to console only

3. **File Upload Validation**:
   - Maximum size: 10MB
   - Allowed types: PDF, images (JPG, PNG, GIF), Office docs (DOC, XLS), text files
   - NO executable files, scripts, or archives

---

## Workflow System Integration

### How ezy_forms Works with ezy_flow

1. **Dynamic Forms** - Created via `Ezy Form Definitions` DocType
2. **Workflow Roadmaps** - Defined in `ezy_flow` app (`WF Roadmap` DocType)
3. **Approval Levels** - Multi-level approval chains (`WF Level Setup`)
4. **Request Tracking** - `WF Workflow Requests` DocType
5. **Activity Logs** - `WF Activity Log` with `WF Comments` child table

### Key Workflow Functions

**Raising Requests** (`ezy_form_rasie_request.py`):
```python
def raising_requests_to_enqueue(...)
    # Creates WF Workflow Request
    # Generates secure tokens
    # Sends email notifications
    # Creates todo items for approvers
```

**Updating Workflow** (`ezy_form_update_worflow.py`):
```python
def updating_wf_workflow_requests(...)
    # Processes approvals/rejections
    # Updates workflow status
    # Moves to next level or completes
    # Sends notifications
```

**Email Approvals** (`custom_email_approval.py`):
```python
@frappe.whitelist(allow_guest=True)  # Legitimate use case
def email_approval(token, action, reason):
    # Validates token format and status
    # Logs IP address for audit
    # Processes approval via email link
```

---

## Common Development Patterns

### Adding a New API Endpoint

1. **Create Python file** in `ezy_forms/api/v1/`:
   ```python
   import frappe

   @frappe.whitelist()
   def my_new_endpoint(param1, param2):
       """API endpoint description"""
       # Authentication check
       if frappe.session.user == "Guest":
           frappe.throw("Authentication required")

       # Business logic
       result = process_data(param1, param2)

       return {"success": True, "data": result}
   ```

2. **Add to apiurls.js** (frontend):
   ```javascript
   export const apis = {
       // ... existing
       myNewEndpoint: domain + `/method/ezy_forms.api.v1.my_module.my_new_endpoint`
   };
   ```

3. **Use in Vue component**:
   ```javascript
   import { apis } from '@/shared/apiurls';
   import { api_post_data } from '@/shared/services/api_req_data';

   const response = await api_post_data(apis.myNewEndpoint, {
       param1: value1,
       param2: value2
   });
   ```

### Creating a New DocType

1. **Navigate to Desk** → DocType → New
2. **Define fields** (or programmatically via `add_dynamic_doctype.py`)
3. **Set permissions** via Role Permission Manager
4. **Add to workflow** if needed (create WF Roadmap)

### Dynamic Form Creation

Forms are created via `Ezy Form Definitions` DocType:
- Stores field definitions in JSON format
- Linked to business units
- Can have QR codes for public submissions
- Integrates with workflow system automatically

---

## Testing & Debugging

### Backend Debugging

```bash
# View logs
tail -f sites/[site-name]/logs/error.log
tail -f sites/[site-name]/logs/web.log

# Python debugger in API methods
import pdb; pdb.set_trace()

# Log errors
frappe.log_error("Error message", "Error Title")
```

### Frontend Debugging

```javascript
// Vue DevTools (browser extension recommended)

// API debugging
console.log('API Response:', response);

// Check Axios interceptor
// All requests/responses logged in Network tab
```

### Common Issues

1. **"Authentication required" errors**:
   - Ensure user is logged in
   - Check `frappe.session.user != "Guest"`

2. **SQL errors**:
   - Verify parameterized queries (use `%s`, not f-strings)
   - Check table names use `tabDocType` format

3. **Frontend build errors**:
   - Run `npm install` to ensure dependencies
   - Check `vite.config.js` for path issues
   - Ensure `npm run build` (not just `vite build`)

4. **Permission denied**:
   - Check Role Permissions for DocType
   - Verify user has required role
   - Check `has_permission()` calls in API

---

## File Upload System

**Allowed File Types** (see `ezy_file_uploads.py`):
- Images: JPG, JPEG, PNG, GIF
- Documents: PDF, DOC, DOCX, XLS, XLSX, CSV, TXT
- Videos: MP4, MOV
- OpenDocument: ODT, ODS

**Security**:
- Maximum size: 10MB
- File extension validation
- MIME type verification
- Dangerous types blocked (ZIP, SQL, P12, executables)

**Files are converted from private to public** via `make_private_file_to_public.py` hook.

---

## Email System

### Email Templates
Default templates created on install (`default_mail_templates.py`):
- Workflow notifications
- Approval requests
- Status updates

### Email Approvals
- Unique tokens generated per approval
- Token validation and expiration tracking
- IP address logging for security audit

### Scheduled Emails
Daily email alerts configured in scheduler (`daily_email_alert.py`).

---

## Build & Deployment

### Production Build Checklist

1. **Backend**:
   ```bash
   bench --site [site] migrate
   bench --site [site] clear-cache
   bench restart
   ```

2. **Frontend**:
   ```bash
   cd apps/ezy_forms/ezyformsfrontend
   npm install
   npm run build  # Outputs to ../ezy_forms/public/ezyformsfrontend/
   ```

3. **Verify**:
   - Check build succeeded (no errors)
   - Access `/ezyformsfrontend` route
   - Test login and core workflows

### Environment Configuration

**Frontend** (`.env`):
```
VITE_API_BASE_URL=production  # or empty for /api
```

**Backend**: Configured via Frappe site config.

---

## Important Notes

1. **Security is critical** - This app handles sensitive workflow approvals and data. Always:
   - Use parameterized SQL queries
   - Validate user authentication
   - Sanitize HTML output
   - Use secure token generation

2. **Dual-app architecture** - `ezy_forms` handles forms and UI, `ezy_flow` provides workflow engine. Both apps work together.

3. **Dynamic nature** - Forms and workflows are created at runtime by users, not hardcoded.

4. **Vue 3 Composition API** - Frontend uses modern Vue 3 patterns with `<script setup>`.

5. **Frappe framework conventions** - Follow Frappe naming (DocTypes use `tab` prefix in SQL, underscore naming, etc.)

6. **Real-time updates** - Socket.io integration for live notifications (`socketService.js`).

---

## Related Documentation

For comprehensive details, see project documentation:
- `SECURITY_FIXES_APPLIED.md` - All security improvements
- `FRONTEND_TESTING_REPORT.md` - Build and testing info
- `SECURITY_AND_BUG_FIXES_DEPLOYMENT_GUIDE.md` - Deployment procedures
- `QUICK_START_GUIDE.md` - Developer quick start
- `REGRESSION_TEST_RESULTS.md` - Test results

---

**Version**: 1.0
**Last Updated**: November 10, 2025
