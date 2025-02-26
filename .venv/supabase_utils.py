import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase URL and API Key from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or API Key is missing. Please check your .env file.")

# Table name
TABLE_NAME = "customers"

# Base URL for Supabase REST API
BASE_URL = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"

# Headers for Supabase API requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"  # This ensures that the response includes the created/updated data
}

# CREATE Operation (Insert a new record using POST)
def create_record(data: dict):
    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=data)
        if response.status_code == 201:
            print("Record created:", response.json())
            return response.json()
        else:
            print(f"Error creating record: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("Error creating record:", e)
        return None

# READ Operation (Fetch all records using GET)
def read_records():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        if response.status_code == 200:
            print("Records fetched:", response.json())
            return response.json()
        else:
            print(f"Error fetching records: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("Error fetching records:", e)
        return None

# READ Operation (Fetch a specific record by ID using GET)
def read_record_by_id(record_id: int):
    try:
        url = f"{BASE_URL}?id=eq.{record_id}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            print(f"Record with ID {record_id} fetched:", response.json())
            return response.json()
        else:
            print(f"Error fetching record with ID {record_id}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching record with ID {record_id}:", e)
        return None

# UPDATE Operation (Update a record by ID using PATCH)
def update_record(record_id: int, data: dict):
    try:
        url = f"{BASE_URL}?id=eq.{record_id}"
        response = requests.patch(url, headers=HEADERS, json=data)
        if response.status_code == 200:
            print(f"Record with ID {record_id} updated:", response.json())
            return response.json()
        else:
            print(f"Error updating record with ID {record_id}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error updating record with ID {record_id}:", e)
        return None

# DELETE Operation (Delete a record by ID using DELETE)
def delete_record(record_id: int):
    try:
        url = f"{BASE_URL}?id=eq.{record_id}"
        response = requests.delete(url, headers=HEADERS)
        if response.status_code == 204:
            print(f"Record with ID {record_id} deleted.")
            return True
        else:
            print(f"Error deleting record with ID {record_id}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error deleting record with ID {record_id}:", e)
        return False

# Example Usage
if __name__ == "__main__":
    # Create a new record
    new_record = {"name": "John Doe", "email": "john.doe@example.com"}
    create_record(new_record)

    # Read all records
    read_records()

    # Read a specific record by ID
    read_record_by_id(1)

    # Update a record by ID
    updated_data = {"name": "Jane Doe", "email": "jane.doe@example.com"}
    update_record(1, updated_data)

    # Delete a record by ID
    delete_record(1)