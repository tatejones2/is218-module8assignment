# tests/integration/test_fastapi_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from fastapi.testclient import TestClient  # Import TestClient for simulating API requests
from main import app  # Import the FastAPI app instance from your main application file

# ---------------------------------------------
# Pytest Fixture: client
# ---------------------------------------------

@pytest.fixture
def client():
    """
    Pytest Fixture to create a TestClient for the FastAPI application.

    This fixture initializes a TestClient instance that can be used to simulate
    requests to the FastAPI application without running a live server. The client
    is yielded to the test functions and properly closed after the tests complete.

    Benefits:
    - Speeds up testing by avoiding the overhead of running a server.
    - Allows for testing API endpoints in isolation.
    """
    with TestClient(app) as client:
        yield client  # Provide the TestClient instance to the test functions

# ---------------------------------------------
# Test Function: test_add_api
# ---------------------------------------------

def test_add_api(client):
    """
    Test the Addition API Endpoint.

    This test verifies that the `/add` endpoint correctly adds two numbers provided
    in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/add` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`15`).
    """
    # Send a POST request to the '/add' endpoint with JSON payload
    response = client.post('/add', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 15, f"Expected result 15, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_subtract_api
# ---------------------------------------------

def test_subtract_api(client):
    """
    Test the Subtraction API Endpoint.

    This test verifies that the `/subtract` endpoint correctly subtracts the second number
    from the first number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/subtract` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/subtract' endpoint with JSON payload
    response = client.post('/subtract', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_multiply_api
# ---------------------------------------------

def test_multiply_api(client):
    """
    Test the Multiplication API Endpoint.

    This test verifies that the `/multiply` endpoint correctly multiplies two numbers
    provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/multiply` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`50`).
    """
    # Send a POST request to the '/multiply' endpoint with JSON payload
    response = client.post('/multiply', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 50, f"Expected result 50, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_api
# ---------------------------------------------

def test_divide_api(client):
    """
    Test the Division API Endpoint.

    This test verifies that the `/divide` endpoint correctly divides the first number
    by the second number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 2}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/divide' endpoint with JSON payload
    response = client.post('/divide', json={'a': 10, 'b': 2})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_by_zero_api
# ---------------------------------------------

def test_divide_by_zero_api(client):
    """
    Test the Division by Zero API Endpoint.

    This test verifies that the `/divide` endpoint correctly handles division by zero
    by returning an appropriate error message and status code.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 0}`.
    2. Assert that the response status code is `400 Bad Request`.
    3. Assert that the JSON response contains an 'error' field with the message "Cannot divide by zero!".
    """
    # Send a POST request to the '/divide' endpoint with JSON payload attempting division by zero
    response = client.post('/divide', json={'a': 10, 'b': 0})
    
    # Assert that the response status code is 400 (Bad Request), indicating an error occurred
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    
    # Assert that the JSON response contains an 'error' field
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"
    
    # Assert that the 'error' field contains the correct error message
    assert "Cannot divide by zero!" in response.json()['error'], \
        f"Expected error message 'Cannot divide by zero!', got '{response.json()['error']}'"


# =============================================
# ADDITIONAL COMPREHENSIVE INTEGRATION TESTS
# =============================================

# Test the root endpoint
def test_root_endpoint(client):
    """
    Test the root endpoint returns HTML content.
    
    This test verifies that the GET / endpoint returns a 200 status code
    and serves HTML template content.
    """
    response = client.get('/')
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert 'text/html' in response.headers.get('content-type', ''), \
        f"Expected HTML content-type, got {response.headers.get('content-type')}"


# Test error handling with invalid input types
def test_add_with_invalid_input(client):
    """
    Test the add endpoint with invalid input (non-numeric).
    
    This test verifies that the API properly validates input and returns
    an appropriate error response when non-numeric values are provided.
    """
    response = client.post('/add', json={'a': 'not a number', 'b': 5})
    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"
    assert 'error' in response.json() or 'detail' in response.json(), \
        "Response should contain error information"


# Test error handling with missing required fields
def test_add_with_missing_field(client):
    """
    Test the add endpoint with missing required field.
    
    This test verifies that the API properly validates that both 'a' and 'b'
    are provided in the request.
    """
    response = client.post('/add', json={'a': 5})
    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"


def test_subtract_with_missing_field(client):
    """Test the subtract endpoint with missing required field."""
    response = client.post('/subtract', json={'b': 3})
    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"


def test_multiply_with_missing_field(client):
    """Test the multiply endpoint with missing required field."""
    response = client.post('/multiply', json={'a': 10})
    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"


def test_divide_with_missing_field(client):
    """Test the divide endpoint with missing required field."""
    response = client.post('/divide', json={'b': 2})
    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"


# Test with floating point numbers
def test_add_with_floats(client):
    """Test the add endpoint with floating point numbers."""
    response = client.post('/add', json={'a': 2.5, 'b': 3.5})
    assert response.status_code == 200
    assert response.json()['result'] == 6.0


def test_subtract_with_floats(client):
    """Test the subtract endpoint with floating point numbers."""
    response = client.post('/subtract', json={'a': 10.5, 'b': 5.2})
    assert response.status_code == 200
    assert abs(response.json()['result'] - 5.3) < 0.001


def test_multiply_with_floats(client):
    """Test the multiply endpoint with floating point numbers."""
    response = client.post('/multiply', json={'a': 2.5, 'b': 4.0})
    assert response.status_code == 200
    assert response.json()['result'] == 10.0


def test_divide_with_floats(client):
    """Test the divide endpoint with floating point numbers."""
    response = client.post('/divide', json={'a': 10.5, 'b': 2.5})
    assert response.status_code == 200
    assert abs(response.json()['result'] - 4.2) < 0.001


# Test with negative numbers
def test_add_with_negative_numbers(client):
    """Test the add endpoint with negative numbers."""
    response = client.post('/add', json={'a': -10, 'b': 5})
    assert response.status_code == 200
    assert response.json()['result'] == -5


def test_subtract_with_negative_numbers(client):
    """Test the subtract endpoint with negative numbers."""
    response = client.post('/subtract', json={'a': -10, 'b': -5})
    assert response.status_code == 200
    assert response.json()['result'] == -5


def test_multiply_with_negative_numbers(client):
    """Test the multiply endpoint with negative numbers."""
    response = client.post('/multiply', json={'a': -10, 'b': 5})
    assert response.status_code == 200
    assert response.json()['result'] == -50


def test_divide_with_negative_numbers(client):
    """Test the divide endpoint with negative numbers."""
    response = client.post('/divide', json={'a': -10, 'b': 5})
    assert response.status_code == 200
    assert response.json()['result'] == -2.0


# Test with zero
def test_add_with_zero(client):
    """Test the add endpoint with zero."""
    response = client.post('/add', json={'a': 0, 'b': 0})
    assert response.status_code == 200
    assert response.json()['result'] == 0


def test_multiply_with_zero(client):
    """Test the multiply endpoint with zero."""
    response = client.post('/multiply', json={'a': 0, 'b': 100})
    assert response.status_code == 200
    assert response.json()['result'] == 0


# Test with large numbers
def test_add_with_large_numbers(client):
    """Test the add endpoint with large numbers."""
    response = client.post('/add', json={'a': 1e10, 'b': 1e10})
    assert response.status_code == 200
    assert response.json()['result'] == 2e10


def test_multiply_with_large_numbers(client):
    """Test the multiply endpoint with large numbers."""
    response = client.post('/multiply', json={'a': 1e5, 'b': 1e5})
    assert response.status_code == 200
    assert response.json()['result'] == 1e10


# Test response structure
def test_response_structure(client):
    """Test that API responses have the correct structure."""
    response = client.post('/add', json={'a': 5, 'b': 3})
    data = response.json()
    assert 'result' in data, "Response should contain 'result' field"
    assert isinstance(data['result'], (int, float)), "Result should be numeric"
