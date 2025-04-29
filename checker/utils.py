import math
import re
import string

# Load a large list of common passwords (e.g., from "Have I Been Pwned")
COMMON_PASSWORDS = set([
    "123456", "password", "qwerty", "letmein", "welcome", "12345678", "123456789", "12345", "111111", "123123",
    "helloworld", "password1", "welcome1", "admin", "abc123", "iloveyou",
    # Add more from a larger dataset as needed
])

# Define possible character sets
CHARACTER_SETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": string.punctuation,
    "unicode": "àáâãäåæçèéêíîìòóôõöøúü"
}

# Define leetspeak substitutions
LEETSPEAK_PATTERNS = {
    'a': '@',
    'o': '0',
    'i': '1',
    's': '$',
    'e': '3',
    't': '7'
}

def calculate_entropy(password):
    """
    Dynamically calculates password entropy based on the actual character sets used.
    Adjusts entropy based on common patterns and predictable structures.
    """
    # Check if the password is in the common password list
    if password.lower() in COMMON_PASSWORDS:
        return 10  # Assign a very low entropy value for common passwords

    # Dynamically calculate the character pool based on the password
    character_pool = set()
    for charset in CHARACTER_SETS.values():
        if any(char in charset for char in password):
            character_pool.update(charset)

    total_chars = len(character_pool)

    # Base entropy calculation
    entropy = len(password) * math.log2(total_chars) if total_chars > 0 else 0

    # Adjust entropy for common patterns (e.g., dictionary words)
    if re.match(r"^[A-Z][a-z]+[\W\d]?$", password):  # Capitalized word with optional symbol/number
        entropy -= 20  # Penalize for predictable patterns

    return max(entropy, 0)  # Ensure entropy is never negative

def estimate_crack_time(password, guesses_per_second=1e12):
    """
    Estimates offline crack time based on modern GPU cracking rates.
    """
    entropy = calculate_entropy(password)
    total_guesses = 2 ** entropy
    seconds = total_guesses / guesses_per_second
    return convert_seconds_to_readable(seconds)

def estimate_online_crack_time(password, guesses_per_second=5):
    """
    Estimates online crack time based on typical rate-limiting policies.
    """
    entropy = calculate_entropy(password)
    total_guesses = 2 ** entropy
    seconds = total_guesses / guesses_per_second
    return convert_seconds_to_readable(seconds)

def convert_seconds_to_readable(seconds):
    """
    Converts seconds to a human-readable format (e.g., years, months, days).
    """
    years = seconds / (60 * 60 * 24 * 365)
    if years >= 1:
        return f"{years:.2f} years"
    months = seconds / (60 * 60 * 24 * 30)
    if months >= 1:
        return f"{months:.2f} months"
    days = seconds / (60 * 60 * 24)
    if days >= 1:
        return f"{days:.2f} days"
    hours = seconds / (60 * 60)
    if hours >= 1:
        return f"{hours:.2f} hours"
    minutes = seconds / 60
    if minutes >= 1:
        return f"{minutes:.2f} minutes"
    return f"{seconds:.0f} seconds"

def is_common_password(password):
    """
    Checks if the password is in a large database of common passwords.
    """
    return password.lower() in COMMON_PASSWORDS

def is_leetspeak(password):
    """
    Checks if the password contains leetspeak substitutions.
    """
    for char, replacement in LEETSPEAK_PATTERNS.items():
        if replacement in password:
            return True
    return False

def evaluate_password(password):
    """
    Evaluates the strength of a password and provides detailed feedback.
    """
    checks = {
        "Length >= 12": len(password) >= 12,
        "Has uppercase": any(char.isupper() for char in password),
        "Has lowercase": any(char.islower() for char in password),
        "Has number": any(char.isdigit() for char in password),
        "Has symbol": any(char in string.punctuation for char in password),
        "Not a common password": not is_common_password(password),
        "Not leetspeak": not is_leetspeak(password),
    }

    entropy = calculate_entropy(password)
    feedback = []

    # Generate feedback based on failed checks
    for check, passed in checks.items():
        if not passed:
            feedback.append(f"Failed check: {check}")

    # Add additional feedback
    if len(password) < 12:
        feedback.append("Password is too short. Consider making it at least 12 characters.")
    if is_common_password(password):
        feedback.append("Password is too common. Avoid using popular passwords.")
    if is_leetspeak(password):
        feedback.append("Password contains leetspeak patterns, which are easier to guess.")

    return {
        "checks": checks,
        "entropy": entropy,
        "offline_crack_time": estimate_crack_time(password),
        "online_crack_time": estimate_online_crack_time(password),
        "feedback": feedback
    }