#!/usr/bin/env python
"""
Demo script to test eBay Marketplace Account Deletion endpoints.
This script shows how to interact with the new endpoints.
"""
import os
import requests
import json

# Set the base URL (change this to your deployed URL)
BASE_URL = os.getenv('APP_URL', 'http://localhost:5000')

def test_verification_token():
    """Test the verification token endpoint."""
    print("=" * 60)
    print("Testing Verification Token Endpoint")
    print("=" * 60)
    
    url = f"{BASE_URL}/ebay/verification-token"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_marketplace_account_deletion():
    """Test the marketplace account deletion endpoint."""
    print("=" * 60)
    print("Testing Marketplace Account Deletion Endpoint")
    print("=" * 60)
    
    url = f"{BASE_URL}/ebay/marketplace-account-deletion"
    print(f"POST {url}")
    
    # Sample payload matching eBay's notification format
    payload = {
        "metadata": {
            "topic": "MARKETPLACE_ACCOUNT_DELETION",
            "schemaVersion": "1.0",
            "deprecated": False
        },
        "notification": {
            "notificationId": "550e8400-e29b-41d4-a716-446655440000",
            "eventDate": "2026-02-04T12:00:00.000Z",
            "publishDate": "2026-02-04T12:00:01.000Z",
            "publishAttemptCount": 1,
            "data": {
                "username": "test_user_123",
                "userId": "987654321",
                "eiasToken": "sample-token-abc123"
            }
        }
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_health_endpoint():
    """Test the health check endpoint."""
    print("=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)
    
    url = f"{BASE_URL}/health"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     eBay Marketplace Account Deletion Test Script      ║
    ║                                                        ║
    ║  Make sure the Flask app is running on port 5000      ║
    ║  and EBAY_VERIFICATION_TOKEN is set in .env           ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Test all endpoints
    test_health_endpoint()
    test_verification_token()
    test_marketplace_account_deletion()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
