import unittest
import requests
from faker import Faker

class TestNewRegister(unittest.TestCase):

    def setUp(self):
        self.url = "https://bcommunity.test.boyot.app/api/company/register"
        self.faker = Faker()

    def send_request(self, payload):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "language": "en"
        }
        return requests.post(self.url, json=payload, headers=headers)

    def print_response(self, response):
        print(f"Status Code: {response.status_code}")
        try:
            print("Response:", response.json())
        except ValueError:
            print("No JSON response")

    def test_successful_registration(self):
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": self.faker.email(),
            "mobile_number": self.faker.msisdn()[:10],
            "user_type_id": 1,
            "gender": "MALE",
            "birthdate": "1990-05-15",
            "password": "securePassword123",
            "password_confirmation": "securePassword123",
            "company_name": "Badreldin",
            "unit_code": "UNIT123",
            "customer_number": "CUST456",
            "national_type": "National_ID",
            "attachments": [
                {"url": "https://bcommunity.test.boyot.app/attachments/Kayan-Logo.png_1_(6)_1744809877.png"},
                {"url": "https://bcommunity.test.boyot.app/attachments/Kayan-Logo.png_1_(6)_1744809877.png"}
            ]
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertEqual(response.status_code, 201)

    def test_missing_required_fields(self):
        payload = {
            "first_name": "John"
            # Missing all other required fields
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertIn(response.status_code, [400, 422])

    def test_invalid_email_format(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "invalid-email",
            "mobile_number": self.faker.msisdn()[:10],
            "user_type_id": 1,
            "gender": "FEMALE",
            "birthdate": "1991-04-20",
            "password": "securePassword123",
            "password_confirmation": "securePassword123",
            "company_name": "Badreldin",
            "unit_code": "UNIT456",
            "customer_number": "CUST789",
            "national_type": "Passport"
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertIn(response.status_code, [400, 422])

    def test_duplicate_mobile_number(self):
        mobile_number = "1234567890"
        payload1 = {
            "first_name": "Ali",
            "last_name": "Khan",
            "email": self.faker.email(),
            "mobile_number": mobile_number,
            "user_type_id": 2,
            "gender": "MALE",
            "birthdate": "1993-01-01",
            "password": "securePassword123",
            "password_confirmation": "securePassword123",
            "company_name": "Badreldin",
            "unit_code": "UNIT999",
            "customer_number": "CUST999",
            "national_type": "Birth_Certificate"
        }
        payload2 = payload1.copy()
        payload2["email"] = self.faker.email()

        # First request should succeed
        response1 = self.send_request(payload1)
        self.print_response(response1)

        # Second request should fail due to duplicate mobile number
        response2 = self.send_request(payload2)
        self.print_response(response2)
        self.assertEqual(response2.status_code, 422)

    def test_password_mismatch(self):
        payload = {
            "first_name": "Mismatch",
            "last_name": "Test",
            "email": self.faker.email(),
            "mobile_number": self.faker.msisdn()[:10],
            "user_type_id": 2,
            "gender": "MALE",
            "birthdate": "1995-07-15",
            "password": "password123",
            "password_confirmation": "differentPassword",
            "company_name": "Badreldin",
            "unit_code": "UNIT321",
            "customer_number": "CUST654",
            "national_type": "National_ID"
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertIn(response.status_code, [400, 422])

    def test_invalid_national_type(self):
        payload = {
            "first_name": "Invalid",
            "last_name": "IDType",
            "email": self.faker.email(),
            "mobile_number": self.faker.msisdn()[:10],
            "user_type_id": 2,
            "gender": "FEMALE",
            "birthdate": "1992-11-11",
            "password": "securePassword123",
            "password_confirmation": "securePassword123",
            "company_name": "Badreldin",
            "unit_code": "UNIT998",
            "customer_number": "CUST998",
            "national_type": "DRIVER_LICENSE"  # Invalid value
        }
        response = self.send_request(payload)
        self.print_response(response)
        self.assertIn(response.status_code, [400, 422])

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
