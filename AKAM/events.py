import requests
import unittest
from faker import Faker

class TestCreateEvent(unittest.TestCase):

    def setUp(self):
        self.url = "https://community-bac.boyot.app/api/company/events"
        self.token = "2323|S2WGR8YiPowdvdJfnFOpLsZu4zncn9nYs0Srjeu595df1d8b"
        self.faker = Faker()

    def send_request(self, payload):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        return requests.post(self.url, json=payload, headers=headers)

    def test_valid_event_creation(self):
        payload = {
            "description": self.faker.sentence(),
            "title": self.faker.catch_phrase(),
            "start_date": self.faker.date(),
            "end_date": self.faker.date(),
            "images": [
                {"url": self.faker.image_url()}
            ]
        }
        response = self.send_request(payload)
        print(f"Valid Event Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 200)  # Adjusted to 200

    def test_missing_title(self):
        payload = {
            "description": self.faker.sentence(),
            "start_date": self.faker.date(),
            "end_date": self.faker.date(),
            "images": [{"url": self.faker.image_url()}]
        }
        response = self.send_request(payload)
        print(f"Missing Title Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_missing_description(self):
        payload = {
            "title": self.faker.catch_phrase(),
            "start_date": self.faker.date(),
            "end_date": self.faker.date(),
            "images": [{"url": self.faker.image_url()}]
        }
        response = self.send_request(payload)
        print(f"Missing Description Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_start_date_after_end_date(self):
        payload = {
            "description": self.faker.sentence(),
            "title": self.faker.catch_phrase(),
            "start_date": "2024-10-10",
            "end_date": "2024-10-01",
            "images": [{"url": self.faker.image_url()}]
        }
        response = self.send_request(payload)
        print(f"Start Date After End Date Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_format(self):
        payload = {
            "description": self.faker.sentence(),
            "title": self.faker.catch_phrase(),
            "start_date": "invalid-date",
            "end_date": "2024-10-01",
            "images": [{"url": self.faker.image_url()}]
        }
        response = self.send_request(payload)
        print(f"Invalid Date Format Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_missing_image_url(self):
        payload = {
            "description": self.faker.sentence(),
            "title": self.faker.catch_phrase(),
            "start_date": self.faker.date(),
            "end_date": self.faker.date(),
            "images": [{}]  # Missing URL
        }
        response = self.send_request(payload)
        print(f"Missing Image URL Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_empty_payload(self):
        payload = {}
        response = self.send_request(payload)
        print(f"Empty Payload Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 400)

    def test_future_event_creation(self):
        payload = {
            "description": self.faker.sentence(),
            "title": self.faker.catch_phrase(),
            "start_date": "2025-10-25",
            "end_date": "2025-10-30",
            "images": [{"url": self.faker.image_url()}]
        }
        response = self.send_request(payload)
        print(f"Future Event Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 200)  # Adjusted to 200

    def test_duplicate_event(self):
        payload = {
            "description": "Duplicate event description",
            "title": "Duplicate Event",
            "start_date": "2024-10-01",
            "end_date": "2024-10-02",
            "images": [{"url": self.faker.image_url()}]
        }
        # Send the request once
        response = self.send_request(payload)
        print(f"First Duplicate Event Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 200)  # Adjusted to 200

        # Send it again
        response = self.send_request(payload)
        print(f"Second Duplicate Event Response: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 409)  # Assuming 409 Conflict

    def tearDown(self):
        # Optionally: clean up any created resources if needed
        pass

if __name__ == "__main__":
    unittest.main()
