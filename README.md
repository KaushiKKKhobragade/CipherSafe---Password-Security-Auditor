<img width="1536" height="1024" alt="CipherSafe 1" src="https://github.com/user-attachments/assets/734708da-a783-42f2-9618-e35010ce23da" />

# 🔐 CipherSafe — Password Security Auditor

CipherSafe is a terminal-based cybersecurity tool built with Python for analysing password strength, generating secure passwords, checking real-world data breaches, and educating users about password security.

Developed as a cybersecurity-focused CLI application, CipherSafe combines security analysis with an interactive hacker-style terminal experience.

---

## 🚀 Features

### 1. Secure Password Generator
- Cryptographically secure password generation using Python's `secrets` module
- Random password generation
- Secure passphrase generation
- Strength scores and grading system
- Multiple password suggestions

### 2. Dark Web Breach Scanner
- Real-time breach detection using the HaveIBeenPwned API
- Uses the secure k-anonymity model
- Passwords are SHA-1 hashed locally
- Supports single and bulk password checks
- Optional JSON report export

### 3. Password Strength Analyser
- Entropy calculation
- Character diversity analysis
- Pattern and weakness detection
- Crack-time estimation
- Recursive character scanning
- Multi-dimensional strength matrix

### 4. Password Time Machine
A unique feature that estimates how long a password would take to crack across different eras of computing:
- 1980s computers
- 1990s PCs
- Modern GPU clusters
- Future quantum computing estimates

### 5. Cybersecurity Education
- Built-in rotating cybersecurity tips
- Password safety recommendations
- Real-world security awareness

### Additional Features
- Persistent activity logging
- Session tracking and summaries
- Animated hacker-style CLI interface
- Colourful terminal UI

---

## 🛠 Technologies Used

- Python 3
- `hashlib`
- `secrets`
- `urllib`
- `re`
- `json`
- ANSI terminal styling

---

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/CipherSafe.git
cd CipherSafe
python3 CipherSafe.py
