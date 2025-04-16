import requests
import unittest
from faker import Faker

class TestAddBannersToPage(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/add-banners-to-page"
        self.token = "2851|4RwXPMypasIqU0H5ICuzqIQY4hwhspZZCxbWJB7qb2c8e2af"  
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
                error_message = response.json()
                print("Validation Errors:", error_message)
            except ValueError:
                print("No error message found in the response")

    def test_valid_banner_addition(self):
        payload = {
            "banners": [
                {
                    "action": "TEST1",
                    "name": "TEST1",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_missing_banners(self):
        payload = {
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

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
        self.assertEqual(response.status_code, 400)

    def test_invalid_page_id(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 99999
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 404)

    def test_invalid_banner_url(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "invalid-url"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_action_or_name(self):
        payload = {
            "banners": [
                {
                    "action": "",
                    "name": "",
                    "url": "https://community-bac.boyot.app/attachments/A_1731322244.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_multiple_banners_addition(self):
        payload = {
            "banners": [
                {
                    "action": "TEST1",
                    "name": "Banner 1",
                    "url": "https://example.com/banner1.png"
                },
                {
                    "action": "TEST2",
                    "name": "Banner 2",
                    "url": "https://example.com/banner2.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_invalid_json_format(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.url, data="invalid json", headers=headers)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_large_payload(self):
        banners = [{
            "action": f"TEST{i}",
            "name": f"Banner {i}",
            "url": "https://example.com/banner.png"
        } for i in range(1, 101)]
        
        payload = {
            "banners": banners,
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_duplicate_banners(self):
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://example.com/banner.png"
                },
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://example.com/banner.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_special_characters_in_fields(self):
        payload = {
            "banners": [
                {
                    "action": "!@#$%^&*()_+",
                    "name": "<Script>alert('test')</Script>",
                    "url": "https://example.com/banner.png"
                }
            ],
            "page_id": 3
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_rate_limiting(self):
        for _ in range(10):
            payload = {
                "banners": [
                    {
                        "action": "TEST",
                        "name": "TEST",
                        "url": "https://example.com/banner.png"
                    }
                ],
                "page_id": 3
            }
            response = self.send_request(payload)
            if response.status_code == 429:
                break
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_expired_token(self):
        expired_token = "expired_token_example"
        payload = {
            "banners": [
                {
                    "action": "TEST",
                    "name": "TEST",
                    "url": "https://example.com/banner.png"
                }
            ],
            "page_id": 3
        }
        headers = {
            "Authorization": f"Bearer {expired_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.url, json=payload, headers=headers)
        self.print_response(response)
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
