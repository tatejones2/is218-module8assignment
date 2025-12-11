# tests/unit/test_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from typing import Union  # Import Union for type hinting multiple possible types
from app.operations import add, subtract, multiply, divide  # Import the calculator functions from the operations module

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]


# ---------------------------------------------
# Unit Tests for the 'add' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),           # Test adding two positive integers
        (-2, -3, -5),        # Test adding two negative integers
        (2.5, 3.5, 6.0),     # Test adding two positive floats
        (-2.5, 3.5, 1.0),    # Test adding a negative float and a positive float
        (0, 0, 0),            # Test adding zeros
    ],
    ids=[
        "add_two_positive_integers",
        "add_two_negative_integers",
        "add_two_positive_floats",
        "add_negative_and_positive_float",
        "add_zeros",
    ]
)
def test_add(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'add' function with various combinations of integers and floats.

    This parameterized test verifies that the 'add' function correctly adds two numbers,
    whether they are positive, negative, integers, or floats. By using parameterization,
    we can efficiently test multiple scenarios without redundant code.

    Parameters:
    - a (Number): The first number to add.
    - b (Number): The second number to add.
    - expected (Number): The expected result of the addition.

    Steps:
    1. Call the 'add' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_add(2, 3, 5)
    >>> test_add(-2, -3, -5)
    """
    # Call the 'add' function with the provided arguments
    result = add(a, b)
    
    # Assert that the result of add(a, b) matches the expected value
    assert result == expected, f"Expected add({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'subtract' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),           # Test subtracting a smaller positive integer from a larger one
        (-5, -3, -2),        # Test subtracting a negative integer from another negative integer
        (5.5, 2.5, 3.0),     # Test subtracting two positive floats
        (-5.5, -2.5, -3.0),  # Test subtracting two negative floats
        (0, 0, 0),            # Test subtracting zeros
    ],
    ids=[
        "subtract_two_positive_integers",
        "subtract_two_negative_integers",
        "subtract_two_positive_floats",
        "subtract_two_negative_floats",
        "subtract_zeros",
    ]
)
def test_subtract(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'subtract' function with various combinations of integers and floats.

    This parameterized test verifies that the 'subtract' function correctly subtracts the
    second number from the first, handling both positive and negative values, as well as
    integers and floats. Parameterization allows for comprehensive testing of multiple cases.

    Parameters:
    - a (Number): The number from which to subtract.
    - b (Number): The number to subtract.
    - expected (Number): The expected result of the subtraction.

    Steps:
    1. Call the 'subtract' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_subtract(5, 3, 2)
    >>> test_subtract(-5, -3, -2)
    """
    # Call the 'subtract' function with the provided arguments
    result = subtract(a, b)
    
    # Assert that the result of subtract(a, b) matches the expected value
    assert result == expected, f"Expected subtract({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'multiply' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),           # Test multiplying two positive integers
        (-2, 3, -6),         # Test multiplying a negative integer with a positive integer
        (2.5, 4.0, 10.0),    # Test multiplying two positive floats
        (-2.5, 4.0, -10.0),  # Test multiplying a negative float with a positive float
        (0, 5, 0),            # Test multiplying zero with a positive integer
    ],
    ids=[
        "multiply_two_positive_integers",
        "multiply_negative_and_positive_integer",
        "multiply_two_positive_floats",
        "multiply_negative_float_and_positive_float",
        "multiply_zero_and_positive_integer",
    ]
)
def test_multiply(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'multiply' function with various combinations of integers and floats.

    This parameterized test verifies that the 'multiply' function correctly multiplies two numbers,
    handling both positive and negative values, as well as integers and floats. Parameterization
    enables efficient testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The first number to multiply.
    - b (Number): The second number to multiply.
    - expected (Number): The expected result of the multiplication.

    Steps:
    1. Call the 'multiply' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_multiply(2, 3, 6)
    >>> test_multiply(-2, 3, -6)
    """
    # Call the 'multiply' function with the provided arguments
    result = multiply(a, b)
    
    # Assert that the result of multiply(a, b) matches the expected value
    assert result == expected, f"Expected multiply({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'divide' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),           # Test dividing two positive integers
        (-6, 3, -2.0),         # Test dividing a negative integer by a positive integer
        (6.0, 3.0, 2.0),       # Test dividing two positive floats
        (-6.0, 3.0, -2.0),     # Test dividing a negative float by a positive float
        (0, 5, 0.0),            # Test dividing zero by a positive integer
    ],
    ids=[
        "divide_two_positive_integers",
        "divide_negative_integer_by_positive_integer",
        "divide_two_positive_floats",
        "divide_negative_float_by_positive_float",
        "divide_zero_by_positive_integer",
    ]
)
def test_divide(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'divide' function with various combinations of integers and floats.

    This parameterized test verifies that the 'divide' function correctly divides the first
    number by the second, handling both positive and negative values, as well as integers
    and floats. Parameterization allows for efficient and comprehensive testing across multiple cases.

    Parameters:
    - a (Number): The dividend.
    - b (Number): The divisor.
    - expected (float): The expected result of the division.

    Steps:
    1. Call the 'divide' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_divide(6, 3, 2.0)
    >>> test_divide(-6, 3, -2.0)
    """
    # Call the 'divide' function with the provided arguments
    result = divide(a, b)
    
    # Assert that the result of divide(a, b) matches the expected value
    assert result == expected, f"Expected divide({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Negative Test Case: Division by Zero
# ---------------------------------------------

def test_divide_by_zero() -> None:
    """
    Test the 'divide' function with division by zero.

    This negative test case verifies that attempting to divide by zero raises a ValueError
    with the appropriate error message. It ensures that the application correctly handles
    invalid operations and provides meaningful feedback to the user.

    Steps:
    1. Attempt to call the 'divide' function with arguments 6 and 0, which should raise a ValueError.
    2. Use pytest's 'raises' context manager to catch the expected exception.
    3. Assert that the error message contains "Cannot divide by zero!".

    Example:
    >>> test_divide_by_zero()
    """
    # Use pytest's context manager to check for a ValueError when dividing by zero
    with pytest.raises(ValueError) as excinfo:
        # Attempt to divide 6 by 0, which should raise a ValueError
        divide(6, 0)
    
    # Assert that the exception message contains the expected error message
    assert "Cannot divide by zero!" in str(excinfo.value), \
        f"Expected error message 'Cannot divide by zero!', but got '{excinfo.value}'"


# ---------------------------------------------
# Extended Unit Tests: Edge Cases and Coverage
# ---------------------------------------------

class TestAddEdgeCases:
    """Test edge cases and special scenarios for the add function."""
    
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1e10, 1e10, 2e10),  # Test with very large numbers
            (1e-10, 1e-10, 2e-10),  # Test with very small numbers
            (-0, 0, 0),  # Test with negative zero
        ],
        ids=[
            "add_very_large_numbers",
            "add_very_small_numbers",
            "add_negative_zero",
        ]
    )
    def test_add_edge_cases(self, a: Number, b: Number, expected: Number) -> None:
        """Test the add function with edge cases."""
        result = add(a, b)
        assert result == expected


class TestSubtractEdgeCases:
    """Test edge cases and special scenarios for the subtract function."""
    
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1e10, 1e10, 0),  # Test subtracting equal very large numbers
            (5, -5, 10),  # Test subtracting negative number
            (0, -1, 1),  # Test subtracting negative from zero
        ],
        ids=[
            "subtract_equal_large_numbers",
            "subtract_negative_number",
            "subtract_negative_from_zero",
        ]
    )
    def test_subtract_edge_cases(self, a: Number, b: Number, expected: Number) -> None:
        """Test the subtract function with edge cases."""
        result = subtract(a, b)
        assert result == expected


class TestMultiplyEdgeCases:
    """Test edge cases and special scenarios for the multiply function."""
    
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3.5, 7.0),  # Test mixed int and float
            (1e5, 1e5, 1e10),  # Test multiplying large numbers
            (-1, -1, 1),  # Test multiplying negative numbers
            (0.5, 0.5, 0.25),  # Test multiplying decimals
        ],
        ids=[
            "multiply_mixed_types",
            "multiply_large_numbers",
            "multiply_negative_numbers",
            "multiply_decimals",
        ]
    )
    def test_multiply_edge_cases(self, a: Number, b: Number, expected: Number) -> None:
        """Test the multiply function with edge cases."""
        result = multiply(a, b)
        assert result == expected


class TestDivideEdgeCases:
    """Test edge cases and special scenarios for the divide function."""
    
    def test_divide_zero_by_zero(self) -> None:
        """Test dividing zero by zero."""
        with pytest.raises(ValueError):
            divide(0, 0)
    
    def test_divide_by_negative_zero(self) -> None:
        """Test dividing by negative zero."""
        with pytest.raises(ValueError):
            divide(5, -0.0)
    
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1e-10, 1e10, 1e-20),  # Test very small divided by very large
            (100, 3, 33.333333333),  # Test rounding
            (7, 2, 3.5),  # Test integer division returning float
        ],
        ids=[
            "divide_small_by_large",
            "divide_with_rounding",
            "divide_returning_float",
        ]
    )
    def test_divide_edge_cases(self, a: Number, b: Number, expected: Number) -> None:
        """Test the divide function with edge cases."""
        result = divide(a, b)
        # Use approximate equality for floating point comparisons
        assert abs(result - expected) < 1e-9 or result == expected


# ---------------------------------------------
# Integration Tests: Function Combinations
# ---------------------------------------------

class TestOperationCombinations:
    """Test combinations of operations to verify they work together correctly."""
    
    def test_add_then_subtract(self) -> None:
        """Test adding then subtracting."""
        result1 = add(10, 5)
        result2 = subtract(result1, 3)
        assert result2 == 12
    
    def test_multiply_then_divide(self) -> None:
        """Test multiplying then dividing."""
        result1 = multiply(10, 4)
        result2 = divide(result1, 2)
        assert result2 == 20.0
    
    def test_complex_operation_chain(self) -> None:
        """Test a complex chain of operations."""
        # (10 + 5) * 2 - 10 / 5 = 15 * 2 - 2 = 30 - 2 = 28
        step1 = add(10, 5)
        step2 = multiply(step1, 2)
        step3 = divide(10, 5)
        result = subtract(step2, step3)
        assert result == 28.0
