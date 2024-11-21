import unittest
import requests  # Assuming you are using requests for making the API calls.

class ShopAPITests(unittest.TestCase):

    BASE_URL = "https://community-bac.boyot.app/api/company/shop"
    TOKEN = "2480|0SNvMwpH7iWKInhnpaLmHxywfALTp39YZGIxZaQJ3dc55ccd"  # Your token here

    def send_request(self, payload):
        # Add the Authorization header with the Bearer token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.TOKEN}'  # Include the token
        }
        response = requests.post(self.BASE_URL, json=payload, headers=headers)
        return response

    def print_response(self, response):
        print(response.status_code)
        

    def test_missing_name(self):
        payload = {
            "category_id": 1,
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/boyot-en-ar_(1)_1731852478.png"}
            ],
            "working_hours": {
                "Saturday": "10:00 AM - 9:00 PM"
            },
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "instagram",
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Missing name, expect 400

    def test_valid_shop_creation(self):
        payload = {
            "category_id": 1,
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/boyot-en-ar_(1)_1731852478.png"}
            ],
            "name": "ttt",
            "working_hours": {
                "Saturday": "10:00 AM - 9:00 PM"
            },
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "instagram",
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Expect 201 for successful creation
        self.assertIn('data', response.json())  # Check if response contains the shop data
        self.assertEqual(response.json()['data']['name'], "ttt")  # Verify the shop name

    def test_missing_category_id(self):
        payload = {
            "name": "Shop Name",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/boyot-en-ar_(1)_1731852478.png"}
            ],
            "working_hours": {
                "Saturday": "10:00 AM - 9:00 PM"
            },
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "instagram",
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Missing category_id, expect 400

    def test_invalid_image_url(self):
        payload = {
            "category_id": 1,
            "name": "Shop Name",
            "images": [
                {"url": "invalid_url"}  # Invalid URL
            ],
            "working_hours": {
                "Saturday": "10:00 AM - 9:00 PM"
            },
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "instagram",
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Invalid image URL, expect 400

    def test_missing_working_hours(self):
        payload = {
            "category_id": 1,
            "name": "Shop Name",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/boyot-en-ar_(1)_1731852478.png"}
            ],
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "instagram",
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Assuming working_hours is optional, expect 201

    def test_invalid_social_media_platform(self):
        payload = {
            "category_id": 1,
            "name": "Shop Name",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/boyot-en-ar_(1)_1731852478.png"}
            ],
            "working_hours": {
                "Saturday": "10:00 AM - 9:00 PM"
            },
            "social_media": [
                {
                    "url": "https://www.instagram.com/",
                    "platform": "unknown_platform",  # Invalid platform
                    "logo": []
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Invalid platform, expect 400

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
