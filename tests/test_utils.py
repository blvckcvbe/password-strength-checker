# Import the function to evaluate the password
from checker.utils import evaluate_password

# Unit test to check the behavior of a strong password
def test_strong_password():
    """
    Tests that a strong password passes all checks and has high entropy.
    """
    password = "Str0ng!Passw0rd"
    result = evaluate_password(password)

    # Assert that all checks pass for this strong password
    assert all(result["checks"].values())

    # Assert that the entropy is greater than 70 (considered very secure)
    assert result["entropy"] > 70
