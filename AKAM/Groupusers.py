import requests
import unittest
from faker import Faker

class TestCreateFilterGroup(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/filter-group"
        self.token = "2480|0SNvMwpH7iWKInhnpaLmHxywfALTp39YZGIxZaQJ3dc55ccd"  # Make sure to update the token
        self.faker = Faker()

    def send_request(self, payload):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        return requests.post(self.url, json=payload, headers=headers)

    def print_response(self, response):
        if response.status_code == 201:
            print("Created")
        else:
            print("ERROR:", response.status_code)
            try:
                # Attempt to print the error message if available in the response
                error_message = response.json()  # Attempt to parse the JSON error message
                print("Validation Errors:", error_message)
            except ValueError:
                print("No error message found in the response")

    # Valid cases
    def test_valid_filter_group_creation_by_gender(self):
        payload = {
            "name": "group3",
            "gender": "FEMALE"
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_valid_filter_group_creation_by_customer_id(self):
        payload = {
            "name": "group2",
            "customer_id": [334, 6]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_valid_filter_group_creation_by_project_id(self):
        payload = {
            "name": "group1",
            "project_id": [212]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    # Missing required fields (negative tests)
    def test_missing_name_field(self):
        payload = {
            "gender": "MALE"  # Missing name field
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Validation error, as 'name' is required

    def test_missing_gender_field(self):
        payload = {
            "name": "group6"  # Missing gender field
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Validation error, as gender can be optional but it should be handled

    def test_missing_customer_id_and_project_id(self):
        payload = {
            "name": "group7"  # Missing customer_id and project_id
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Both fields can be optional, but validation should consider missing combinations

    def test_missing_all_optional_fields(self):
        payload = {
            "name": "group8"  # Missing all optional fields (gender, customer_id, project_id)
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # It should still work because 'name' is required and others are optional

    # Invalid data (negative tests)
    def test_invalid_gender_field(self):
        payload = {
            "name": "group4",
            "gender": "INVALID_GENDER"  # Invalid gender
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad request, assuming invalid gender is rejected

    def test_invalid_customer_id(self):
        payload = {
            "name": "group2",
            "customer_id": [9999]  # Invalid customer ID that doesn't exist
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Unprocessable entity

    def test_invalid_project_id(self):
        payload = {
            "name": "group1",
            "project_id": [9999]  # Invalid project ID
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Unprocessable entity, invalid project ID

    # Edge case scenarios
    def test_customer_id_with_no_matching_user(self):
        payload = {
            "name": "group9",
            "customer_id": [99999]  # Customer ID that does not exist in the database
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # If no users are found, the request might be rejected

    def test_project_id_with_no_matching_units(self):
        payload = {
            "name": "group10",
            "project_id": [99999]  # Project ID that does not match any units
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # If no units are found, this might return a validation error

    def test_empty_project_id_array(self):
        payload = {
            "name": "group11",
            "project_id": []  # Empty array for project_id
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # An empty array might be considered invalid depending on backend logic

    def test_empty_customer_id_array(self):
        payload = {
            "name": "group12",
            "customer_id": []  # Empty array for customer_id
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # An empty array might be considered invalid depending on backend logic


    # Test with additional unexpected fields
    def test_extra_fields_in_payload(self):
        payload = {
            "name": "group13",
            "gender": "MALE",
            "customer_id": [334],
            "extra_field": "unexpected"  # Unexpected field
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Check how the API handles unexpected fields. They might be ignored.

    # Stress test with large number of customer IDs or project IDs
    def test_large_customer_id_list(self):
        payload = {
            "name": "group14",
            "customer_id": list(range(1, 1001))  # Large number of customer IDs
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Ensure the API can handle large lists

    def test_large_project_id_list(self):
        payload = {
            "name": "group15",
            "project_id": list(range(1, 1001))  # Large number of project IDs
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Ensure the API can handle large lists

    # Test edge case where gender is missing but customer_id and project_id are provided
    def test_gender_missing_with_valid_customer_and_project_ids(self):
        payload = {
            "name": "group16",
            "customer_id": [334, 6],
            "project_id": [212]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Gender can be missing if other valid fields are provided

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
