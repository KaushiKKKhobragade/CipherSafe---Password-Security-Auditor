"""
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │    OPERATOR  :  KaushiK aka Kira                             │
  │    CLEARANCE :  ██████████ MAXIMUM                           │
  │    LICENSE   :  MIT — Fork it, Clone it, Never Erase My Name.│
  │                                                              │
  │  > INITIALIZING CIPHERSAFE...                                │
  │  > LOADING ENCRYPTION PROTOCOLS...              [OK]         │
  │  > CONNECTING TO DARK WEB SCANNERS...           [OK]         │
  │  > BYPASSING FIREWALL...                        [OK]         │
  │  > ACCESS GRANTED ████████████████████ 100%                  │
  │                                                              │
  │              [ HACK THE PLANET. STAY SECURE. ]               │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
  
CipherSafe - Password Security Auditor

A terminal-based cybersecurity tool for password analysis, generation,
breach detection, and security education.

Features:
  1. Secure Password / Passphrase Generator  (cryptographic, with strength scores)
  2. Real-Time Dark Web Breach Check         (HaveIBeenPwned API, k-anonymity)
  3. Password Strength Analyser              (entropy, patterns, crack-time)
  4. Password Time Machine                   (crack time across computing eras)
  5. Security Tips & Education               (rotating cybersecurity facts)
  + Session summary on exit
  + Persistent activity log (ciphersafe_log.txt)
"""

import os
import re
import time
import random
import hashlib
import secrets
import string
import json
import platform
import urllib.request
import urllib.error
from datetime import datetime


# ─────────────────────────────────────────────
#  SESSION TRACKER  (global, updated throughout)
# ─────────────────────────────────────────────

class Session:
    """
    Tracks statistics for the current CipherSafe run.

    Attributes:
        start_time (datetime): When the session started.
        passwords_generated (int): Total passwords/passphrases generated.
        strength_checks (int): Total strength analyses performed.
        breaches_found (int): Number of breach-positive results this session.
        breach_checks (int): Total HIBP lookups performed.
        time_machine_runs (int): Times the Time Machine was used.
    """
    def __init__(self):
        self.start_time          = datetime.now()
        self.passwords_generated = 0
        self.strength_checks     = 0
        self.breaches_found      = 0
        self.breach_checks       = 0
        self.time_machine_runs   = 0

    def duration(self) -> str:
        """Return human-readable session duration."""
        secs = int((datetime.now() - self.start_time).total_seconds())
        if secs < 60:
            return f"{secs}s"
        return f"{secs // 60}m {secs % 60}s"


SESSION = Session()


# ─────────────────────────────────────────────
#  CYBERSECURITY TIPS
# ─────────────────────────────────────────────

SECURITY_TIPS = [
    ("Reuse = Disaster",
     "81% of data breaches are caused by weak or reused passwords.\n"
     "  Each account you own should have a unique, strong password."),

    ("Length > Complexity",
     "A 20-character lowercase passphrase is stronger than an 8-character\n"
     "  mixed-case password. Length multiplies cracking time exponentially."),

    ("2FA is Your Safety Net",
     "Two-factor authentication (2FA) blocks 99.9% of automated attacks\n"
     "  even if your password is leaked. Enable it everywhere you can."),

    ("Phishing > Brute Force",
     "Most passwords aren't cracked — they're stolen via phishing emails.\n"
     "  Always check the URL before entering your credentials."),

    ("Password Managers",
     "A password manager lets you use a unique 20-char password for every\n"
     "  site without memorising any of them. It's the #1 security upgrade."),

    ("Dictionary Attacks",
     "Attackers don't guess randomly — they use wordlists of billions of\n"
     "  real leaked passwords. 'P@ssw0rd' is on every list. Be unpredictable."),

    ("Breach Monitoring",
     "Data breaches happen constantly. Check haveibeenpwned.com regularly\n"
     "  and change passwords for any account that appears in a breach."),

    ("The 3-2-1 Rule",
     "For critical passwords: 3+ character types, 2+ special characters,\n"
     "  and 1 check against breach databases before using it."),

    ("Shoulder Surfing",
     "Be aware of who can see your screen in public. Attackers don't always\n"
     "  need software — sometimes they just need to look over your shoulder."),

    ("Social Engineering",
     "Your mother's maiden name, pet's name, and birthday are public on\n"
     "  social media. Never use personal information in passwords."),

    ("Session Hijacking",
     "Always log out on shared computers. Leaving sessions open lets the\n"
     "  next user access your accounts without needing your password."),

    ("Credential Stuffing",
     "When a site is breached, attackers try those exact credentials on\n"
     "  500+ other sites automatically. Unique passwords per site stop this."),
]

LOG_FILE = "ciphersafe_log.txt"


# ─────────────────────────────────────────────
#  COLOUR & TERMINAL HELPERS
# ─────────────────────────────────────────────

class Colour:
    """ANSI colour codes for terminal styling."""
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


def c(colour, text):
    """Wrap text in a colour code."""
    return f"{colour}{text}{Colour.RESET}"


def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.018):
    """Print text character by character for a hacker aesthetic."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def glitch_print(text, colour=Colour.GREEN):
    """
    Print text with a brief glitch animation effect —
    shows scrambled characters then resolves to the real text.
    """
    glitch_chars = "!@#$%^&*<>?/\\|~`"
    width = len(text)
    for _ in range(5):
        scrambled = "".join(
            random.choice(glitch_chars) if random.random() < 0.5 else ch
            for ch in text
        )
        print(f"\r{colour}{scrambled}{Colour.RESET}", end="", flush=True)
        time.sleep(0.06)
    print(f"\r{colour}{text}{Colour.RESET}")


def type_line(text, colour=Colour.GREEN, delay=0.025):
    """Type out a single line with colour."""
    print(colour, end="")
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(Colour.RESET)


def bar(length=52, char="─"):
    """Print a decorative horizontal bar."""
    print(c(Colour.DIM, char * length))


def spinner(message, duration=1.5):
    """Display a spinner animation for a given duration."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{c(Colour.CYAN, frames[i % len(frames)])}  {message}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{c(Colour.GREEN, '✔')}  {message}          ")


# ─────────────────────────────────────────────
#  ASCII BANNER
# ─────────────────────────────────────────────

BANNER = r"""
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ███████╗ █████╗ ███████╗███████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝███████╗███████║█████╗  █████╗
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗╚════██║██╔══██║██╔══╝  ██╔══╝
╚██████╗██║██║     ██║  ██║███████╗██║  ██║███████║██║  ██║██║     ███████╗
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝
"""

TAGLINE = "[ Password Security Auditor ]"


def print_banner():
    """Print the animated CipherSafe banner, tagline, and a random security tip."""
    clear()
    lines = BANNER.strip("\n").split("\n")
    for line in lines:
        print(c(Colour.GREEN, line))
        time.sleep(0.04)
    time.sleep(0.2)
    glitch_print(TAGLINE.center(74), colour=Colour.CYAN)
    time.sleep(0.3)
    bar(74)
    _print_startup_tip()


def _print_startup_tip():
    """Display a random cybersecurity tip after the banner."""
    title, body = random.choice(SECURITY_TIPS)
    print()
    print(c(Colour.YELLOW, f"  [TIP]  {title}"))
    print(c(Colour.DIM,    f"  {body}"))
    print()
    bar(74)


# ─────────────────────────────────────────────
#  DATA — TOP 500 COMMON PASSWORDS (built-in)
# ─────────────────────────────────────────────

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "1234567",
    "1234567890", "qwerty", "abc123", "111111", "123123", "admin",
    "letmein", "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "shadow", "superman", "michael", "football", "password1",
    "iloveyou", "1234", "batman", "passw0rd", "qwerty123", "000000",
    "654321", "555555", "666666", "777777", "888888", "999999",
    "121212", "112233", "password123", "password!", "pa$$word",
    "pass@123", "hello123", "test1234", "changeme", "secret",
    "qwertyuiop", "asdfghjkl", "zxcvbnm", "1q2w3e4r", "q1w2e3r4",
    "abc123!", "abcdef", "123qwe", "mypassword", "trustno1",
    "hunter2", "starwars", "charlie", "donald", "baseball",
    "ashley", "bailey", "jessica", "letmein1", "access",
    "matrix", "google", "apple", "samsung", "internet",
    "login", "admin123", "root", "toor", "user",
    "1111111111", "00000000", "123321", "pass", "test",
    "hello", "love", "ninja", "mustang", "password2",
}


# ─────────────────────────────────────────────
#  PASSWORD CLASS
# ─────────────────────────────────────────────

class Password:
    """
    Represents a password and provides analysis methods.

    Attributes:
        raw (str): The plain-text password.
    """

    def __init__(self, raw: str):
        self.raw = raw

    # ── Strength Analysis ──────────────────────

    def length_score(self) -> int:
        """Score based on character length (0–35)."""
        l = len(self.raw)
        if l >= 24: return 35
        if l >= 20: return 30
        if l >= 16: return 25
        if l >= 12: return 18
        if l >= 10: return 12
        if l >= 8:  return 7
        if l >= 6:  return 3
        return 0

    def variety_score(self) -> int:
        """Score based on character variety (0–40)."""
        score = 0
        if re.search(r"[a-z]", self.raw): score += 8
        if re.search(r"[A-Z]", self.raw): score += 8
        if re.search(r"\d",    self.raw): score += 8
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", self.raw): score += 16
        # Bonus: uses MULTIPLE special characters
        if len(re.findall(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", self.raw)) >= 2:
            score += 5
        # Bonus: mixes upper and lower throughout (not just capitalised first char)
        if re.search(r"[a-z]", self.raw) and re.search(r"[A-Z]", self.raw):
            if not re.match(r"^[A-Z][a-z]+$", self.raw):
                score += 3
        return min(score, 40)

    def pattern_penalty(self) -> int:
        """Deduct points for predictable patterns (0–40 penalty)."""
        penalty = 0
        # keyboard walks
        walks = ["qwerty", "asdfgh", "zxcvbn", "qazwsx", "12345", "09876",
                 "abcdef", "abcabc", "aaaaaa", "zzzzzz"]
        for w in walks:
            if w in self.raw.lower():
                penalty += 15

        # repeated characters (aaa, 111)
        if re.search(r"(.)\1{2,}", self.raw):
            penalty += 10

        # sequential digits
        if re.search(r"(012|123|234|345|456|567|678|789|890)", self.raw):
            penalty += 8

        # sequential letters
        if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)", self.raw.lower()):
            penalty += 8

        # common substitutions that don't help (p@ssw0rd style)
        leet = self.raw.lower()
        for a, b in [("@","a"),("0","o"),("1","i"),("3","e"),("$","s"),("!","i")]:
            leet = leet.replace(a, b)
        if leet in COMMON_PASSWORDS:
            penalty += 20

        # year patterns (1990–2029)
        if re.search(r"(19[0-9]{2}|20[0-2][0-9])", self.raw):
            penalty += 6

        # starts/ends with digit only
        if re.match(r"^\d+", self.raw) and re.search(r"\d+$", self.raw):
            if not re.search(r"[a-zA-Z!@#$%^&*]", self.raw[2:-2] or self.raw):
                penalty += 5

        return min(penalty, 40)

    def total_score(self) -> int:
        """Compute overall strength score (0–100)."""
        # Hard override: if in common list, cap at 5
        if self.is_common():
            return 5
        score = self.length_score() + self.variety_score() - self.pattern_penalty()
        return max(0, min(score, 100))

    def strength_label(self) -> tuple:
        """Return (label, colour) based on score."""
        score = self.total_score()
        if score >= 85: return ("VERY STRONG 🔒", Colour.GREEN)
        if score >= 65: return ("STRONG",          Colour.CYAN)
        if score >= 45: return ("MODERATE ⚠",      Colour.YELLOW)
        if score >= 25: return ("WEAK",             Colour.RED)
        return ("CRITICAL ☠",   Colour.RED)

    def feedback(self) -> list:
        """Return a prioritised list of improvement suggestions."""
        tips = []
        if self.is_common():
            tips.append("This is one of the most common passwords in the world — change it immediately")
        if len(self.raw) < 8:
            tips.append("Password is dangerously short — use at least 12 characters")
        elif len(self.raw) < 12:
            tips.append("Use at least 12 characters (16+ is ideal for high-security accounts)")
        if not re.search(r"[A-Z]", self.raw):
            tips.append("Add uppercase letters (A–Z)")
        if not re.search(r"[a-z]", self.raw):
            tips.append("Add lowercase letters (a–z)")
        if not re.search(r"\d", self.raw):
            tips.append("Add numbers (0–9)")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", self.raw):
            tips.append("Add special characters (!@#$%^&*...)")
        elif len(re.findall(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", self.raw)) < 2:
            tips.append("Use 2+ different special characters for extra strength")
        if re.search(r"(.)\1{2,}", self.raw):
            tips.append("Avoid repeated characters (e.g. 'aaa', '111', '???')")
        if any(w in self.raw.lower() for w in ["qwerty", "asdfgh", "zxcvbn", "12345", "abcdef"]):
            tips.append("Avoid keyboard walks or sequential patterns (qwerty, asdf, 12345...)")
        if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij)", self.raw.lower()):
            tips.append("Avoid sequential letter patterns (abc, def, ghi...)")
        if re.search(r"(19[0-9]{2}|20[0-2][0-9])", self.raw):
            tips.append("Avoid using years — attackers always try birth years and graduation years")
        # Check leet substitution
        leet = self.raw.lower()
        for a, b in [("@","a"),("0","o"),("1","i"),("3","e"),("$","s"),("!","i")]:
            leet = leet.replace(a, b)
        if leet in COMMON_PASSWORDS:
            tips.append("Simple letter substitutions (@ for a, 0 for o) are well-known to attackers")
        if re.match(r"^[A-Z][a-z]+\d+$", self.raw):
            tips.append("Avoid 'Word + Numbers' format (e.g. Tiger123) — very easy to crack")
        return tips

    # ── Breach Detection ───────────────────────

    def sha1_hash(self) -> str:
        """Return the SHA-1 hex digest of the password (used for HIBP-style checks)."""
        return hashlib.sha1(self.raw.encode("utf-8")).hexdigest().upper()

    def is_common(self) -> bool:
        """Check if password appears in the built-in common-password list."""
        return self.raw.lower() in COMMON_PASSWORDS

    def hibp_breach_check(self) -> dict:
        """
        Check password against the HaveIBeenPwned database in real time.

        Uses the k-anonymity model:
          1. SHA-1 hash the password locally.
          2. Send only the first 5 hex characters to the HIBP API.
          3. HIBP returns all hash suffixes that share that prefix.
          4. We search the returned list locally — the full hash never leaves the machine.

        This checks against 14+ billion real passwords leaked from dark web breaches.

        Returns:
            dict with keys:
                'found'  (bool)  — whether the password was found in a breach
                'count'  (int)   — number of times it appeared across all breaches
                'source' (str)   — 'hibp_live', 'hibp_offline_fallback', or 'error'
                'error'  (str)   — error message if something went wrong (optional)
        """
        sha1   = self.sha1_hash()          # full 40-char uppercase hex
        prefix = sha1[:5]
        suffix = sha1[5:]

        url     = f"https://api.pwnedpasswords.com/range/{prefix}"
        headers = {
            "User-Agent":     "CipherSafe-COMP9001/1.0",
            "Add-Padding":    "true",   # prevents traffic analysis via response size
        }

        try:
            req      = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                body = response.read().decode("utf-8")

            # Each line: "SUFFIX:COUNT"  (padding lines have count 0)
            for line in body.splitlines():
                parts = line.strip().split(":")
                if len(parts) != 2:
                    continue
                returned_suffix, count_str = parts
                if returned_suffix.upper() == suffix.upper():
                    count = int(count_str)
                    if count == 0:
                        # Padding entry — not a real breach hit
                        break
                    return {"found": True, "count": count, "source": "hibp_live"}

            return {"found": False, "count": 0, "source": "hibp_live"}

        except urllib.error.URLError as e:
            # Network unavailable — fall back to local common-password check
            return self._offline_fallback(reason=str(e))
        except Exception as e:
            return self._offline_fallback(reason=str(e))

    def _offline_fallback(self, reason: str = "") -> dict:
        """
        Offline fallback used when the HIBP API is unreachable.
        Checks against the built-in common-password list only.

        Returns a result dict tagged with source='hibp_offline_fallback'.
        """
        if self.is_common():
            return {
                "found":  True,
                "count":  0,          # real count unknown offline
                "source": "hibp_offline_fallback",
                "error":  reason,
            }
        return {
            "found":  False,
            "count":  0,
            "source": "hibp_offline_fallback",
            "error":  reason,
        }

    def entropy_bits(self) -> float:
        """
        Estimate password entropy in bits.
        entropy = log2(charset_size ^ length)
        Uses char_diversity_score() (recursive) to determine charset size.
        """
        import math
        charset = self._charset_size()
        if charset == 0:
            return 0.0
        return round(len(self.raw) * math.log2(charset), 2)

    def _charset_size(self) -> int:
        """Return the effective character-set size based on character types used."""
        charset = 0
        if re.search(r"[a-z]", self.raw): charset += 26
        if re.search(r"[A-Z]", self.raw): charset += 26
        if re.search(r"\d",    self.raw): charset += 10
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", self.raw): charset += 32
        return charset

    def char_diversity_score(self, index: int = 0, found: set = None) -> set:
        """
        Recursively walk the password character by character, building a set
        of all unique character categories found.

        This uses RECURSION (Week 11 advanced topic): the method calls itself
        with index+1 until it reaches the end of the password string.

        Args:
            index (int): Current character position (starts at 0).
            found (set): Accumulator set of category strings found so far.

        Returns:
            set: All character categories present in the password.
                 Possible values: 'lower', 'upper', 'digit', 'special'
        """
        if found is None:
            found = set()

        # Base case — we have processed every character
        if index >= len(self.raw):
            return found

        ch = self.raw[index]

        # Classify this character and add to the found set
        if ch.islower():
            found.add("lower")
        elif ch.isupper():
            found.add("upper")
        elif ch.isdigit():
            found.add("digit")
        else:
            found.add("special")

        # Recursive case — process the next character
        return self.char_diversity_score(index + 1, found)

    def strength_matrix(self) -> list:
        """
        Build a 2D list (multi-dimensional array) representing the full
        strength profile of this password.

        This uses a MULTI-DIMENSIONAL ARRAY (Week 12 advanced topic):
        each row is [criterion, status_bool, detail_string].

        Returns:
            list[list]: A 2D matrix where each row is:
                        [criterion_name (str),
                         passed (bool),
                         detail (str)]
        """
        special_pat = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]"
        leet = self.raw.lower()
        for a, b in [("@","a"),("0","o"),("1","i"),("3","e"),("$","s"),("!","i")]:
            leet = leet.replace(a, b)

        # 2D list — each inner list is [name, passed, detail]
        matrix = [
            ["Length >= 8",         len(self.raw) >= 8,
             f"{len(self.raw)} characters"],
            ["Length >= 12",        len(self.raw) >= 12,
             "recommended minimum"],
            ["Length >= 16",        len(self.raw) >= 16,
             "highly recommended"],
            ["Lowercase letters",   bool(re.search(r"[a-z]", self.raw)),
             f"{len(re.findall(r'[a-z]', self.raw))} found"],
            ["Uppercase letters",   bool(re.search(r"[A-Z]", self.raw)),
             f"{len(re.findall(r'[A-Z]', self.raw))} found"],
            ["Digits",              bool(re.search(r"\d", self.raw)),
             f"{len(re.findall(r'[0-9]', self.raw))} found"],
            ["Special characters",  bool(re.search(special_pat, self.raw)),
             f"{len(re.findall(special_pat, self.raw))} found"],
            ["No repeated chars",   not bool(re.search(r"(.)\1{2,}", self.raw)),
             "e.g. aaa / 111"],
            ["No keyboard walks",   not any(w in self.raw.lower()
             for w in ["qwerty","asdfgh","zxcvbn","12345","abcdef"]),
             "e.g. qwerty / 12345"],
            ["No year pattern",     not bool(re.search(
             r"(19[0-9]{2}|20[0-2][0-9])", self.raw)),
             "e.g. 1998 / 2023"],
            ["Not a common password", not self.is_common(),
             "checked against known list"],
            ["No leet substitution", leet not in COMMON_PASSWORDS,
             "e.g. p@ssw0rd"],
        ]
        return matrix

    def crack_time_estimate(self) -> str:
        """
        Estimate time to crack via brute force at 10 billion guesses/sec
        (modern GPU benchmark).
        """
        import math
        charset = self._charset_size()
        if charset == 0:
            return "instantly"

        combinations = charset ** len(self.raw)
        guesses_per_sec = 10_000_000_000  # 10B/s GPU attack

        seconds = combinations / guesses_per_sec

        if seconds < 1:        return c(Colour.RED,    "instantly")
        if seconds < 60:       return c(Colour.RED,    f"{int(seconds)} seconds")
        if seconds < 3600:     return c(Colour.RED,    f"{int(seconds/60)} minutes")
        if seconds < 86400:    return c(Colour.YELLOW,  f"{int(seconds/3600)} hours")
        if seconds < 2_592_000: return c(Colour.YELLOW, f"{int(seconds/86400)} days")
        if seconds < 31_536_000: return c(Colour.CYAN, f"{int(seconds/2_592_000)} months")
        years = seconds / 31_536_000
        if years < 1_000:      return c(Colour.GREEN,  f"{int(years)} years")
        if years < 1_000_000:  return c(Colour.GREEN,  f"{int(years/1000)}K years")
        return c(Colour.GREEN, "millions of years 🔒")


# ─────────────────────────────────────────────
#  FEATURE 1 — PASSWORD GENERATOR
# ─────────────────────────────────────────────

WORD_LIST = [
    "silver", "falcon", "ocean", "tiger", "ember", "storm", "viper",
    "lunar", "ghost", "cobalt", "cedar", "raven", "arctic", "blaze",
    "cipher", "dagger", "echo", "frost", "gravel", "haven", "iron",
    "jade", "knight", "lotus", "marble", "nebula", "onyx", "phantom",
    "quartz", "ridge", "shadow", "thunder", "ultra", "void", "wolf",
    "xenon", "yellow", "zenith", "alpha", "beta", "delta", "gamma",
    "prism", "spiral", "tundra", "basalt", "comet", "draco", "flint",
]


def generate_password(length=16, use_upper=True, use_digits=True, use_symbols=True) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length (int): Desired password length.
        use_upper (bool): Include uppercase letters.
        use_digits (bool): Include digits.
        use_symbols (bool): Include special characters.

    Returns:
        str: Generated password.
    """
    pool = string.ascii_lowercase
    required = [secrets.choice(string.ascii_lowercase)]

    if use_upper:
        pool += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        pool += string.digits
        required.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += symbols
        required.append(secrets.choice(symbols))

    remaining = [secrets.choice(pool) for _ in range(length - len(required))]
    combined  = required + remaining
    secrets.SystemRandom().shuffle(combined)
    return "".join(combined)


def generate_passphrase(num_words=4) -> str:
    """
    Generate a memorable passphrase from random words with a separator digit.

    Args:
        num_words (int): Number of words to combine.

    Returns:
        str: Generated passphrase.
    """
    words = [secrets.choice(WORD_LIST).capitalize() for _ in range(num_words)]
    sep   = secrets.choice(["@", "#", "!", "-", "_"])
    num   = str(secrets.randbelow(900) + 100)
    return sep.join(words) + sep + num


def _copy_hint(pwd: str):
    """Print the platform-specific copy-to-clipboard command."""
    sys = platform.system()
    print()
    print(c(Colour.WHITE, "  Copy to clipboard:"))
    if sys == "Darwin":
        print(c(Colour.DIM, f'  echo -n "{pwd}" | pbcopy'))
        print(c(Colour.DIM,  "  (macOS — paste with Cmd+V)"))
    elif sys == "Windows":
        print(c(Colour.DIM, f'  echo|set /p="{pwd}" | clip'))
        print(c(Colour.DIM,  "  (Windows — paste with Ctrl+V)"))
    else:
        print(c(Colour.DIM, f'  echo -n "{pwd}" | xclip -selection clipboard'))
        print(c(Colour.DIM,  "  (Linux — requires xclip)"))


def _print_gen_table(items: list, col_header: str, scores: list,
                     grades: list, cols: list):
    """
    Print a perfectly aligned generation table with dynamic column width.

    Args:
        items   : list of password/passphrase strings.
        col_header : 'PASSWORD' or 'PASSPHRASE'.
        scores  : matching list of int scores.
        grades  : matching list of grade strings.
        cols    : matching list of colour codes for score/grade.
    """
    # Column widths — PASSWORD col fits the longest entry exactly
    W_NUM  = 3                                  # " 1 "
    W_PWD  = max(len(col_header), max(len(p) for p in items)) + 2
    W_SCR  = max(len("SCORE"), 3) + 2           # " 100 "  → width 5+2=7
    W_GRD  = max(len("GRADE"), 2) + 2           # " A+ "   → width 2+2=4 → pad to 6
    W_GRD  = max(W_GRD, 6)

    B  = c(Colour.CYAN, "|")                    # border pipe

    def hline(l, m, r, fill):
        """One full horizontal rule."""
        return c(Colour.CYAN,
                 l +
                 fill * (W_NUM + 2) + m +
                 fill * (W_PWD + 2) + m +
                 fill * (W_SCR + 2) + m +
                 fill * (W_GRD + 2) + r)

    def row(num_str, pwd_str, scr_str, grd_str,
            num_col, pwd_col, scr_col, grd_col):
        return (
            B +
            c(num_col, f" {num_str.center(W_NUM)} ") + B +
            c(pwd_col, f" {pwd_str.ljust(W_PWD)} ") + B +
            c(scr_col, f" {scr_str.center(W_SCR)} ") + B +
            c(grd_col, f" {grd_str.center(W_GRD)} ") + B
        )

    # ── Top border ──
    print("  " + hline("+", "+", "+", "-"))

    # ── Header ──
    print("  " + row("#", col_header, "SCORE", "GRADE",
                      Colour.YELLOW, Colour.YELLOW,
                      Colour.YELLOW, Colour.YELLOW))

    # ── Header separator (double) ──
    print("  " + hline("+", "+", "+", "="))

    # ── Data rows ──
    for i, (pwd, score, grade, col) in enumerate(zip(items, scores, grades, cols)):
        print("  " + row(str(i + 1), pwd, str(score), grade,
                          Colour.DIM, Colour.WHITE, col, col))
        if i < len(items) - 1:
            print("  " + hline("|", "+", "|", "-"))

    # ── Bottom border ──
    print("  " + hline("+", "+", "+", "-"))


def feature_generate():
    """
    Interactive password / passphrase generator.
    Generates 5 options each with a live strength score and grade,
    in a perfectly aligned dynamic-width table.
    """
    bar(52)
    print(c(Colour.CYAN, Colour.BOLD + "  ⚡ SECURE PASSWORD GENERATOR"))
    bar(52)
    print()
    print(c(Colour.WHITE, "  Choose generation mode:"))
    print(c(Colour.YELLOW, "  [1]") + "  Random Password   (maximum entropy)")
    print(c(Colour.YELLOW, "  [2]") + "  Passphrase        (memorable + secure)")
    print()

    mode = input(c(Colour.GREEN, "  ▶ Select mode: ")).strip()

    if mode == "1":
        try:
            length = int(input(c(Colour.GREEN,
                "  ▶ Password length [default 16]: ")).strip() or "16")
            length = max(8, min(length, 128))
        except ValueError:
            length = 16

        print()
        spinner("Generating with cryptographic randomness...", 1.2)
        print()

        # Generate all 5 first so column width is known before printing
        items, scores, grades, cols = [], [], [], []
        for _ in range(5):
            pwd   = generate_password(length)
            p     = Password(pwd)
            score = p.total_score()
            _, col = p.strength_label()
            grade = ("A+" if score >= 85 else "A"  if score >= 75 else
                     "B"  if score >= 65 else "C"  if score >= 45 else "D")
            items.append(pwd)
            scores.append(score)
            grades.append(grade)
            cols.append(col)

        _print_gen_table(items, "PASSWORD", scores, grades, cols)

        SESSION.passwords_generated += 5
        _log_event("GENERATE", f"Generated 5 passwords  length={length}")

        best = max(items, key=lambda p: Password(p).total_score())
        _copy_hint(best)

    elif mode == "2":
        try:
            num_words = int(input(c(Colour.GREEN,
                "  ▶ Number of words [default 4]: ")).strip() or "4")
            num_words = max(3, min(num_words, 8))
        except ValueError:
            num_words = 4

        print()
        spinner("Picking words from the vault...", 1.0)
        print()

        items, scores, grades, cols = [], [], [], []
        for _ in range(5):
            phrase = generate_passphrase(num_words)
            p      = Password(phrase)
            score  = p.total_score()
            _, col = p.strength_label()
            grade  = ("A+" if score >= 85 else "A"  if score >= 75 else
                      "B"  if score >= 65 else "C"  if score >= 45 else "D")
            items.append(phrase)
            scores.append(score)
            grades.append(grade)
            cols.append(col)

        _print_gen_table(items, "PASSPHRASE", scores, grades, cols)

        SESSION.passwords_generated += 5
        _log_event("GENERATE", f"Generated 5 passphrases  words={num_words}")

        best = max(items, key=lambda p: Password(p).total_score())
        _copy_hint(best)

    else:
        print(c(Colour.RED, "  Invalid option."))
        return

    print()
    print(c(Colour.DIM, "  All passwords generated using Python's secrets module"))
    print(c(Colour.DIM, "  (cryptographically secure random — safe for real use)."))
    print()


# ─────────────────────────────────────────────
#  FEATURE 2 — DARK WEB BREACH CHECK
# ─────────────────────────────────────────────

def feature_breach():
    """
    Real-time dark web breach check using the HaveIBeenPwned (HIBP) API.

    Implements the k-anonymity model:
      - SHA-1 hash is computed locally.
      - Only the first 5 hex chars of the hash are sent to HIBP.
      - HIBP returns all matching hash suffixes and breach counts.
      - The full password and full hash never leave this machine.
    """
    bar(52)
    print(c(Colour.CYAN, Colour.BOLD + "  🕷  DARK WEB BREACH SCANNER"))
    print(c(Colour.DIM,  "      Powered by HaveIBeenPwned · 14B+ leaked passwords"))
    bar(52)
    print()

    # ── Privacy notice ──
    print(c(Colour.WHITE,  "  How your privacy is protected:"))
    print(c(Colour.DIM,    "  1. Your password is hashed with SHA-1 locally."))
    print(c(Colour.DIM,    "  2. Only the first 5 characters of that hash are sent."))
    print(c(Colour.DIM,    "  3. HIBP returns ~500 possible matches — we search locally."))
    print(c(Colour.DIM,    "  4. Your actual password never leaves your computer."))
    print()
    print(c(Colour.DIM, "  ─" * 26))
    print()

    # ── Support bulk checking ──
    print(c(Colour.WHITE, "  Check mode:"))
    print(c(Colour.YELLOW, "  [1]") + "  Check a single password")
    print(c(Colour.YELLOW, "  [2]") + "  Bulk check — check multiple passwords at once")
    print()
    mode = input(c(Colour.GREEN, "  ▶ Select mode [1/2]: ")).strip()
    print()

    if mode == "2":
        _breach_bulk()
    else:
        _breach_single()


def _breach_single():
    """Check one password against HIBP live."""
    pwd_input = input(c(Colour.GREEN, "  ▶ Enter password to check: ")).strip()
    if not pwd_input:
        print(c(Colour.RED, "  No password entered."))
        return

    pwd = Password(pwd_input)
    h   = pwd.sha1_hash()

    # ── Hash Details box ──
    # Strategy: build every content string as plain text first,
    # measure its length, then apply colour. The box width = longest line.
    title_plain = "  Hash Details"
    sha_plain   = f"  SHA-1       :  {h}"
    sent_plain  = f"  Sent to API :  {h[:5]} {'*' * 35}"
    W           = max(len(title_plain), len(sha_plain), len(sent_plain)) + 2

    def hbox_line(plain_text, colour_fn=None):
        """
        Print one content row of the hash box.
        plain_text  — the raw string with no ANSI codes.
        colour_fn   — optional callable(plain_text) -> coloured string.
        The padding is computed from the plain length so the right | is exact.
        """
        pad     = " " * (W - len(plain_text))
        content = colour_fn(plain_text) if colour_fn else plain_text
        print(c(Colour.CYAN, "  |") + content + pad + c(Colour.CYAN, "|"))

    print()
    print(c(Colour.CYAN, "  +" + "-" * W + "+"))

    # Title row — yellow
    hbox_line(title_plain, lambda t: c(Colour.YELLOW, t))

    print(c(Colour.CYAN, "  |" + "-" * W + "|"))

    # SHA-1 row — prefix dim, first 5 chars of hash yellow, rest dim
    pad_sha = " " * (W - len(sha_plain))
    print(c(Colour.CYAN, "  |") +
          c(Colour.DIM,    "  SHA-1       :  ") +
          c(Colour.YELLOW, h[:5]) +
          c(Colour.DIM,    h[5:]) +
          pad_sha + c(Colour.CYAN, "|"))

    # Sent row — prefix dim, first 5 chars yellow, stars dim
    pad_sent = " " * (W - len(sent_plain))
    print(c(Colour.CYAN, "  |") +
          c(Colour.DIM,    "  Sent to API :  ") +
          c(Colour.YELLOW, h[:5]) +
          c(Colour.DIM,    " " + "*" * 35) +
          pad_sent + c(Colour.CYAN, "|"))

    print(c(Colour.CYAN, "  +" + "-" * W + "+"))
    print()

    spinner("Connecting to HaveIBeenPwned API...", 1.0)
    spinner("Fetching breach hash range...", 1.2)
    spinner("Scanning 14 billion leaked records...", 1.0)
    print()

    result = pwd.hibp_breach_check()

    # ── Session + log update ──
    SESSION.breach_checks += 1
    if result["found"]:
        SESSION.breaches_found += 1
    _log_event("BREACH_CHECK",
               f"source={result.get('source','?')}  "
               f"found={result['found']}  "
               f"count={result.get('count', 0)}")
    _print_breach_result(result, pwd_input)


def _breach_bulk():
    """Check multiple passwords from user input against HIBP."""
    print(c(Colour.WHITE,  "  Enter passwords one per line."))
    print(c(Colour.DIM,    "  Type 'done' on a new line when finished."))
    print()

    passwords = []
    while True:
        entry = input(c(Colour.GREEN, f"  Password {len(passwords)+1}: ")).strip()
        if entry.lower() == "done":
            break
        if entry:
            passwords.append(entry)
        if len(passwords) >= 20:
            print(c(Colour.YELLOW, "  (Max 20 passwords per bulk check)"))
            break

    if not passwords:
        print(c(Colour.RED, "  No passwords entered."))
        return

    print()
    bar(52)
    print(c(Colour.WHITE, f"  Checking {len(passwords)} password(s) against HIBP..."))
    bar(52)
    print()

    breached_count = 0
    results_log    = []

    for i, pwd_input in enumerate(passwords, 1):
        pwd    = Password(pwd_input)
        h      = pwd.sha1_hash()
        masked = pwd_input[:2] + "*" * max(0, len(pwd_input) - 4) + pwd_input[-2:] \
                 if len(pwd_input) > 4 else "****"

        print(f"  {c(Colour.DIM, f'[{i}/{len(passwords)}]')}  Checking {c(Colour.WHITE, masked)} ...", end="", flush=True)
        time.sleep(0.3)   # brief pause between API calls to respect rate limits

        result = pwd.hibp_breach_check()

        if result["found"]:
            breached_count += 1
            count_str = f"{result['count']:,}" if result["count"] else "unknown count"
            print(f"  {c(Colour.RED, '⚠  BREACHED')}  ({count_str} times)")
        else:
            print(f"  {c(Colour.GREEN, '✔  SAFE')}")

        results_log.append({
            "password_masked": masked,
            "breached":        result["found"],
            "count":           result.get("count", 0),
            "source":          result.get("source", ""),
        })

    # ── Session update ──
    SESSION.breach_checks  += len(passwords)
    SESSION.breaches_found += breached_count
    _log_event("BULK_BREACH", f"checked={len(passwords)}  breached={breached_count}")

    print()
    bar(52)

    if breached_count == 0:
        print(c(Colour.GREEN, f"  ✔  All {len(passwords)} passwords are clean — not found in any breach."))
    else:
        print(c(Colour.RED, f"  ⚠  {breached_count} of {len(passwords)} passwords were found in breaches!"))
        print(c(Colour.YELLOW, "  → Change breached passwords immediately and enable 2FA."))

    print()

    # Offer to save bulk report
    save = input(c(Colour.GREEN, "  ▶ Save bulk report to file? (y/n): ")).strip().lower()
    if save == "y":
        filename = f"ciphersafe_bulk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, "w") as f:
                json.dump({
                    "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_checked":   len(passwords),
                    "breached":        breached_count,
                    "results":         results_log,
                }, f, indent=2)
            print(c(Colour.GREEN, f"\n  ✔  Bulk report saved: {filename}"))
        except IOError as e:
            print(c(Colour.RED, f"\n  ✘  Could not save: {e}"))
    print()


def _print_breach_result(result: dict, pwd_input: str):
    """Pretty-print the result of a single HIBP breach check."""

    # ── Source badge ──
    if result.get("source") == "hibp_live":
        src_badge = c(Colour.GREEN, "● LIVE")
        src_note  = "Data sourced live from HaveIBeenPwned (haveibeenpwned.com)"
    elif result.get("source") == "hibp_offline_fallback":
        src_badge = c(Colour.YELLOW, "● OFFLINE FALLBACK")
        src_note  = f"API unreachable — used local list only.  ({result.get('error', '')})"
    else:
        src_badge = c(Colour.DIM, "● UNKNOWN SOURCE")
        src_note  = ""

    print(f"  Source:  {src_badge}")
    if src_note:
        print(c(Colour.DIM, f"  {src_note}"))
    print()

    if result["found"]:
        count = result.get("count", 0)

        # Visual severity scale
        if count >= 1_000_000:
            severity = c(Colour.RED,    "CRITICAL  — Extremely Common Breach")
            bar_char  = "█"
            bar_col   = Colour.RED
        elif count >= 100_000:
            severity = c(Colour.RED,    "HIGH      — Very Widely Leaked")
            bar_char  = "▓"
            bar_col   = Colour.RED
        elif count >= 10_000:
            severity = c(Colour.YELLOW, "MEDIUM    — Commonly Leaked")
            bar_char  = "▒"
            bar_col   = Colour.YELLOW
        else:
            severity = c(Colour.YELLOW, "LOW       — Appeared in Some Breaches")
            bar_char  = "░"
            bar_col   = Colour.YELLOW

        # Exposure bar (max 20 chars, log scale)
        import math
        bar_len = min(20, max(1, int(math.log10(max(count, 1)) * 3)))
        exposure_bar = c(bar_col, bar_char * bar_len + "░" * (20 - bar_len))

        W_BOX       = 44
        bd_plain    = "  [!]  BREACH DETECTED!"
        bd_pad      = " " * (W_BOX - len(bd_plain))
        print(c(Colour.RED, "  +" + "=" * W_BOX + "+"))
        print(c(Colour.RED, "  |") +
              c(Colour.RED + Colour.BOLD, bd_plain) +
              bd_pad +
              c(Colour.RED, "|"))
        print(c(Colour.RED, "  +" + "=" * W_BOX + "+"))
        print()
        print(f"  Severity    :  {severity}")
        if count:
            print(f"  Seen        :  {c(Colour.RED, f'{count:,} times')}  across real data breaches")
        print(f"  Exposure    :  [{exposure_bar}]")
        print()
        print(c(Colour.YELLOW + Colour.BOLD, "  What you MUST do right now:"))
        print(c(Colour.YELLOW, "   [1]") + "  Change this password on EVERY site you use it on")
        print(c(Colour.YELLOW, "   [2]") + "  Enable two-factor authentication (2FA) everywhere")
        print(c(Colour.YELLOW, "   [3]") + "  Use CipherSafe option [1] to generate a secure replacement")
        print(c(Colour.YELLOW, "   [4]") + "  Check if your email was breached at haveibeenpwned.com")
        print()
        print(c(Colour.DIM, "  This password exists in real hacker wordlists and can be"))
        print(c(Colour.DIM, "  cracked near-instantly in any credential stuffing attack."))

    else:
        print(c(Colour.GREEN + Colour.BOLD, "  ✔  NOT FOUND in any known breach database."))
        print()
        print(c(Colour.GREEN,  "  This password has not appeared in any of the 14+ billion"))
        print(c(Colour.GREEN,  "  leaked credentials indexed by HaveIBeenPwned."))
        print()
        print(c(Colour.DIM,    "  This means it has not been leaked — not that it is strong."))
        print(c(Colour.DIM,    "  Run option [3] to check password strength as well."))

    print()


# ─────────────────────────────────────────────
#  FEATURE 3 — STRENGTH ANALYSER
# ─────────────────────────────────────────────

def draw_strength_bar(score: int) -> str:
    """Render a visual strength meter as a coloured bar."""
    filled = score // 5       # out of 20 blocks
    empty  = 20 - filled

    if score >= 80:   col = Colour.GREEN
    elif score >= 60: col = Colour.CYAN
    elif score >= 40: col = Colour.YELLOW
    else:             col = Colour.RED

    bar_str = c(col, "█" * filled) + c(Colour.DIM, "░" * empty)
    return f"  [{bar_str}]  {c(col, str(score) + '/100')}"


def feature_strength():
    """
    Comprehensive password strength analysis.
    Scores on length, character variety, entropy, patterns, and leet substitutions.
    Displays a visual strength meter, sub-score breakdown, detected weaknesses,
    and a prioritised improvement checklist.
    """
    bar(52)
    print(c(Colour.CYAN, Colour.BOLD + "  🔬 PASSWORD STRENGTH ANALYSER"))
    bar(52)
    print()

    pwd_input = input(c(Colour.GREEN, "  ▶ Enter password to analyse: ")).strip()
    if not pwd_input:
        print(c(Colour.RED, "  No password entered."))
        return

    pwd = Password(pwd_input)

    print()
    spinner("Scanning character composition...", 0.6)
    spinner("Checking entropy & pattern library...", 0.8)
    spinner("Calculating crack-time estimates...", 0.6)
    print()

    score       = pwd.total_score()
    label, col  = pwd.strength_label()

    # ── Grade letter ──
    if score >= 85:   grade = "A+"
    elif score >= 75: grade = "A"
    elif score >= 65: grade = "B"
    elif score >= 45: grade = "C"
    elif score >= 25: grade = "D"
    else:             grade = "F"

    # ── Overall banner ──
    # Strip emoji from label so len() is accurate (emoji = 1 byte but 2 cols wide)
    lbl_clean = (label.replace("🔒", "LOCKED").replace("⚠", "!")
                      .replace("☠", "!").strip())
    lbl_fixed = lbl_clean.ljust(12)   # pad to fixed width
    grd_fixed = grade.ljust(2)
    inner_plain = f"  STRENGTH: {lbl_fixed}   GRADE: {grd_fixed}  "
    W_BOX       = len(inner_plain)
    right_pad   = ""                   # already exact

    print(c(Colour.WHITE, "  +" + "=" * W_BOX + "+"))
    print(c(Colour.WHITE, "  |") +
          "  STRENGTH: " +
          c(col + Colour.BOLD, lbl_fixed) +
          "   GRADE: " +
          c(col + Colour.BOLD, grd_fixed) +
          "  " +
          c(Colour.WHITE, "|"))
    print(c(Colour.WHITE, "  +" + "=" * W_BOX + "+"))
    print()

    # ── Visual bar ──
    print(draw_strength_bar(score))
    print()

    # ── Sub-score breakdown ──
    bar(52)
    print(c(Colour.WHITE, "  SCORE BREAKDOWN"))
    bar(52)

    l_score  = pwd.length_score()
    v_score  = pwd.variety_score()
    p_penalty = pwd.pattern_penalty()

    def mini_bar(val, max_val, width=12):
        filled = int((val / max_val) * width)
        return c(Colour.CYAN, "▰" * filled) + c(Colour.DIM, "▱" * (width - filled))

    print(f"  {c(Colour.DIM, 'Length score'.ljust(20))}  {mini_bar(l_score, 35)}  {c(Colour.CYAN,   str(l_score).rjust(3))}/35")
    print(f"  {c(Colour.DIM, 'Variety score'.ljust(20))}  {mini_bar(v_score, 40)}  {c(Colour.CYAN,   str(v_score).rjust(3))}/40")
    print(f"  {c(Colour.RED,  'Pattern penalty'.ljust(20))}  {mini_bar(p_penalty, 40)}  {c(Colour.RED,  '-' + str(p_penalty).rjust(2))}/40")
    print()
    print(f"  {c(Colour.WHITE, 'Final score'.ljust(20))}  {'':12}   {c(col, Colour.BOLD + str(score).rjust(3))}/100")
    print()

    # ── Detailed attribute table — uses strength_matrix() 2D array (Week 12) ──
    bar(52)
    print(c(Colour.WHITE, "  CHARACTER ANALYSIS"))
    print(c(Colour.DIM,   "  (built from a 2D strength matrix — Week 12 advanced topic)"))
    bar(52)

    # strength_matrix() returns a 2D list: [[name, passed, detail], ...]
    matrix = pwd.strength_matrix()
    for row in matrix:
        name, passed, detail = row[0], row[1], row[2]
        tick       = c(Colour.GREEN, "✔") if passed else c(Colour.RED, "✘")
        detail_str = c(Colour.DIM, f"  {detail}") if detail else ""
        print(f"  {tick}  {c(Colour.WHITE, name.ljust(24))}{detail_str}")

    # ── Recursive character diversity (Week 11) ──
    print()
    diversity = pwd.char_diversity_score()   # recursive call
    cat_map   = {
        "lower":   c(Colour.CYAN,   "lowercase"),
        "upper":   c(Colour.YELLOW, "uppercase"),
        "digit":   c(Colour.GREEN,  "digits"),
        "special": c(Colour.MAGENTA,"special chars"),
    }
    found_str = "  ".join(cat_map[k] for k in sorted(diversity))
    print(c(Colour.DIM, "  Character categories found") +
          c(Colour.DIM, " (via recursive scan):"))
    print(f"  {found_str  or c(Colour.RED, 'none')}")
    print()

    # ── Entropy & crack time ──
    bar(52)
    print(c(Colour.WHITE, "  CRYPTOGRAPHIC METRICS"))
    bar(52)

    entropy = pwd.entropy_bits()
    crack   = pwd.crack_time_estimate()

    # Entropy quality label
    if entropy >= 80:   eq = c(Colour.GREEN, "Excellent")
    elif entropy >= 60: eq = c(Colour.CYAN,  "Good")
    elif entropy >= 40: eq = c(Colour.YELLOW,"Fair")
    else:               eq = c(Colour.RED,   "Poor")

    print(f"  {c(Colour.DIM, 'Entropy'.ljust(24))}  {c(Colour.CYAN, str(entropy) + ' bits')}  ({eq})")
    print(f"  {c(Colour.DIM, 'Crack time (GPU brute)'.ljust(24))}  {crack}")
    print(f"  {c(Colour.DIM, 'Password length'.ljust(24))}  {c(Colour.WHITE, str(len(pwd_input)) + ' characters')}")

    # Unique character ratio
    unique_ratio = round(len(set(pwd_input)) / len(pwd_input) * 100)
    ur_col = Colour.GREEN if unique_ratio >= 80 else (Colour.YELLOW if unique_ratio >= 60 else Colour.RED)
    print(f"  {c(Colour.DIM, 'Unique char ratio'.ljust(24))}  {c(ur_col, str(unique_ratio) + '%')}")
    print()

    # ── Pattern warnings ──
    warnings = []
    if re.search(r"(.)\1{2,}", pwd_input):
        warnings.append(("Repeated characters detected",        "e.g. 'aaa', '111' — easy to guess"))
    if any(w in pwd_input.lower() for w in ["qwerty","asdfgh","zxcvbn","12345","abcdef"]):
        warnings.append(("Keyboard walk / sequence detected",   "attackers try these first"))
    if re.search(r"(19[0-9]{2}|20[0-2][0-9])", pwd_input):
        warnings.append(("Year pattern detected",               "years are high-priority targets"))
    if re.match(r"^[A-Z][a-z]+\d+$", pwd_input):
        warnings.append(("Word+Number format detected",         "e.g. Tiger123 — very common pattern"))
    leet = pwd_input.lower()
    for a, b in [("@","a"),("0","o"),("1","i"),("3","e"),("$","s"),("!","i")]:
        leet = leet.replace(a, b)
    if leet in COMMON_PASSWORDS:
        warnings.append(("Leet substitution of common word",    "p@ssw0rd is as weak as password"))
    if pwd.is_common():
        warnings.append(("Listed in top common passwords",      "immediately change this password"))

    if warnings:
        bar(52)
        print(c(Colour.RED, "  ⚠  WEAKNESSES DETECTED"))
        bar(52)
        for title, detail in warnings:
            print(f"  {c(Colour.RED, '✘')}  {c(Colour.WHITE, title)}")
            print(f"       {c(Colour.DIM, detail)}")
        print()

    # ── Improvement tips ──
    tips = pwd.feedback()
    if tips:
        bar(52)
        print(c(Colour.YELLOW, "  RECOMMENDATIONS  (in priority order)"))
        bar(52)
        for i, tip in enumerate(tips, 1):
            print(f"  {c(Colour.YELLOW, str(i) + '.')}  {tip}")
        print()
    else:
        print(c(Colour.GREEN, "  ✔  No improvements needed — this is an excellent password!"))
        print()

    # ── Session + log ──
    SESSION.strength_checks += 1
    _log_event("STRENGTH", f"score={score}  grade={'A+' if score>=85 else 'A' if score>=75 else 'B' if score>=65 else 'C' if score>=45 else 'D'}  length={len(pwd_input)}")

    # ── Save option ──
    save = input(c(Colour.GREEN, "  ▶ Save this report to file? (y/n): ")).strip().lower()
    if save == "y":
        save_report(pwd_input, score, label, pwd)


# ─────────────────────────────────────────────
#  UNIQUE FEATURE — PASSWORD TIME MACHINE
# ─────────────────────────────────────────────

def feature_time_machine():
    """
    THE UNIQUE FEATURE: Password Time Machine
    Shows how long a password would have taken to crack in different eras of computing,
    from 1980s to modern quantum computers — giving users a historical perspective
    on why password complexity matters.
    """
    bar(52)
    print(c(Colour.MAGENTA, Colour.BOLD + "  ⏳ PASSWORD TIME MACHINE"))
    bar(52)
    print()
    print(c(Colour.DIM, "  See how long it would take to crack your password"))
    print(c(Colour.DIM, "  across different eras of computing history."))
    print()

    pwd_input = input(c(Colour.GREEN, "  ▶ Enter password: ")).strip()
    if not pwd_input:
        print(c(Colour.RED, "  No password entered."))
        return

    import math
    pwd = Password(pwd_input)

    charset = 0
    if re.search(r"[a-z]", pwd_input): charset += 26
    if re.search(r"[A-Z]", pwd_input): charset += 26
    if re.search(r"\d",    pwd_input): charset += 10
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", pwd_input): charset += 32
    if charset == 0:
        print(c(Colour.RED, "  Cannot analyse this password."))
        return

    combinations = charset ** len(pwd_input)

    # Guesses per second for each era — tags kept to max 5 chars, names max 22 chars
    eras = [
        ("1980s  - Apple II",      1,              "[>_] "),
        ("1990s  - Pentium PC",    1_000_000,      "[PC]  "),
        ("2000s  - Dual-Core",     100_000_000,    "[DC]  "),
        ("2010s  - GPU Cluster",   1_000_000_000,  "[GPU] "),
        ("2020s  - RTX 4090",      10_000_000_000, "[RTX] "),
        ("2030s+ - Quantum",       10**15,         "[QTM] "),
    ]

    print()
    spinner("Travelling through time...", 1.5)
    print()

    # ── Password info card (fixed 60-char inner width, no emoji) ──
    masked = pwd_input[:2] + "*" * max(0, len(pwd_input) - 4) + pwd_input[-2:] \
             if len(pwd_input) > 4 else "****"
    inner  = 60

    def info_line(text):
        """Print a fixed-width info card line."""
        padded = text.ljust(inner)
        print(c(Colour.CYAN, "  |") + c(Colour.WHITE, "  " + padded) + c(Colour.CYAN, "|"))

    print(c(Colour.CYAN, "  +" + "-" * (inner + 2) + "+"))
    info_line(f"Password    : {masked}")
    line2 = (f"Length: {len(pwd_input)} chars    "
             f"Charset: {charset}    "
             f"Combinations: ~{combinations:.2e}")
    info_line(line2)
    print(c(Colour.CYAN, "  +" + "-" * (inner + 2) + "+"))
    print()

    # ── Table dimensions (all plain chars, no emoji) ──
    # Columns:   | # | ERA - DEVICE          | SPEED          | CRACK TIME           |
    W_NUM   = 3
    W_ERA   = 29
    W_SPEED = 14
    W_TIME  = 26

    def hline(left, mid, right, fill="="):
        """Build one horizontal border line."""
        seg = fill * (W_NUM + 2)
        return (
            c(Colour.MAGENTA,
              left +
              seg + mid +
              fill * (W_ERA   + 2) + mid +
              fill * (W_SPEED + 2) + mid +
              fill * (W_TIME  + 2) +
              right)
        )

    def data_row(num, era, speed, crack_time, time_col):
        """Build one data row with correct fixed-width padding."""
        B = c(Colour.MAGENTA, "|")
        return (
            B +
            c(Colour.DIM,    f" {str(num).center(W_NUM)} ") + B +
            c(Colour.WHITE,  f" {era.ljust(W_ERA)} ")        + B +
            c(Colour.DIM,    f" {speed.ljust(W_SPEED)} ")    + B +
            c(time_col,      f" {crack_time.ljust(W_TIME)} ") + B
        )

    # Print table
    print(hline("+", "+", "+"))

    # Header
    B = c(Colour.MAGENTA, "|")
    print(
        B +
        c(Colour.YELLOW, f" {'#'.center(W_NUM)} ") + B +
        c(Colour.YELLOW, f" {'ERA  -  DEVICE'.ljust(W_ERA)} ") + B +
        c(Colour.YELLOW, f" {'SPEED (g/s)'.ljust(W_SPEED)} ") + B +
        c(Colour.YELLOW, f" {'CRACK TIME'.ljust(W_TIME)} ") + B
    )

    print(hline("+", "+", "+"))

    for idx, (era_name, gps, tag) in enumerate(eras, 1):
        seconds = combinations / gps

        # Format speed (plain text, fixed max width)
        if gps < 1_000:
            speed_str = f"{gps} g/s"
        elif gps < 1_000_000:
            speed_str = f"{gps // 1_000}K g/s"
        elif gps < 1_000_000_000:
            speed_str = f"{gps // 1_000_000}M g/s"
        elif gps < 1_000_000_000_000:
            speed_str = f"{gps // 1_000_000_000}B g/s"
        else:
            speed_str = f"{gps:.0e} g/s"

        # Format crack time + colour + danger tag (plain text only)
        if seconds < 1:
            time_str = "[!!!] Instantly"
            time_col = Colour.RED
        elif seconds < 60:
            time_str = f"[!!!] {int(seconds)} seconds"
            time_col = Colour.RED
        elif seconds < 3_600:
            time_str = f"[!!] {int(seconds / 60)} minutes"
            time_col = Colour.RED
        elif seconds < 86_400:
            time_str = f"[!] {int(seconds / 3600)} hours"
            time_col = Colour.YELLOW
        elif seconds < 2_592_000:
            time_str = f"[~] {int(seconds / 86400)} days"
            time_col = Colour.YELLOW
        elif seconds < 31_536_000:
            time_str = f"[~] {int(seconds / 2_592_000)} months"
            time_col = Colour.CYAN
        else:
            years = seconds / 31_536_000
            if years < 1_000:
                time_str = f"[OK] {int(years)} years"
            elif years < 1_000_000:
                time_str = f"[OK] {years / 1000:.1f}K years"
            elif years < 1_000_000_000:
                time_str = f"[OK] {years / 1_000_000:.1f}M years"
            else:
                time_str = "[OK] Heat death of universe"
            time_col = Colour.GREEN

        # Era column includes the tag badge
        era_col = f"{tag} {era_name}"

        print(data_row(idx, era_col, speed_str, time_str, time_col))

        if idx < len(eras):
            print(hline("+", "+", "+", fill="-"))

        time.sleep(0.18)

    print(hline("+", "+", "+"))
    print()

    # ── Danger legend (plain text) ──
    legend = [
        ("[!!!] Instantly / Seconds",  Colour.RED),
        ("[!!]  Minutes",               Colour.RED),
        ("[!]   Hours / Days",          Colour.YELLOW),
        ("[~]   Months",                Colour.CYAN),
        ("[OK]  Years+",                Colour.GREEN),
    ]
    print(c(Colour.WHITE, "  DANGER SCALE:"))
    for leg_text, leg_col in legend:
        print(f"    {c(leg_col, leg_text)}")
    print()
    print(c(Colour.DIM, "  * Worst-case brute force at each era's benchmark speed."))
    print(c(Colour.DIM, "    Dictionary / rule-based attacks can crack far faster."))
    print()

    SESSION.time_machine_runs += 1
    _log_event("TIME_MACHINE", f"length={len(pwd_input)}  charset={charset}")


# ─────────────────────────────────────────────
#  ACTIVITY LOG
# ─────────────────────────────────────────────

def _log_event(event_type: str, detail: str = ""):
    """
    Append a timestamped event to the persistent activity log file.

    Each line format:  YYYY-MM-DD HH:MM:SS | EVENT_TYPE | detail
    The log file accumulates across sessions (never overwritten).

    Args:
        event_type (str): Category label e.g. 'STRENGTH', 'BREACH_CHECK'.
        detail (str): Additional context (no passwords stored here).
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line      = f"{timestamp} | {event_type:<15} | {detail}\n"
        with open(LOG_FILE, "a") as f:
            f.write(line)
    except IOError:
        pass   # Log failure is silent — never crash the main program


# ─────────────────────────────────────────────
#  FEATURE 5 — SECURITY TIPS & EDUCATION
# ─────────────────────────────────────────────

def feature_tips():
    """
    Display all cybersecurity tips with navigation.
    Users can step through each tip or jump to any by number.
    """
    bar(52)
    print(c(Colour.CYAN, Colour.BOLD + "  📚 SECURITY TIPS & EDUCATION"))
    bar(52)
    print()
    print(c(Colour.WHITE, f"  {len(SECURITY_TIPS)} cybersecurity tips to keep you safe online."))
    print()
    print(c(Colour.YELLOW, "  [1-" + str(len(SECURITY_TIPS)) + "]") + "  Jump to a specific tip")
    print(c(Colour.YELLOW, "  [A]  ") + "  Read all tips")
    print(c(Colour.YELLOW, "  [R]  ") + "  Random tip")
    print()

    choice = input(c(Colour.GREEN, "  ▶ Choice: ")).strip().upper()
    print()

    if choice == "A":
        tips_to_show = list(range(len(SECURITY_TIPS)))
    elif choice == "R":
        tips_to_show = [random.randrange(len(SECURITY_TIPS))]
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SECURITY_TIPS):
                tips_to_show = [idx]
            else:
                print(c(Colour.RED, f"  Invalid tip number. Enter 1–{len(SECURITY_TIPS)}."))
                return
        except ValueError:
            print(c(Colour.RED, "  Invalid input."))
            return

    for idx in tips_to_show:
        title, body = SECURITY_TIPS[idx]
        num_label   = f"TIP {idx+1}/{len(SECURITY_TIPS)}"

        W_CARD  = 52
        header  = f"  {num_label}  {title}"
        h_pad   = " " * max(0, W_CARD - len(header) - 1)

        print(c(Colour.CYAN, "  +" + "=" * W_CARD + "+"))
        print(c(Colour.CYAN, "  |") +
              c(Colour.DIM,    f"  {num_label}  ") +
              c(Colour.YELLOW, title) +
              h_pad +
              c(Colour.CYAN, "|"))
        print(c(Colour.CYAN, "  |" + "-" * W_CARD + "|"))

        # Word-wrap body to W_CARD - 4 chars per line
        wrap_w = W_CARD - 4
        words    = body.replace("\n", " ").replace("  ", " ").split()
        line_buf = ""
        wrapped  = []
        for word in words:
            if len(line_buf) + len(word) + 1 > wrap_w:
                wrapped.append(line_buf.rstrip())
                line_buf = word + " "
            else:
                line_buf += word + " "
        if line_buf.strip():
            wrapped.append(line_buf.rstrip())

        for wl in wrapped:
            pad = " " * max(0, W_CARD - len(wl) - 2)
            print(c(Colour.CYAN, "  |") +
                  c(Colour.DIM,  f"  {wl}") +
                  pad +
                  c(Colour.CYAN, "|"))

        print(c(Colour.CYAN, "  +" + "=" * W_CARD + "+"))
        print()

        if choice == "A" and idx < tips_to_show[-1]:
            cont = input(c(Colour.DIM, "  [Enter] next tip, [Q] quit: ")).strip().upper()
            if cont == "Q":
                break
            print()

    _log_event("TIPS", f"viewed={len(tips_to_show)} tips")




def save_report(pwd_input: str, score: int, label: tuple, pwd: Password):
    """
    Save a password analysis report to a JSON file.

    Args:
        pwd_input (str): The original password string.
        score (int): Calculated strength score.
        label (tuple): Strength label and colour.
        pwd (Password): Password object for additional analysis.
    """
    label_text = label[0] if isinstance(label, tuple) else str(label)
    report = {
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "password_length": len(pwd_input),
        "score":        score,
        "strength":     label_text,
        "entropy_bits": pwd.entropy_bits(),
        "recommendations": pwd.feedback(),
    }

    filename = f"ciphersafe_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        print(c(Colour.GREEN, f"\n  ✔  Report saved to: {filename}"))
    except IOError as e:
        print(c(Colour.RED, f"\n  ✘  Could not save report: {e}"))


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def print_menu():
    """Display the main menu with live session counters."""
    print()
    print(c(Colour.GREEN + Colour.BOLD, "  Welcome, Master!"))
    print(c(Colour.WHITE, "  What would you like to do today?"))
    print()
    print(c(Colour.YELLOW, "  [1]") + c(Colour.WHITE, "  Generate Secure Password"))
    print(c(Colour.YELLOW, "  [2]") + c(Colour.WHITE, "  Check Password Breach in Dark Web"))
    print(c(Colour.YELLOW, "  [3]") + c(Colour.WHITE, "  Password Strength Analyser"))
    print(c(Colour.YELLOW, "  [4]") + c(Colour.WHITE, "  Password Time Machine"))
    print(c(Colour.YELLOW, "  [5]") + c(Colour.WHITE, "  Security Tips & Education"))
    print("\033[38;2;139;0;0m" + "  [0]" + Colour.RESET +
          "\033[38;2;139;0;0m" + "  Exit" + Colour.RESET)
    print()
    # ── Live session stats bar ──
    stats = (
        f"Generated: {c(Colour.CYAN, str(SESSION.passwords_generated))}  "
        f"Strength checks: {c(Colour.CYAN, str(SESSION.strength_checks))}  "
        f"Breach checks: {c(Colour.CYAN, str(SESSION.breach_checks))}  "
        f"Breaches found: {c(Colour.RED if SESSION.breaches_found else Colour.CYAN, str(SESSION.breaches_found))}"
    )
    print(c(Colour.DIM, "  Session ─── ") + stats)
    print()


def _print_session_summary():
    """
    Print a formatted session summary on exit.
    Shows all activity stats and writes a final log entry.
    """
    duration = SESSION.duration()
    bar(60)
    print(c(Colour.CYAN + Colour.BOLD, "  SESSION SUMMARY"))
    bar(60)
    print()

    def stat(label, value, col=Colour.WHITE):
        print(f"  {c(Colour.DIM, label.ljust(28))}  {c(col, str(value))}")

    stat("Session duration",          duration)
    stat("Passwords generated",       SESSION.passwords_generated,
         Colour.CYAN if SESSION.passwords_generated else Colour.DIM)
    stat("Strength checks run",       SESSION.strength_checks,
         Colour.CYAN if SESSION.strength_checks else Colour.DIM)
    stat("Breach checks run",         SESSION.breach_checks,
         Colour.CYAN if SESSION.breach_checks else Colour.DIM)

    if SESSION.breaches_found:
        stat("Breaches detected",     f"{SESSION.breaches_found}  ← Change these passwords NOW",
             Colour.RED)
    else:
        stat("Breaches detected",     "0  — All clear", Colour.GREEN)

    stat("Time Machine analyses",     SESSION.time_machine_runs,
         Colour.CYAN if SESSION.time_machine_runs else Colour.DIM)

    print()

    # ── Security reminder based on what they did ──
    if SESSION.breach_checks == 0:
        print(c(Colour.YELLOW, "  Tip: Try option [2] next time to check your passwords"))
        print(c(Colour.YELLOW, "       against 14 billion real leaked credentials."))
    elif SESSION.breaches_found > 0:
        print(c(Colour.RED,    "  ACTION REQUIRED: You found breached passwords this session."))
        print(c(Colour.RED,    "  Change them immediately and enable 2FA on those accounts."))
    else:
        print(c(Colour.GREEN,  "  Great work — no breaches found this session."))
        print(c(Colour.GREEN,  "  Keep using unique passwords for every account."))

    print()
    print(c(Colour.DIM, f"  Activity logged to: {LOG_FILE}"))
    print()

    # Write final log entry
    _log_event("SESSION_END",
               f"duration={duration}  "
               f"generated={SESSION.passwords_generated}  "
               f"strength={SESSION.strength_checks}  "
               f"breach_checks={SESSION.breach_checks}  "
               f"breaches={SESSION.breaches_found}")

    bar(60)


def main():
    """Entry point — run the main CipherSafe loop."""
    # Write session start to log
    _log_event("SESSION_START", f"platform={platform.system()}  python={platform.python_version()}")

    print_banner()
    time.sleep(0.4)

    while True:
        print_menu()
        choice = input(c(Colour.GREEN, "  ▶ Enter your choice: ")).strip()
        print()

        if choice == "1":
            feature_generate()
        elif choice == "2":
            feature_breach()
        elif choice == "3":
            feature_strength()
        elif choice == "4":
            feature_time_machine()
        elif choice == "5":
            feature_tips()
        elif choice == "0":
            print()
            _print_session_summary()
            print()
            slow_print(c(Colour.GREEN, "  Goodbye, Master. Stay secure. 🔒"), delay=0.03)
            print()
            break
        else:
            print(c(Colour.RED, "  Invalid option. Enter 1, 2, 3, 4, 5 or 0."))

        input(c(Colour.DIM, "  Press Enter to return to menu..."))
        print()
        bar(52)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()
