import requests
import unittest
from faker import Faker

class TestCreateProject(unittest.TestCase):
    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/projects"
        self.token = "2480|0SNvMwpH7iWKInhnpaLmHxywfALTp39YZGIxZaQJ3dc55ccd"
        self.faker = Faker()

    def send_request(self, payload):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        return requests.post(self.url, json=payload, headers=headers)

    def print_response(self, response):
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.content) 
        if response.status_code == 201:
            print("Project created")
        else:
            print("ERROR:", response.status_code)
            try:
                error_message = response.json()
                print("Validation Errors:", error_message)
            except ValueError:
                print("No error message found in the response")

    def test_valid_project_creation(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 200)  # Adjusted to 200 based on your findings

    def test_empty_payload(self):
        payload = {}
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_status(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "INVALID_STATUS",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_missing_name(self):
        payload = {
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_latitude(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 100.0,  # Invalid latitude
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_longitude(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 200.0,  # Invalid longitude
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_exceeding_description_length(self):
        payload = {
            "name": "scerio",
            "description": "x" * 1001,  # Assuming the max length is 1000
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_area_type(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": 12345,  # Should be a string
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_invalid_number_of_units(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "three hundred",  # Should be a number
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_missing_latitude_and_longitude(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [],
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def test_exceeding_banners_length(self):
        payload = {
            "name": "scerio",
            "description": "Valid description",
            "lat": 30.053514016543126,
            "long": 31.366142791794758,
            "area": "16513",
            "city": "fawfe",
            "governorate": "sdaffff",
            "number_of_units": "3443",
            "status": "ACTIVE",
            "amenities": [5],
            "unit_types": [],
            "images": [],
            "banners": [{"url": "https://example.com/image.png"}] * 101,  # Assuming max is 100
            "file": []
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        # Optionally clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()