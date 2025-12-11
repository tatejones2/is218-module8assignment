# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Use an assertion to check that the text within the first <h1> tag is exactly "Hello World".
    # If the text does not match, the test will fail.
    assert page.inner_text('h1') == 'Hello World'

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.

    This test simulates a user performing an addition operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Add" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '5'.
    page.fill('#b', '5')
    
    # Click the button that has the exact text "Add". This triggers the addition operation.
    page.click('button:text("Add")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly "Result: 15".
    # This verifies that the addition operation was performed correctly and the result is displayed as expected.
    assert page.inner_text('#result') == 'Calculation Result: 15'

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator.
    It fills in the numbers, clicks the "Divide" button, and verifies that the appropriate
    error message is displayed. This ensures that the application correctly handles invalid
    operations and provides meaningful feedback to the user.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')
    
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly
    # "Error: Cannot divide by zero!". This verifies that the application handles division by zero
    # gracefully and displays the correct error message to the user.
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'


# =============================================
# COMPREHENSIVE END-TO-END TESTS
# =============================================

@pytest.mark.e2e
def test_calculator_subtract(page, fastapi_server):
    """
    Test the subtraction functionality of the calculator.
    
    This test verifies that a user can perform subtraction and get the correct result.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '20')
    page.fill('#b', '8')
    page.click('button:text("Subtract")')
    assert page.inner_text('#result') == 'Calculation Result: 12'


@pytest.mark.e2e
def test_calculator_multiply(page, fastapi_server):
    """
    Test the multiplication functionality of the calculator.
    
    This test verifies that a user can perform multiplication and get the correct result.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '6')
    page.fill('#b', '7')
    page.click('button:text("Multiply")')
    assert page.inner_text('#result') == 'Calculation Result: 42'


@pytest.mark.e2e
def test_calculator_divide(page, fastapi_server):
    """
    Test the division functionality of the calculator.
    
    This test verifies that a user can perform division and get the correct result.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '20')
    page.fill('#b', '4')
    page.click('button:text("Divide")')
    assert page.inner_text('#result') == 'Calculation Result: 5'


@pytest.mark.e2e
def test_calculator_with_negative_numbers(page, fastapi_server):
    """
    Test the calculator with negative numbers.
    
    This test verifies that the calculator correctly handles negative inputs.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '-10')
    page.fill('#b', '5')
    page.click('button:text("Add")')
    assert page.inner_text('#result') == 'Calculation Result: -5'


@pytest.mark.e2e
def test_calculator_with_decimals(page, fastapi_server):
    """
    Test the calculator with decimal numbers.
    
    This test verifies that the calculator correctly handles decimal inputs.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '10.5')
    page.fill('#b', '2.5')
    page.click('button:text("Add")')
    assert page.inner_text('#result') == 'Calculation Result: 13'


@pytest.mark.e2e
def test_calculator_multiple_operations_sequence(page, fastapi_server):
    """
    Test performing multiple operations in sequence without page reload.
    
    This test verifies that a user can perform multiple calculations by changing
    the input values and clicking different operation buttons.
    """
    page.goto('http://localhost:8000')
    
    # First operation: add 5 + 3
    page.fill('#a', '5')
    page.fill('#b', '3')
    page.click('button:text("Add")')
    assert page.inner_text('#result') == 'Calculation Result: 8'
    
    # Second operation: multiply 4 * 2
    page.fill('#a', '4')
    page.fill('#b', '2')
    page.click('button:text("Multiply")')
    assert page.inner_text('#result') == 'Calculation Result: 8'
    
    # Third operation: subtract 20 - 5
    page.fill('#a', '20')
    page.fill('#b', '5')
    page.click('button:text("Subtract")')
    assert page.inner_text('#result') == 'Calculation Result: 15'


@pytest.mark.e2e
def test_calculator_zero_operations(page, fastapi_server):
    """
    Test calculator operations with zero.
    
    This test verifies correct handling of zero in various operations.
    """
    page.goto('http://localhost:8000')
    
    # Test adding zero
    page.fill('#a', '0')
    page.fill('#b', '5')
    page.click('button:text("Add")')
    assert page.inner_text('#result') == 'Calculation Result: 5'
    
    # Test multiplying by zero
    page.fill('#a', '100')
    page.fill('#b', '0')
    page.click('button:text("Multiply")')
    assert page.inner_text('#result') == 'Calculation Result: 0'


@pytest.mark.e2e
def test_calculator_large_numbers(page, fastapi_server):
    """
    Test calculator with large numbers.
    
    This test verifies that the calculator can handle large number inputs.
    """
    page.goto('http://localhost:8000')
    page.fill('#a', '1000000')
    page.fill('#b', '2000000')
    page.click('button:text("Add")')
    assert page.inner_text('#result') == 'Calculation Result: 3000000'


@pytest.mark.e2e
def test_calculator_clear_fields(page, fastapi_server):
    """
    Test that input fields can be cleared and refilled.
    
    This test verifies that users can clear the input fields and enter new values.
    """
    page.goto('http://localhost:8000')
    
    # Fill in values
    page.fill('#a', '10')
    page.fill('#b', '5')
    
    # Clear and refill
    page.fill('#a', '20')
    page.fill('#b', '3')
    
    page.click('button:text("Subtract")')
    assert page.inner_text('#result') == 'Calculation Result: 17'


@pytest.mark.e2e
def test_calculator_page_title(page, fastapi_server):
    """
    Test that the calculator page has the correct title.
    
    This test verifies the page title/heading is present.
    """
    page.goto('http://localhost:8000')
    # Verify the page contains the main heading
    assert page.locator('h1').count() > 0, "Page should have an h1 heading"


@pytest.mark.e2e
def test_calculator_all_buttons_present(page, fastapi_server):
    """
    Test that all operation buttons are present on the page.
    
    This test verifies that the calculator UI has all expected operation buttons.
    """
    page.goto('http://localhost:8000')
    
    # Check for all operation buttons
    assert page.locator('button:text("Add")').count() == 1, "Add button should be present"
    assert page.locator('button:text("Subtract")').count() == 1, "Subtract button should be present"
    assert page.locator('button:text("Multiply")').count() == 1, "Multiply button should be present"
    assert page.locator('button:text("Divide")').count() == 1, "Divide button should be present"


@pytest.mark.e2e
def test_calculator_input_fields_present(page, fastapi_server):
    """
    Test that both input fields are present on the page.
    
    This test verifies that the calculator has input fields for both operands.
    """
    page.goto('http://localhost:8000')
    
    # Check for input fields
    assert page.locator('#a').count() > 0, "First input field (a) should be present"
    assert page.locator('#b').count() > 0, "Second input field (b) should be present"


@pytest.mark.e2e
def test_calculator_result_display_present(page, fastapi_server):
    """
    Test that result display area is present on the page.
    
    This test verifies that there is a div for displaying calculation results.
    """
    page.goto('http://localhost:8000')
    
    # Check for result display area
    assert page.locator('#result').count() > 0, "Result display area should be present"
