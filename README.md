# vulnerable-flask-app
# Vulnerable Flask App - VulnVault

This is a deliberately insecure Flask web application built for educational purposes to demonstrate and test common web security vulnerabilities.

## Features / Vulnerabilities included

- SQL Injection (Login)
- Cross-Site Scripting (XSS)
- Insecure File Upload
- Insecure Direct Object Reference (IDOR)
- Broken Authentication (Change Admin Password)

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/elen31/vulnerable-flask-app.git
cd vulnerable-flask-app
Usage

    Use /login to test SQL Injection.

    Use /xss to test Cross-Site Scripting.

    Use /upload to test insecure file uploads.

    Use /idor?id=1 to test IDOR vulnerability.

    Use /change_password to test broken authentication.

Warning

This app is intentionally insecure. Do not deploy it on production or public servers.
License

MIT License
## Vulnerabilities Included

| Vulnerability          | OWASP | Description                                      |
|-----------------------|-------|-------------------------------------------------|
| 💬 XSS                | A7    | User comments render unescaped HTML (unsafe)    |
| 🛑 SQL Injection       | A1    | Login bypass using classic `' OR 1=1 --`         |
| 🔁 CSRF                | A5    | Profile update without CSRF tokens                |
| 🧾 IDOR                | A4    | Invoices accessible by changing `/invoice/<id>`  |
| 📎 Insecure File Upload | A8    | Uploads allow arbitrary file types                |
| 🧑‍💻 Broken Auth       | A2    | No rate limit or session expiration               |
| ⚙️ Misconfiguration    | A6    | Debug mode enabled, stack traces visible          |

