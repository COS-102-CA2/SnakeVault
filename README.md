# SnakeVault

SnakeVault is a desktop password manager built with Python, CustomTkinter, and Supabase.

It was created as a university group project. The app allows users to create an account, protect their vault with a local master key, save encrypted passwords, search saved credentials, generate strong passwords, and export backups.

## Features

- Email and password signup/login using Supabase Auth
- Local master key flow for vault access
- Master key hashing with bcrypt
- Local password encryption before saving to Supabase
- Dashboard showing saved vault entries
- Add password form with password generator
- Password strength feedback
- Searchable password list
- Password detail screen with master-key verification before reveal
- Copy controls for saved values
- Delete saved credentials
- Change master key flow with re-encryption
- Backup and export screen
- Encrypted backup export
- Plain-text CSV export with warning and master key verification
- Dark themed CustomTkinter interface

## Security Model

SnakeVault uses two separate security layers.

### 1. Supabase Auth

Supabase Auth handles account identity.

It answers:

```text
Who is the user?
```

Users sign up and log in with an email and password. Supabase manages authentication sessions.

### 2. Master Key

The master key protects the password vault.

It answers:

```text
Can this user decrypt their saved passwords?
```

The master key itself is never stored in Supabase. Only a bcrypt hash of the master key is saved in the `users` table.

Saved passwords are encrypted locally before being sent to Supabase. Decryption also happens locally after the user verifies their master key.

## User Flow

New user:

```text
Welcome -> Login/Signup -> Create Master Key -> Confirm Master Key -> Setup Complete -> Dashboard
```

Returning user:

```text
Welcome -> Login -> Unlock Vault -> Dashboard
```

## Tech Stack

- Python
- CustomTkinter
- Tkinter
- Supabase
- bcrypt
- python-dotenv
- cryptography
- Pillow

## Project Structure

```text
SnakeVault/
├── main.py
├── config.py
├── db.py
├── requirements.txt
├── README.md
├── libs/
│   ├── crypto.py
│   └── window_manager.py
└── screens/
    ├── welcome.py
    ├── login_screen.py
    ├── create_key.py
    ├── confirm_key.py
    ├── setup_done.py
    ├── unlock.py
    ├── dashboard_screen.py
    ├── add_password.py
    ├── password_detail.py
    ├── generator.py
    ├── search.py
    ├── settings.py
    └── backup_export.py
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd SnakeVault
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 5. Run the app

```bash
python main.py
```

## Supabase Tables

Run these SQL statements in the Supabase SQL Editor.

### users table

```sql
create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  key_hash text,
  created_at timestamp with time zone default now(),
  unique (user_id)
);
```

### passwords table

```sql
create table if not exists public.passwords (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  site_name text not null,
  url text,
  username text not null,
  encrypted_password text not null,
  category text default 'General',
  notes text,
  created_at timestamp with time zone default now()
);
```

## Row Level Security Policies

Enable Row Level Security:

```sql
alter table public.users enable row level security;
alter table public.passwords enable row level security;
```

### users policies

```sql
create policy "Users can read own master key"
on public.users
for select
using (auth.uid() = user_id);

create policy "Users can insert own master key"
on public.users
for insert
with check (auth.uid() = user_id);

create policy "Users can update own master key"
on public.users
for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);
```

### passwords policies

```sql
create policy "Users can read own passwords"
on public.passwords
for select
using (auth.uid() = user_id);

create policy "Users can insert own passwords"
on public.passwords
for insert
with check (auth.uid() = user_id);

create policy "Users can update own passwords"
on public.passwords
for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

create policy "Users can delete own passwords"
on public.passwords
for delete
using (auth.uid() = user_id);
```

## Backup and Export

SnakeVault supports two export options.

### Encrypted backup

The encrypted backup exports saved vault data while keeping passwords encrypted.

This is the safer option.

### CSV export

CSV export decrypts saved passwords and writes them as plain text.

The app shows a warning and asks the user to verify their master key before exporting CSV. Users should delete CSV exports immediately after use.

## Team Roles

P1: project lead, routing, shared state, database helpers, crypto helpers, merges  
P2: dashboard and add password flow  
P3: final UI/UX polish  
P4: password detail, reveal, decrypt, delete  
P5: welcome screen and password generator  
P6: login/signup, create key, confirm key, unlock  
P7: search, settings, change master key, backup/export, README

## Branch Workflow

P1 works on:

```text
main
```

Other members work on feature branches:

```text
feature/auth-screens
feature/welcome-generator
feature/add-password
feature/crypto-screens
feature/search-detail
feature/style-pass
feature/customtkinter-polish
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

P1 merges after review:

```bash
git checkout main
git pull origin main
git merge feature/branch-name
git push origin main
```

After P1 merges, everyone pulls latest main:

```bash
git checkout feature/your-branch-name
git pull origin main
```

## Commit Types

Use clear commit prefixes:

```text
feat: new feature
fix: bug fix
refactor: code restructuring
style: UI or visual changes
docs: documentation
chore: setup or maintenance
```

## Notes

- Do not commit `.env`.
- The master key should never be stored directly.
- Passwords should be encrypted before saving to Supabase.
- Plain-text CSV exports should be handled carefully and deleted after use.
