import requests
import unittest
from faker import Faker

class TestAddBannersToPage(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/add-banners-to-page"
        self.token = "2480|0SNvMwpH7iWKInhnpaLmHxywfALTp39YZGIxZaQJ3dc55ccd"  # Replace with valid token
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

    def test_valid_banner_addition(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 3  # Assuming page 3 exists in the system
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_missing_banners(self):
        payload = {
            "page_id": 3  # Missing 'banners' field
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Or 422 based on the backend validation

    def test_missing_page_id(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Or 422 based on the backend validation

    def test_invalid_page_id(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 99999  # Invalid page_id (assuming 99999 doesn't exist)
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 404)  # Not Found if page does not exist

    def test_invalid_banner_url(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "invalid-url"  # Invalid image URL
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for invalid URL

    def test_invalid_action_or_name(self):
        payload = {
            "banners": [
                {
                    "action": "",  # Invalid empty action
                    "name": "",  # Invalid empty name
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for empty fields

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
