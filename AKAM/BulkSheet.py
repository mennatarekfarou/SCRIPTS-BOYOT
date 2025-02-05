import requests
import time

class TestImportUnits:

    def __init__(self):
        self.url = "https://community-bac.boyot.app/api/admin/import-units"
        self.token = "2553|nPYF58oNstE0sCvtgP7103XJm58rjLnYC1kq8rrA593445e7"  
        self.check_unit_url = "https://community-bac.boyot.app/api/company/units"  
        self.check_unit_token = "2807|AyJNStZ1SLn0zYGwF8imXxHstD44i2JfDIrnPg05abab3c6f"  

    def send_request(self, url, payload, token=None):
        token = token or self.token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        return requests.post(url, json=payload, headers=headers)

    def check_unit_exists(self, customer_mapping_id, unit_code):
        #  check if the unit already exists for the given customer_mapping_id
        check_payload = {
            "customer_mapping_id": customer_mapping_id,
            "unit_code": unit_code
        }
        # Pass the different token for checking units
        check_response = self.send_request(self.check_unit_url, check_payload, token=self.check_unit_token)
        print(f"Status code for check_unit_exists: {check_response.status_code}")
        
        if check_response.status_code == 200:
            try:
                response_json = check_response.json()
                print(f"Response JSON for check_unit_exists: {response_json}")
                # Return whether the unit exists
                return response_json.get("exists", False)
            except ValueError:
                print("Error parsing response as JSON.")
                return False
        else:
            print(f"Failed to check unit existence, status code: {check_response.status_code}")
            return False

    def upload_unit(self, customer_mapping_id, unit_code):
        upload_payload = {
            "company_id": 1,  # Valid company_id
            "project_id": 291,  # Valid project_id
            "sheet_id": "1-AZswdetTrmIzrqh9_YAGRxu2-7zZ2DJh7k4D1p5iAM",  # Valid sheet_id
            "customer_mapping_id": customer_mapping_id,
            "unit_code": unit_code  # Include the unit code in the payload
        }

        upload_response = self.send_request(self.url, upload_payload)
        
        # Check status code and handle response
        if upload_response.status_code == 200 or upload_response.status_code == 201:
            try:
                # If the response contains a JSON message, extract it
                response_json = upload_response.json()
                if response_json.get("status") == "success":
                    print(f"Success: {response_json['message']}")
                elif response_json.get("status") == "error":
                    print(f"Error: {response_json['message']}")
            except ValueError:
                print("Error: Failed to parse JSON response.")
        else:
            # Handle case when the response status code is not 200 or 201
            print(f"Error: Failed to upload unit. Status code: {upload_response.status_code}")
            try:
                # If the response is JSON, print the error details
                error_message = upload_response.json()
                print(f"Error: {error_message.get('message', 'Unknown error occurred')}")
            except ValueError:
                print("No JSON error message in response.")
                print("Raw Response:", upload_response.text)  # Print raw response if not JSON

    def test_upload_units(self):
        customer_mapping_id = "new_mapping_id"
        unit_code = "unit_code_new"

        # First check: Does the unit exist?
        unit_exists = self.check_unit_exists(customer_mapping_id, unit_code)

        if unit_exists:
            print(f"Unit code '{unit_code}' already exists for customer_mapping_id '{customer_mapping_id}'.")
        else:
            # Proceed to upload the unit if it doesn't exist
            self.upload_unit(customer_mapping_id, unit_code)
            # Wait a few seconds before checking again to see if the unit now exists
            time.sleep(5)  # Delay to simulate time taken by backend to update the state

            # Check again if the unit exists after uploading
            unit_exists_after_upload = self.check_unit_exists(customer_mapping_id, unit_code)
            if unit_exists_after_upload:
                print(f"Unit code '{unit_code}' successfully uploaded for customer_mapping_id '{customer_mapping_id}'.")
            else:
                print(f"Failed to upload unit with customer_mapping_id '{customer_mapping_id}' and unit_code '{unit_code}'.")

if __name__ == "__main__":
    test = TestImportUnits()
    test.test_upload_units()
