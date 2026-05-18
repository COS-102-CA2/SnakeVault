#SnakeVault
A desktop password manager built with Python, Tkinter, and PostgreSQL.

##Requirements

- Python 3.10 or higher
- PostgreSQL installed and running

##Setup — do this once before running the app

**1. Clone the repository**
git clone <your-org-repo-url>
cd SnakeVault

**2. Install dependencies**
pip install -r requirements.txt

**3. Create your .env file**
Copy the example file and fill in your own PostgreSQL credentials:
cp .env.example .env

Then open .env and replace the placeholder values with your actual details.

**4. Create the database in PostgreSQL**
Open your PostgreSQL shell and run:
CREATE DATABASE snakvault;

**5. Run the app**
python main.py

##Project structure
SnakeVault/
├── main.py — app entry point
├── db.py — all PostgreSQL queries
├── requirements.txt — project dependencies
├── .env — your local credentials (never committed)
├── .env.example — template showing what .env needs
├── libs/
│ ├── crypto.py — encryption and decryption
│ └── window_manager.py — screen navigation
├── screens/
│ ├── welcome.py — welcome screen
│ ├── create_key.py — new user master key setup
│ ├── confirm_key.py — confirm master key
│ ├── setup_done.py — setup success screen
│ ├── unlock.py — returning user unlock
│ ├── dashboard.py — main vault dashboard
│ ├── add_password.py — add new password form
│ ├── password_detail.py — view and reveal password
│ ├── search.py — search entries
│ ├── generator.py — password generator
│ └── settings.py — app settings
└── docs/
└── commit-plan.md — team commit guide

##Team
Group project — 7 members.
