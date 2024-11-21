import requests
import unittest
from faker import Faker

class TestCreateViolation(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/violations"
        self.token = "2464|24ypTRGjtaMA0HsTmc6E0kvLikIUvCAPNLevnQ58053f0f62"
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

    def test_valid_violation_creation(self):
        payload = {
            "unit_id": 4811,
            "customer_id": 6,
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_empty_payload(self):
        payload = {}
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Or 422 based on your API design

    def test_invalid_category_id(self):
        payload = {
            "unit_id": 4811,
            "customer_id": 6,
            "category_id": 9999,  # Invalid category ID
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Unprocessable entity if category is invalid

    def test_invalid_customer_id(self):
        payload = {
            "unit_id": 4811,
            "customer_id": 9999,  # Invalid customer ID
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)

    def test_invalid_image_url(self):
        payload = {
            "unit_id": 4811,
            "customer_id": 6,
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "invalid-url"}  # Invalid image URL
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad request if image URL is invalid

    def test_invalid_status(self):
        payload = {
            "unit_id": 4811,
            "customer_id": 6,
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "INVALID_STATUS",  # Invalid status
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_missing_customer_id(self):
        payload = {
            "unit_id": 4811,
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_missing_unit_id(self):
        payload = {
            "customer_id": 6,
            "category_id": 1,
            "type_id": 1,
            "description": "Description",
            "required_action": "TEST",
            "status": "TO-DO",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/Project_1_1725965616.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
