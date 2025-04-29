import sys
import os

# Add the root directory to the Python path (for local development)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing the function to evaluate the password from utils.py
from checker.utils import evaluate_password
# Importing colorama for color-coded output
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def main():
    """
    Advanced Password Strength Checker
    Continuously evaluates passwords for strength until the user exits.
    """
    # Displaying an introduction message
    print("🔐 Advanced Password Strength Checker")
    print("Type 'exit' to quit.\n")

    # Infinite loop to keep asking for passwords until 'exit' is typed
    while True:
        # Get user input for password
        password = input("Enter password: ")

        # Check if the user wants to exit the program
        if password.lower() == 'exit':
            print(f"{Fore.GREEN}Goodbye! Stay secure!{Style.RESET_ALL}")
            break

        # Check for empty password
        if not password.strip():
            print(f"{Fore.YELLOW}Password cannot be empty. Please try again.{Style.RESET_ALL}")
            continue

        # Evaluate the password (checks if it meets criteria)
        try:
            result = evaluate_password(password)
        except Exception as e:
            print(f"{Fore.RED}Error evaluating password: {e}{Style.RESET_ALL}")
            continue

        # Output the results of the password evaluation
        print("\nPassword Checks:")
        for check, passed in result["checks"].items():
            status = '✔' if passed else '✘'
            color = Fore.GREEN if passed else Fore.RED
            print(f"{color}{check}: {status}{Style.RESET_ALL}")

        # Display the password entropy (security level) and estimated crack time
        print(f"\n{Fore.CYAN}Entropy: {result['entropy']:.2f} bits{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Estimated offline crack time: {result['offline_crack_time']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Estimated online crack time: {result['online_crack_time']}{Style.RESET_ALL}\n")

        # Display additional feedback for improving the password
        if result["feedback"]:
            print(f"{Fore.YELLOW}Suggestions to improve your password:{Style.RESET_ALL}")
            for feedback in result["feedback"]:
                print(f"- {feedback}")
        else:
            print(f"{Fore.GREEN}Your password is strong!{Style.RESET_ALL}")

        print("\n" + "=" * 50 + "\n")


# Ensures that the main() function runs only when the script is executed directly
if __name__ == "__main__":
    main()