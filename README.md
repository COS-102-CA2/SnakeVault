# SnakeVault

SnakeVault is a desktop password manager built with Python, Tkinter, and Supabase.

It uses two layers of security:

1. Supabase Auth for account login/signup
2. A local master key for vault encryption and decryption

The master key is never stored directly. Only its bcrypt hash is saved in Supabase.

## Tech Stack

- Python
- Tkinter
- Supabase
- bcrypt
- python-dotenv

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

Run the app:

```bash
python main.py
```

## Supabase Tables

### users

| Column     | Type      |
| ---------- | --------- |
| id         | uuid      |
| user_id    | uuid      |
| key_hash   | text      |
| created_at | timestamp |

### passwords

| Column             | Type      |
| ------------------ | --------- |
| id                 | bigint    |
| user_id            | uuid      |
| site_name          | text      |
| url                | text      |
| username           | text      |
| encrypted_password | text      |
| category           | text      |
| notes              | text      |
| created_at         | timestamp |

## User Flow

New user:

```text
Welcome -> Login/Signup -> Create Master Key -> Confirm Master Key -> Setup Complete -> Dashboard
```

Returning user:

```text
Welcome -> Login -> Unlock Vault -> Dashboard
```

## Branch Workflow

The group uses feature branches.

Team Lead works on:

```text
main
```

Other members work on:

```text
feature/auth-screens
feature/welcome-generator
feature/add-password
feature/crypto-screens
feature/search-detail
feature/style-pass
```

Create a feature branch:

```bash
git checkout main
git pull origin main
git checkout -b feature/branch-name
```

Commit changes:

```bash
git add filename.py
git commit -m "feat: short description"
git push -u origin feature/branch-name
```

Team Lead merges after review:

```bash
git checkout main
git pull origin main
git merge feature/branch-name
git push origin main
```

After Team Lead merges, everyone pulls latest main into their branch:

```bash
git checkout feature/your-branch-name
git pull origin main
```

## Commit Types

Use:

```text
feat: new feature or screen
fix: bug fix
refactor: code restructuring without behavior change
style: visual/UI consistency changes
docs: README or documentation updates
chore: setup or maintenance changes
```

## Team Roles

Chinemerem Okolie: project lead, routing, shared state, database helpers, crypto helpers, merges  
Ozioma Anieke: dashboard and add-password flow  
Ogunremi Temiloluwa: final style pass  
Zaccheaus Oluwatobiloba: password detail, reveal, decrypt, delete  
Ohakaba Ebubechukwu: welcome screen and password generator  
Moses Abraham: login/signup, create key, confirm key, unlock  
Ukwu Kelechi: search, settings, change master key, README
