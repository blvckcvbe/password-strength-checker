# 🔐 Advanced Password Strength Checker

This is a terminal-based password evaluation tool written in Python. It checks password strength based on:

- ✅ Minimum length
- ✅ Use of upper/lowercase letters, numbers, and symbols
- ✅ Entropy calculation (bits of security)
- ✅ Estimated brute-force crack time
  
🎨 Using `colorama` for color-coded outputs to make it more readable and user-friendly.

---

## ✨ Password Strength Metrics Explained

### 🔐 **Offline Crack Time**
- **Definition:** How long it would take an attacker to guess your password if they already have access to its encrypted hash (e.g., after a data breach).
- **Speed:** Billions of guesses per second using modern GPUs.
- **Tools:** Hashcat, John the Ripper.
- **Risk:** Extremely high for weak passwords.

### 🌐 **Online Crack Time**
- **Definition:** Time to guess your password through a live interface (e.g., login form).
- **Speed:** Slow due to network delays, rate limits, and CAPTCHA.
- **Tools:** Hydra, browser automation.
- **Risk:** Lower, but still dangerous if MFA/2FA isn't enabled.

---

## How the Crack Time Estimates Are Calculated

### Assumptions
1. **Offline Crack Time**:
   - Assumes no salting and fast hashing algorithms like MD5 or SHA-1.
   - Offline cracking speed: ~1 trillion guesses per second (modern GPUs).
       - (seems a bit unrealistic but I did it like this because compared to other password strength checkers, this was waayy off (by a billion years!)
        so i just increased the guesses per second and it seemed to make it more accurate. If it didn't fix it please do let me know.)
       - *Edit*: perhaps I could adjust the dictionary used and that could fix the accuracy? Rather than just changing the guesses per second? 
   - For bcrypt or Argon2, the effective cracking speed drops to ~100 guesses per second.

2. **Online Crack Time**:
   - Assumes no rate-limiting or MFA/2FA.
   - Online cracking speed: ~5 guesses per second (typical for rate-limited systems).

---

## Real-World Defenses
- **Salting:** Ensures that hashes are unique, even for identical passwords, preventing precomputed attacks (e.g., rainbow tables).
- **Slow Hashing Algorithms:** Algorithms like bcrypt or Argon2 are computationally expensive and drastically slow down offline attacks.
- **Rate Limiting:** Restricts the number of login attempts per second, making online brute-forcing impractical.
- **Multi-Factor Authentication (MFA):** Adds an additional layer of security that renders brute-forcing ineffective.

---

## 🚀 Setup

### 🐧 Arch Linux / Fish Shell:
```fish
git clone https://github.com/blvckcvbe/password-strength-checker
sudo pacman -S python
cd ~/password-strength-checker
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
```

### 🐧 Debian / Ubuntu:
```bash
git clone https://github.com/blvckcvbe/password-strength-checker
sudo apt update && sudo apt install python3 python3-venv python3-pip -y
cd ~/password-strength-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🪟 Windows 11 (PowerShell):
```powershell
git clone https://github.com/blvckcvbe/password-strength-checker
winget install -e --id Python.Python.3.11 --scope machine
cd C:\path\to\password-strength-checker
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 🍎 macOS:
Install Python using Homebrew (if you don't have Homebrew installed, follow instructions [here](https://brew.sh/)):
```bash
git clone https://github.com/blvckcvbe/password-strength-checker
brew install python
cd ~/password-strength-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python checker/main.py
```

---

## ✅ Example Output
```
🔐 Advanced Password Strength Checker
Type 'exit' to quit.

Enter password: P@ssw0rd123

Password Checks:
Length >= 12: ✔
Has uppercase: ✔
Has lowercase: ✔
Has number: ✔
Has symbol: ✔

Entropy: 75.35 bits
Estimated offline crack time: ~22 years
Estimated online crack time: ~120,000 years
```

---

## 🧪 Run Tests
```bash
pytest tests/
```

---

## Exit
Once your done, simply type exit, then deactivate to leave the virtual environment

---

## Feedback
If you have any feedback on my password-checker please do let me know! I want to improve it and make it as accurate as possible. Thank you!

## 📂 License
MIT

---

## 🙋‍♂️ Author
**Rumi** – [GitHub](https://github.com/blvckcvbe)
