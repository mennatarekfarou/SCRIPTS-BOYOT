import requests
import unittest

class TestCreateNews(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/news"
        self.token = "2480|0SNvMwpH7iWKInhnpaLmHxywfALTp39YZGIxZaQJ3dc55ccd"  # Use your actual token here
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_request(self, payload):
        return requests.post(self.url, json=payload, headers=self.headers)

    def print_response(self, response):
        if response.status_code == 201:
            print("News Created Successfully")
        else:
            print("ERROR:", response.status_code)
            try:
                # Attempt to print the error message if available in the response
                error_message = response.json()
                print("Error Message:", error_message)
            except ValueError:
                print("No error message found in the response")

    def test_valid_news_creation(self):
        payload = {
            "content": "content",
            "title": "title",
            "images": [
                {
                    "name": "",
                    "tag": "featured",
                    "url": "https://community-bac.boyot.app/attachments/A_1731316155.png"
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)  # Should return HTTP 201 if successful

    def test_missing_content(self):
        payload = {
            "title": "title",
            "images": [
                {
                    "name": "",
                    "tag": "featured",
                    "url": "https://community-bac.boyot.app/attachments/A_1731316155.png"
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Assuming missing content leads to validation error

    def test_missing_title(self):
        payload = {
            "content": "content",
            "images": [
                {
                    "name": "",
                    "tag": "featured",
                    "url": "https://community-bac.boyot.app/attachments/A_1731316155.png"
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Assuming missing title leads to validation error

    def test_missing_images(self):
        payload = {
            "content": "content",
            "title": "title"
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Assuming missing images leads to validation error

    def test_invalid_image_url(self):
        payload = {
            "content": "content",
            "title": "title",
            "images": [
                {
                    "name": "",
                    "tag": "featured",
                    "url": "invalid-url"  # Invalid image URL
                }
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad request due to invalid URL

    def test_empty_payload(self):
        payload = {}
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Or 422 based on API design

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()

