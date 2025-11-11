#!/usr/bin/env python3
"""
Test script for check_first_login_status API endpoint (guest-allowed)
Tests the new guest-allowed API for checking first-time login status
"""

import frappe

def test_check_first_login_guest_api():
    """Test the check_first_login_status function with various scenarios"""

    print("=" * 80)
    print("Testing check_first_login_status API Endpoint (Guest-Allowed)")
    print("=" * 80)

    # Test 1: Guest user can call the API
    print("\n[Test 1] Testing guest access...")
    try:
        frappe.set_user("Guest")

        # Get a valid user email from Ezy Employee
        frappe.set_user("Administrator")  # Temporarily switch to get test data
        test_user = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")
        frappe.set_user("Guest")  # Switch back to Guest

        if test_user:
            print(f"   Using test user: {test_user}")

            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status

            result = check_first_login_status(user_id=test_user)

            if result and result.get("success"):
                print("   ✓ Test PASSED - Guest can access API")
                print(f"   Response: {result}")
                print(f"   is_first_login: {result.get('is_first_login', 'N/A')}")
                print(f"   enable_check: {result.get('enable_check', 'N/A')}")
                print(f"   user_exists: {result.get('user_exists', 'N/A')}")
            else:
                print(f"   ✗ Test FAILED - Error: {result.get('error')}")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 1 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 2: Invalid email format
    print("\n[Test 2] Testing invalid email format validation...")
    try:
        frappe.set_user("Guest")

        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status

        result = check_first_login_status(user_id="invalid-email")

        if result.get("error") and "email format" in result.get("error", "").lower():
            print("   ✓ Test PASSED - Invalid email rejected")
            print(f"   Error message: {result.get('error')}")
        else:
            print(f"   ✗ Test FAILED - Should reject invalid email")
            print(f"   Result: {result}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 2 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 3: Non-existent user
    print("\n[Test 3] Testing non-existent user...")
    try:
        frappe.set_user("Guest")

        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status

        result = check_first_login_status(user_id="nonexistent@example.com")

        if result.get("success") and result.get("user_exists") == False:
            print("   ✓ Test PASSED - Non-existent user handled correctly")
            print(f"   Response: {result}")
        else:
            print(f"   ✗ Test FAILED - Should return user_exists=False")
            print(f"   Result: {result}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 3 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 4: Auto-creation of Login Check document
    print("\n[Test 4] Testing auto-creation of Login Check document...")
    try:
        frappe.set_user("Administrator")

        # Create a test user without Login Check document
        test_email = f"test_user_{frappe.generate_hash(length=8)}@example.com"

        # Create User
        if not frappe.db.exists("User", test_email):
            user = frappe.new_doc("User")
            user.email = test_email
            user.first_name = "Test User"
            user.enabled = 1
            user.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"   Created test user: {test_email}")

        # Check if Login Check exists (should not)
        login_check_before = frappe.db.exists("Login Check", {"user_id": test_email})
        print(f"   Login Check exists before API call: {login_check_before}")

        # Call API as Guest
        frappe.set_user("Guest")
        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status
        result = check_first_login_status(user_id=test_email)

        # Check if Login Check exists now (should exist)
        frappe.set_user("Administrator")
        login_check_after = frappe.db.exists("Login Check", {"user_id": test_email})
        print(f"   Login Check exists after API call: {login_check_after}")

        if not login_check_before and login_check_after:
            print("   ✓ Test PASSED - Login Check auto-created")
            print(f"   API Response: {result}")

            # Verify is_first_login is set to 0 (needs password change)
            login_doc = frappe.get_doc("Login Check", {"user_id": test_email})
            if login_doc.is_first_login == 0:
                print("   ✓ Verification PASSED - is_first_login set to 0 (first time)")
            else:
                print(f"   ✗ Verification FAILED - Expected is_first_login=0, got {login_doc.is_first_login}")
        else:
            print(f"   ✗ Test FAILED - Login Check not created")

        # Cleanup
        frappe.delete_doc("Login Check", {"user_id": test_email}, force=True)
        frappe.delete_doc("User", test_email, force=True)
        frappe.db.commit()
        print(f"   Cleaned up test user: {test_email}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 4 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 5: Existing user with Login Check
    print("\n[Test 5] Testing existing user with Login Check...")
    try:
        frappe.set_user("Administrator")

        # Get a user with Login Check
        test_user = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")

        if test_user:
            # Ensure Login Check exists
            if not frappe.db.exists("Login Check", {"user_id": test_user}):
                new_doc = frappe.new_doc("Login Check")
                new_doc.user_id = test_user
                new_doc.is_first_login = 1
                new_doc.insert(ignore_permissions=True)
                frappe.db.commit()

            # Get current is_first_login value
            current_value = frappe.db.get_value("Login Check", {"user_id": test_user}, "is_first_login")
            print(f"   Current is_first_login value: {current_value}")

            # Call API as Guest
            frappe.set_user("Guest")
            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status
            result = check_first_login_status(user_id=test_user)

            if result.get("success") and result.get("is_first_login") == current_value:
                print("   ✓ Test PASSED - Returns correct is_first_login value")
                print(f"   Response: {result}")
            else:
                print(f"   ✗ Test FAILED - Incorrect value returned")
                print(f"   Expected: {current_value}, Got: {result.get('is_first_login')}")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 5 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 6: Disabled user
    print("\n[Test 6] Testing disabled user...")
    try:
        frappe.set_user("Administrator")

        # Create a disabled test user
        test_email = f"disabled_user_{frappe.generate_hash(length=8)}@example.com"

        if not frappe.db.exists("User", test_email):
            user = frappe.new_doc("User")
            user.email = test_email
            user.first_name = "Disabled User"
            user.enabled = 0  # Disabled
            user.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"   Created disabled test user: {test_email}")

        # Call API as Guest
        frappe.set_user("Guest")
        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status
        result = check_first_login_status(user_id=test_email)

        if result.get("success") and result.get("enable_check") == 0:
            print("   ✓ Test PASSED - Disabled user returns enable_check=0")
            print(f"   Response: {result}")
        else:
            print(f"   ✗ Test FAILED - Should return enable_check=0")
            print(f"   Result: {result}")

        # Cleanup
        frappe.set_user("Administrator")
        frappe.delete_doc("Login Check", {"user_id": test_email}, force=True, ignore_missing=True)
        frappe.delete_doc("User", test_email, force=True)
        frappe.db.commit()
        print(f"   Cleaned up disabled test user: {test_email}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 6 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 7: Response structure validation
    print("\n[Test 7] Testing response structure...")
    try:
        frappe.set_user("Guest")

        # Get a valid user
        frappe.set_user("Administrator")
        test_user = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")
        frappe.set_user("Guest")

        if test_user:
            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status
            result = check_first_login_status(user_id=test_user)

            # Check all required fields are present
            required_fields = ["success", "user_exists", "is_first_login", "enable_check"]
            missing_fields = [field for field in required_fields if field not in result]

            if not missing_fields:
                print("   ✓ Test PASSED - All required fields present")
                print(f"   Response structure: {list(result.keys())}")

                # Verify data types
                if (isinstance(result.get("success"), bool) and
                    isinstance(result.get("user_exists"), bool) and
                    isinstance(result.get("is_first_login"), int) and
                    isinstance(result.get("enable_check"), int)):
                    print("   ✓ Data types correct")
                else:
                    print("   ✗ Data types incorrect")
            else:
                print(f"   ✗ Test FAILED - Missing fields: {missing_fields}")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 7 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 8: No sensitive data exposed
    print("\n[Test 8] Testing that no sensitive data is exposed...")
    try:
        frappe.set_user("Guest")

        # Get a valid user
        frappe.set_user("Administrator")
        test_user = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")
        frappe.set_user("Guest")

        if test_user:
            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_first_login_status
            result = check_first_login_status(user_id=test_user)

            # Check that sensitive fields are NOT present
            sensitive_fields = [
                "signature", "acknowledgement", "company_field", "business_unit",
                "enable_two_factor_auth", "minimum_password_score", "subscription_end_date",
                "login_acknowledge", "is_acknowledge"
            ]
            exposed_fields = [field for field in sensitive_fields if field in result]

            if not exposed_fields:
                print("   ✓ Test PASSED - No sensitive data exposed")
                print(f"   Only safe fields returned: {list(result.keys())}")
            else:
                print(f"   ✗ Test FAILED - Sensitive fields exposed: {exposed_fields}")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 8 Failed")
    finally:
        frappe.set_user("Administrator")

    print("\n" + "=" * 80)
    print("Test Suite Completed")
    print("=" * 80)
    print("\nNote: Check Error Log for detailed error messages if any test failed")
    print("Run: bench --site [your-site] logs to view logs\n")


if __name__ == "__main__":
    # This will be run via: bench --site [site-name] execute ezy_forms.test_first_login_guest_api.test_check_first_login_guest_api
    test_check_first_login_guest_api()
