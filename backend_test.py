#!/usr/bin/env python3
import requests
import json
import sys
import time
from typing import Dict, List, Any, Tuple, Optional
import os
import dotenv
import random

# Load environment variables from frontend/.env to get the backend URL
dotenv.load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Ensure the URL ends with /api
API_URL = f"{BACKEND_URL}/api"
print(f"Using API URL: {API_URL}")

# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def run_test(test_name: str, test_func, *args, **kwargs) -> bool:
    """Run a test function and track results"""
    global test_results
    test_results["total"] += 1
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'-'*80}")
    
    start_time = time.time()
    try:
        result = test_func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        
        if result:
            test_results["passed"] += 1
            status = "PASSED"
        else:
            test_results["failed"] += 1
            status = "FAILED"
            
        test_results["tests"].append({
            "name": test_name,
            "status": status,
            "duration": duration
        })
        
        print(f"{status} in {duration:.2f}s")
        return result
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        test_results["failed"] += 1
        test_results["tests"].append({
            "name": test_name,
            "status": "ERROR",
            "duration": duration,
            "error": str(e)
        })
        print(f"ERROR in {duration:.2f}s: {str(e)}")
        return False

def test_api_health() -> bool:
    """Test the API health endpoint"""
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check status code
        if response.status_code != 200:
            print(f"Expected status code 200, got {response.status_code}")
            return False
        
        # Check response content
        data = response.json()
        if "message" not in data or data["message"] != "Welcome to the Dog Breeds API":
            print(f"Unexpected response content: {data}")
            return False
        
        # Check CORS headers
        if 'access-control-allow-origin' not in response.headers:
            print("CORS headers not found in response")
            return False
        
        print("API health check passed")
        return True
    except Exception as e:
        print(f"Error testing API health: {e}")
        return False

def test_breeds_population() -> bool:
    """Test the breeds population endpoint"""
    try:
        response = requests.post(f"{API_URL}/breeds/populate")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check status code
        if response.status_code != 200:
            print(f"Expected status code 200, got {response.status_code}")
            return False
        
        # Check response content
        data = response.json()
        if "message" not in data or "Successfully populated" not in data["message"]:
            print(f"Unexpected response content: {data}")
            return False
        
        # Extract number of breeds populated
        import re
        match = re.search(r"Successfully populated (\d+) dog breeds", data["message"])
        if not match:
            print(f"Could not extract number of breeds from message: {data['message']}")
            return False
        
        num_breeds = int(match.group(1))
        if num_breeds < 25:
            print(f"Expected at least 25 breeds, got {num_breeds}")
            return False
        
        print(f"Successfully populated {num_breeds} breeds")
        return True
    except Exception as e:
        print(f"Error testing breeds population: {e}")
        return False

def test_breeds_retrieval() -> Tuple[bool, Optional[List[Dict[str, Any]]]]:
    """Test the breeds retrieval endpoint"""
    try:
        response = requests.get(f"{API_URL}/breeds")
        print(f"Status Code: {response.status_code}")
        print(f"Response contains {len(response.json())} breeds")
        
        # Check status code
        if response.status_code != 200:
            print(f"Expected status code 200, got {response.status_code}")
            return False, None
        
        # Check response content
        breeds = response.json()
        if not isinstance(breeds, list):
            print(f"Expected a list of breeds, got {type(breeds)}")
            return False, None
        
        # Check number of breeds
        if len(breeds) < 25:
            print(f"Expected at least 25 breeds, got {len(breeds)}")
            return False, None
        
        # Check breed fields
        required_fields = [
            "id", "name", "size", "temperament", "origin", "lifespan", 
            "weight", "height", "care_level", "exercise_needs", 
            "good_with_kids", "good_with_pets", "grooming_needs", 
            "image_url", "description", "health_issues", "breed_group"
        ]
        
        # Check a random breed for all required fields
        sample_breed = random.choice(breeds)
        print(f"Checking sample breed: {sample_breed['name']}")
        
        missing_fields = [field for field in required_fields if field not in sample_breed]
        if missing_fields:
            print(f"Missing required fields in breed: {missing_fields}")
            return False, None
        
        # Check that all image URLs are valid
        for breed in breeds[:5]:  # Check first 5 breeds to avoid too many requests
            image_url = breed.get("image_url")
            if not image_url:
                print(f"Breed {breed['name']} has no image URL")
                continue
                
            try:
                img_response = requests.head(image_url)
                if img_response.status_code != 200:
                    print(f"Image URL for {breed['name']} returned status {img_response.status_code}: {image_url}")
            except Exception as e:
                print(f"Error checking image URL for {breed['name']}: {e}")
        
        print(f"Successfully retrieved {len(breeds)} breeds with all required fields")
        return True, breeds
    except Exception as e:
        print(f"Error testing breeds retrieval: {e}")
        return False, None

def test_individual_breed_retrieval(breeds: List[Dict[str, Any]]) -> bool:
    """Test the individual breed retrieval endpoint"""
    if not breeds:
        print("No breeds available for testing")
        return False
    
    try:
        # Test with a valid breed ID
        sample_breed = random.choice(breeds)
        breed_id = sample_breed["id"]
        
        print(f"Testing retrieval of breed with ID: {breed_id}")
        response = requests.get(f"{API_URL}/breeds/{breed_id}")
        
        print(f"Status Code: {response.status_code}")
        
        # Check status code
        if response.status_code != 200:
            print(f"Expected status code 200, got {response.status_code}")
            return False
        
        # Check response content
        breed = response.json()
        if not isinstance(breed, dict):
            print(f"Expected a breed object, got {type(breed)}")
            return False
        
        # Check that the retrieved breed matches the expected breed
        if breed["id"] != breed_id or breed["name"] != sample_breed["name"]:
            print(f"Retrieved breed does not match expected breed")
            print(f"Expected: {sample_breed['name']}, Got: {breed['name']}")
            return False
        
        # Test with an invalid breed ID
        invalid_id = "invalid-id-12345"
        print(f"Testing retrieval with invalid ID: {invalid_id}")
        invalid_response = requests.get(f"{API_URL}/breeds/{invalid_id}")
        
        print(f"Status Code for invalid ID: {invalid_response.status_code}")
        
        # Check status code for invalid ID
        if invalid_response.status_code != 404:
            print(f"Expected status code 404 for invalid ID, got {invalid_response.status_code}")
            return False
        
        print("Successfully tested individual breed retrieval")
        return True
    except Exception as e:
        print(f"Error testing individual breed retrieval: {e}")
        return False

def test_search_functionality(breeds: List[Dict[str, Any]]) -> bool:
    """Test the search functionality endpoint"""
    if not breeds:
        print("No breeds available for testing")
        return False
    
    try:
        # Test cases for search
        search_tests = [
            # Search by breed name
            {"query": "Golden", "expected_field": "name", "expected_value": "Golden Retriever"},
            # Search by temperament
            {"query": "Friendly", "expected_field": "temperament", "expected_contains": "Friendly"},
            # Search by breed group
            {"query": "Sporting", "expected_field": "breed_group", "expected_value": "Sporting"},
            # Search by size
            {"query": "Large", "expected_field": "size", "expected_value": "Large"}
        ]
        
        for test_case in search_tests:
            query = test_case["query"]
            print(f"\nTesting search with query: '{query}'")
            
            response = requests.get(f"{API_URL}/breeds/search/{query}")
            print(f"Status Code: {response.status_code}")
            
            # Check status code
            if response.status_code != 200:
                print(f"Expected status code 200, got {response.status_code}")
                return False
            
            # Check response content
            results = response.json()
            if not isinstance(results, list):
                print(f"Expected a list of results, got {type(results)}")
                return False
            
            print(f"Found {len(results)} results for query '{query}'")
            
            # Check that we got at least one result
            if len(results) == 0:
                print(f"Expected at least one result for query '{query}', got none")
                return False
            
            # Check that the results match the expected criteria
            expected_field = test_case["expected_field"]
            
            if "expected_value" in test_case:
                expected_value = test_case["expected_value"]
                found_match = any(breed[expected_field] == expected_value for breed in results)
                if not found_match:
                    print(f"Expected to find a breed with {expected_field}={expected_value}, but none found")
                    return False
            elif "expected_contains" in test_case:
                expected_contains = test_case["expected_contains"]
                found_match = any(expected_contains in breed[expected_field] for breed in results)
                if not found_match:
                    print(f"Expected to find a breed with {expected_contains} in {expected_field}, but none found")
                    return False
        
        print("Successfully tested search functionality")
        return True
    except Exception as e:
        print(f"Error testing search functionality: {e}")
        return False

def test_error_handling() -> bool:
    """Test error handling for malformed requests"""
    try:
        # Test non-existent endpoint
        print("Testing non-existent endpoint")
        response = requests.get(f"{API_URL}/nonexistent")
        print(f"Status Code: {response.status_code}")
        
        # Check status code
        if response.status_code < 400:
            print(f"Expected error status code (4xx), got {response.status_code}")
            return False
        
        print("Successfully tested error handling")
        return True
    except Exception as e:
        print(f"Error testing error handling: {e}")
        return False

def print_summary():
    """Print a summary of test results"""
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("-"*80)
    print(f"Total Tests: {test_results['total']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    print(f"Success Rate: {(test_results['passed'] / test_results['total']) * 100:.2f}%")
    print("="*80)
    
    # Print details of failed tests
    if test_results['failed'] > 0:
        print("\nFAILED TESTS:")
        for test in test_results['tests']:
            if test['status'] != 'PASSED':
                print(f"- {test['name']}: {test['status']}")
                if 'error' in test:
                    print(f"  Error: {test['error']}")
        print("="*80)

def main():
    """Run all tests"""
    print(f"Starting Dog Breeds API Tests against {API_URL}")
    
    # Test API health
    api_health_ok = run_test("API Health Check", test_api_health)
    if not api_health_ok:
        print("API health check failed, aborting further tests")
        print_summary()
        return
    
    # Test breeds population
    breeds_population_ok = run_test("Breeds Data Population", test_breeds_population)
    if not breeds_population_ok:
        print("Breeds population failed, aborting further tests")
        print_summary()
        return
    
    # Test breeds retrieval
    breeds_retrieval_ok, breeds = run_test("Breeds Retrieval", test_breeds_retrieval)
    if not breeds_retrieval_ok or not breeds:
        print("Breeds retrieval failed, aborting further tests")
        print_summary()
        return
    
    # Test individual breed retrieval
    run_test("Individual Breed Retrieval", test_individual_breed_retrieval, breeds)
    
    # Test search functionality
    run_test("Search Functionality", test_search_functionality, breeds)
    
    # Test error handling
    run_test("Error Handling", test_error_handling)
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    main()