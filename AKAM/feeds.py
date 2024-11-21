import requests
import unittest

class TestCreateFeed(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/feeds"
        self.token = "2464|24ypTRGjtaMA0HsTmc6E0kvLikIUvCAPNLevnQ58053f0f62"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_request(self, payload):
        return requests.post(self.url, json=payload, headers=self.headers)

    def print_response(self, response):
        if response.status_code == 201:
            print("Created")
        else:
            print("ERROR:", response.status_code)
            try:
                error_message = response.json()  # Attempt to parse the JSON error message
                print("Validation Errors:", error_message)
            except ValueError:
                print("No error message found in the response")

    def test_valid_feed_creation(self):
        payload = {
            "title": "Unlock your dream home today—explore stunning properties in prime locations!",
            "content": "Invest in your future with our exclusive listings, offering unparalleled value and amenities",
            "visibility": ["OWNER"],
            "start_date": "2024-08-10",
            "end_date": "2024-10-12",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/vsd_1727014430_1727600448.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_empty_payload(self):
        payload = {}
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for empty payload

    def test_invalid_visibility(self):
        payload = {
            "title": "Unlock your dream home today—explore stunning properties in prime locations!",
            "content": "Invest in your future with our exclusive listings, offering unparalleled value and amenities",
            "visibility": ["OWNER", "GUEST"],  # Invalid visibility combination
            "start_date": "2024-08-10",
            "end_date": "2024-10-12",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/vsd_1727014430_1727600448.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity for invalid visibility

    def test_invalid_date_format(self):
        payload = {
            "title": "Unlock your dream home today—explore stunning properties in prime locations!",
            "content": "Invest in your future with our exclusive listings, offering unparalleled value and amenities",
            "visibility": ["OWNER"],
            "start_date": "2024-08-32",  # Invalid date (August has only 31 days)
            "end_date": "2024-13-10",  # Invalid date (there's no month 13)
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/vsd_1727014430_1727600448.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for invalid dates

    def test_invalid_image_url(self):
        payload = {
            "title": "Unlock your dream home today—explore stunning properties in prime locations!",
            "content": "Invest in your future with our exclusive listings, offering unparalleled value and amenities",
            "visibility": ["OWNER"],
            "start_date": "2024-08-10",
            "end_date": "2024-10-12",
            "images": [
                {"url": "invalid-url"}  # Invalid image URL
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for invalid image URL

    def test_missing_title(self):
        payload = {
            "content": "Invest in your future with our exclusive listings, offering unparalleled value and amenities",
            "visibility": ["OWNER"],
            "start_date": "2024-08-10",
            "end_date": "2024-10-12",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/vsd_1727014430_1727600448.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for missing title

    def test_missing_content(self):
        payload = {
            "title": "Unlock your dream home today—explore stunning properties in prime locations!",
            "visibility": ["OWNER"],
            "start_date": "2024-08-10",
            "end_date": "2024-10-12",
            "images": [
                {"url": "https://community-bac.boyot.app/attachments/vsd_1727014430_1727600448.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)  # Bad Request for missing content

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
