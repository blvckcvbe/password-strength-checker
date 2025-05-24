import math
import re
import string

# Load a large list of common passwords from rockyou.txt (around 14 million or so)
COMMON_PASSWORD_RANKS = {}

with open("rockyou.txt.gz", encoding="latin-1") as f:
    for rank, line in enumerate(f, 1):  # Start ranks from 1
        password = line.strip().lower()
        if password and password not in COMMON_PASSWORD_RANKS:
            COMMON_PASSWORD_RANKS[password] = rank

TOTAL_COMMON_PASSWORDS = len(COMMON_PASSWORD_RANKS)

# Define possible character sets
CHARACTER_SETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": string.punctuation,
    "unicode": "àáâãäåæçèéêíîìòóôõöøúü"
}

# Define leetspeak substitutions with common possible replacements
LEETSPEAK_PATTERNS = {
    'a': ['@', '4', '^', 'aye', '(L'],
    'b': ['I3', '8', '13', '6'],
    'o': ['0'],
    'i': ['1', '!'],
    's': ['$', '5'],
    'e': ['3'],
    't': ['7']
}

HASH_RATES = {
    'md5': 1.2e11,
    'sha1': 1.0e11,
    'sha256': 2.5e10,
    'ntlm': 1.4e11,
    'bcrypt': 500,
    'argon2id': 1200,
    'scrypt': 800,
}

def calculate_entropy(password):
    """
    Calculates password entropy based on:
    - Rank in common password list (if found)
    - Dynamic character set size based on actual characters used
    - Adjustments for common patterns
    """
    password_lower = password.lower()

    # Early check for empty/whitespace-only password
    if not password.strip():
        return 0

    # Use rank-based entropy if the password is in the common password list
    if password_lower in COMMON_PASSWORD_RANKS:
        rank = COMMON_PASSWORD_RANKS[password_lower]
        # Entropy based on guess number: total_common / rank
        guess_number = max(TOTAL_COMMON_PASSWORDS / rank, 1)
        return math.log2(guess_number)

    # Build character pool based on actual characters used in password
    character_pool = set()
    for charset in CHARACTER_SETS.values():
        chars_in_password = set(c for c in password if c in charset)
        if chars_in_password:
            character_pool.update(chars_in_password)

    total_chars = len(character_pool)
    if total_chars == 0:
        # In case password has unusual chars not in defined sets, fall back to full ASCII printable range (or len=95 for printable ASCII)
        total_chars = 95

    # Base entropy calculation
    entropy = len(password) * math.log2(total_chars)

    # This regex matches: Capitalized word + optional symbol/digit at end
    if re.match(r"^[A-Z][a-z]+[\W\d]?$", password):
        penalty = entropy * 0.4  # Penalty for common pattern
        entropy -= penalty

    return max(entropy, 0)

def estimate_crack_time(password, hash_type='md5'):
    """
    Estimates offline crack time based on selected hash type.
    """
    entropy = calculate_entropy(password)
    guesses_per_second = HASH_RATES.get(hash_type, 1e11)  # fallback default
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
    return f"{seconds:.3f} seconds"

def is_common_password(password):
    """
    Checks if the password is in a large database of common passwords.
    """
    return password.lower() in COMMON_PASSWORD_RANKS

def is_leetspeak(password):
    """
    Checks if the password contains leetspeak substitutions.
    """
    password_lower = password.lower()
    for replacements in LEETSPEAK_PATTERNS.values():
        count = sum(1 for r in replacements if r in password_lower)
        if count > 1:  # Need more than 1 to be accurately considered 'leetspeak'
            return True
    return False

def evaluate_password(password):
    """
    Evaluates the strength of a password and provides detailed feedback.
    """
    # Early empty check
    if not password.strip():
        return {
            "checks": {},
            "entropy": 0,
            "offline_crack_time": "N/A",
            "online_crack_time": "N/A",
            "feedback": ["Password cannot be empty or whitespace only."]
        }

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
    if len(password) < 12:
        feedback.append("Password is too short. Consider making it at least 12 characters.")
    if is_common_password(password):
        feedback.append("Password is too common. Avoid using popular passwords.")
    if is_leetspeak(password):
        feedback.append("Password contains leetspeak patterns, which are easier to guess.")

    if entropy < 28:
        feedback.append("Very weak password.")
    elif entropy < 36:
        feedback.append("Weak password.")
    elif entropy < 60:
        feedback.append("Moderate strength password.")
    else:
        feedback.append("Strong password.")

    return {
        "checks": checks,
        "entropy": entropy,
        "offline_crack_time": estimate_crack_time(password),
        "online_crack_time": estimate_online_crack_time(password),
        "feedback": feedback
    }
