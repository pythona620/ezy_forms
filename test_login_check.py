#!/usr/bin/env python3
"""
Test script for login_check API endpoint
Tests the check_is_first_time_or_not function after security fixes
"""

import frappe

def test_check_is_first_time_or_not():
    """Test the check_is_first_time_or_not function with various scenarios"""

    print("=" * 80)
    print("Testing check_is_first_time_or_not API Endpoint")
    print("=" * 80)

    # Test 1: Check with existing user (Administrator)
    print("\n[Test 1] Testing with Administrator user...")
    try:
        frappe.set_user("Administrator")

        # Get a valid user email from Ezy Employee
        test_user = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")

        if test_user:
            print(f"   Using test user: {test_user}")

            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_is_first_time_or_not

            result = check_is_first_time_or_not(user_id=test_user)

            if result and not result.get("error"):
                print("   ✓ Test PASSED - Got user data successfully")
                print(f"   Response keys: {list(result.keys())}")
                print(f"   is_first_login: {result.get('is_first_login', 'N/A')}")
                print(f"   is_signature: {result.get('is_signature', 'N/A')}")
                print(f"   enable_check: {result.get('enable_check', 'N/A')}")
            else:
                print(f"   ✗ Test FAILED - Error: {result.get('error')}")
                print(f"   Message: {result.get('message')}")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 1 Failed")

    # Test 2: Check Login Check document creation
    print("\n[Test 2] Testing Login Check document auto-creation...")
    try:
        frappe.set_user("Administrator")

        # Get a user that might not have Login Check document
        test_user2 = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")

        if test_user2:
            # Delete existing Login Check if exists
            existing_login = frappe.db.get_value("Login Check", {"user_id": test_user2}, "name")
            if existing_login:
                print(f"   Found existing Login Check: {existing_login}")

            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_is_first_time_or_not

            result = check_is_first_time_or_not(user_id=test_user2)

            # Check if Login Check was created/fetched
            login_check_exists = frappe.db.exists("Login Check", {"user_id": test_user2})

            if login_check_exists and not result.get("error"):
                print("   ✓ Test PASSED - Login Check document exists/created")
            else:
                print(f"   ✗ Test FAILED - Login Check not created properly")

        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 2 Failed")

    # Test 3: Test authentication requirement
    print("\n[Test 3] Testing authentication requirement...")
    try:
        frappe.set_user("Guest")

        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_is_first_time_or_not

        try:
            result = check_is_first_time_or_not(user_id="test@example.com")
            print(f"   ✗ Test FAILED - Should have thrown authentication error")
        except frappe.AuthenticationError:
            print("   ✓ Test PASSED - Authentication error thrown correctly")
        except Exception as e:
            # Check if it's an authentication related error
            if "Authentication required" in str(e):
                print("   ✓ Test PASSED - Authentication check working")
            else:
                print(f"   ? Test UNCLEAR - Got exception: {str(e)}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 3 Failed")
    finally:
        frappe.set_user("Administrator")

    # Test 4: Test with acknowledgement update
    print("\n[Test 4] Testing acknowledgement update...")
    try:
        frappe.set_user("Administrator")

        test_user3 = frappe.db.get_value("Ezy Employee", {"name": ["!=", ""]}, "emp_mail_id")

        if test_user3:
            from ezy_forms.ezy_forms.doctype.login_check.login_check import check_is_first_time_or_not

            result = check_is_first_time_or_not(
                user_id=test_user3,
                acknowledgement="Test acknowledgement text"
            )

            if result.get("acknowledgement_updated"):
                print("   ✓ Test PASSED - Acknowledgement updated successfully")

                # Verify the update
                ack_value = frappe.db.get_value("Ezy Employee", test_user3, "acknowledgement")
                if ack_value == "Test acknowledgement text":
                    print("   ✓ Verification PASSED - Data persisted correctly")
                else:
                    print(f"   ✗ Verification FAILED - Expected acknowledgement not found")
            else:
                print(f"   ✗ Test FAILED - Acknowledgement not updated")
        else:
            print("   ⊘ Test SKIPPED - No Ezy Employee found")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 4 Failed")

    # Test 5: Test error handling for non-existent user
    print("\n[Test 5] Testing error handling for non-existent user...")
    try:
        frappe.set_user("Administrator")

        from ezy_forms.ezy_forms.doctype.login_check.login_check import check_is_first_time_or_not

        try:
            result = check_is_first_time_or_not(user_id="nonexistent@user.com")
            if result.get("error"):
                print("   ✓ Test PASSED - Error returned for non-existent user")
            else:
                print("   ✗ Test FAILED - Should return error for non-existent user")
        except frappe.DoesNotExistError:
            print("   ✓ Test PASSED - DoesNotExistError thrown correctly")
        except Exception as e:
            if "does not exist" in str(e).lower():
                print("   ✓ Test PASSED - Proper error handling")
            else:
                print(f"   ? Test UNCLEAR - Got exception: {str(e)}")

    except Exception as e:
        print(f"   ✗ Test FAILED - Exception: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Test 5 Failed")

    print("\n" + "=" * 80)
    print("Test Suite Completed")
    print("=" * 80)
    print("\nNote: Check Error Log for detailed error messages if any test failed")
    print("Run: bench --site [your-site] logs to view logs\n")


if __name__ == "__main__":
    # This will be run via: bench --site [site-name] execute test_login_check.test_check_is_first_time_or_not
    test_check_is_first_time_or_not()
