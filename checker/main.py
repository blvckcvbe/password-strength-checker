import sys
import os

# Add the root directory to the Python path (for local development)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from checker.utils import evaluate_password, estimate_crack_time, HASH_RATES
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print("🔐 Advanced Password Strength Checker")
    print("Type 'exit' to quit.\n")

    while True:
        password = input("Enter password: ")
        if password.lower() == 'exit':
            print(f"{Fore.GREEN}Goodbye! Stay secure!{Style.RESET_ALL}")
            break
        if not password.strip():
            print(f"{Fore.YELLOW}Password cannot be empty. Please try again.{Style.RESET_ALL}")
            continue

        try:
            result = evaluate_password(password)
        except Exception as e:
            print(f"{Fore.RED}Error evaluating password: {e}{Style.RESET_ALL}")
            continue

        print("\nPassword Checks:")
        for check, passed in result["checks"].items():
            status = '✔' if passed else '✘'
            color = Fore.GREEN if passed else Fore.RED
            print(f"{color}{check}: {status}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Entropy: {result['entropy']:.2f} bits{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Estimated offline crack time (default): {result['offline_crack_time']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Estimated online crack time: {result['online_crack_time']}{Style.RESET_ALL}\n")

        # Print crack times for all hash types
        print(f"{Fore.MAGENTA}Crack times for different hash types:{Style.RESET_ALL}")
        for hash_type in HASH_RATES.keys():
            crack_time = estimate_crack_time(password, hash_type=hash_type)
            print(f"{Fore.LIGHTMAGENTA_EX}{hash_type.upper():<10}: {crack_time}{Style.RESET_ALL}")
        print()

        if result["feedback"]:
            print(f"{Fore.YELLOW}Suggestions to improve your password:{Style.RESET_ALL}")
            for feedback in result["feedback"]:
                print(f"- {feedback}")
        else:
            print(f"{Fore.GREEN}Your password is strong!{Style.RESET_ALL}")

        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
