# KeyVault — Group Commit Plan
**Stack:** Python · Tkinter · PostgreSQL  
**Team:** 7 members (P1 – P7)  
**Repo:** Group GitHub Organization

---

## Commit keyword guide

| Keyword | When to use |
|---|---|
| `feat:` | Adding a new screen, button, or working feature |
| `fix:` | Correcting something broken or wrong in existing code |
| `refactor:` | Reorganizing code without changing what it does |
| `style:` | Visual changes — colors, fonts, padding, layout |
| `chore:` | Project setup, configuration, file structure |
| `docs:` | README, comments, notes — no code logic |

Each commit message goes: `type: short description in lowercase`  
Example: `feat: add master key input to create key screen`

---

## Project folder structure
Every member should understand what lives where before writing any code.

```
snakevault/
├── main.py               ← app entry point (P1)
├── libs/password_backend.py
├── requirements.txt      ← project dependencies (P1)
├── .gitignore            ← ignores .env and __pycache__ (P1)
├── screens/
│   ├── title.py          ← welcome screen (P3) The user enters their master key here.
│   ├── create_key.py     ← create master key screen (P4)
│   ├── dashboard.py      ← main vault dashboard (P1)
│   ├── search.py         ← search screen (P7)
│   ├── password_detail.py← password item + reveal (P6)
│   ├── generator.py      ← password generator tool (P3)
└── README.md             ← setup and run instructions (P7)
```

---


## Phase 4 — Welcome screen
> **Who:** P5  
> **Goal:** First screen the user ever sees. Two buttons — one for new users, one for returning users.

| # | Commit | What it does |
|---|---|---|
| 14 | `feat: build welcome screen frame in screens/welcome.py` | Tkinter Frame with app name label and two buttons |
| 15 | `style: apply background color, font, and button styling to welcome screen` | Matches the agreed color theme |
| 16 | `feat: wire welcome screen buttons to show correct next screen` | "Create vault" goes to create_key; "Unlock vault" goes to unlock |

**P5 total: 3 commits**

---

## Phase 5 — Create master key + Confirm + Setup complete
> **Who:** P6  
> **Goal:** The three screens a new user walks through to create their vault for the first time.

| # | Commit | What it does |
|---|---|---|
| 17 | `feat: build create master key screen with password entry field` | Entry widget with show/hide toggle button |
| 18 | `feat: add password strength label that updates as user types` | Checks length and character variety, shows Weak / Fair / Strong |
| 19 | `feat: build confirm master key screen` | Second entry field asking user to re-type their key |
| 20 | `fix: show error message when the two keys do not match` | Red label appears if strings differ; clears fields for retry |
| 21 | `feat: on match, hash the key and save to users table` | Calls `hash_key()` from crypto.py, writes result to PostgreSQL |
| 22 | `feat: build setup complete screen and route to dashboard` | Simple success message then navigates to dashboard |

**P6 total: 6 commits**

---

## Phase 6 — Unlock screen (returning user)
> **Who:** P7  
> **Goal:** The screen returning users see. Verifies their master key before letting them into the vault.

| # | Commit | What it does |
|---|---|---|
| 23 | `feat: build unlock screen with master key entry field` | Entry field + Unlock button |
| 24 | `feat: load stored key hash from database on screen open` | Fetches from the users table |
| 25 | `feat: verify entered key and navigate to dashboard on success` | Calls `verify_key()` from crypto.py |
| 26 | `fix: display wrong key error and clear field on failed attempt` | Prevents silent failures |

**P7 total: 4 commits**

---

## Phase 7 — Dashboard
> **Who:** P1  
> **Goal:** The hub screen users see after unlocking. Shows recent passwords and navigation options.

| # | Commit | What it does |
|---|---|---|
| 27 | `feat: build dashboard screen frame with heading and nav buttons` | Buttons for All Passwords, Add, Search, Settings |
| 28 | `feat: load and display 5 most recent password entries on dashboard` | Queries passwords table ordered by `created_at DESC LIMIT 5` |
| 29 | `style: apply consistent card-style layout to recent entries list` | Each entry shows site name and username in a neat row |

**P1 additional: 3 commits → P1 total: 6 commits**

---

## Phase 8 — Add password form
> **Who:** P2  
> **Goal:** The form users fill in to save a new password. Encrypts before saving.

| # | Commit | What it does |
|---|---|---|
| 30 | `feat: build add password form with all input fields` | Site name, URL, username, password (with show/hide), category, notes |
| 31 | `feat: encrypt password field value before saving to database` | Calls `encrypt()` from crypto.py before the INSERT |
| 32 | `feat: save completed form to passwords table on submit` | Runs the INSERT query via db.py |
| 33 | `fix: validate required fields are not empty before saving` | Shows inline error if site name, username, or password is blank |
| 34 | `fix: clear the form fields after a successful save` | Prevents leftover data confusion |

**P2 additional: 5 commits → P2 total: 8 commits**

---

## Phase 9 — All passwords list + Search
> **Who:** P3  
> **Goal:** Let users browse and find all their saved entries.

| # | Commit | What it does |
|---|---|---|
| 35 | `feat: build password list screen showing all saved entries` | Scrollable list of rows, each showing site name and username |
| 36 | `feat: load all password entries from database into list screen` | SELECT query via db.py, results rendered as rows |
| 37 | `feat: add search bar to list screen that filters results as user types` | Filters the rendered rows by site_name in real time |
| 38 | `fix: show empty state message when no entries match search` | "No results found" label when the filtered list is empty |

**P3 additional: 4 commits → P3 total: 7 commits**

---

## Phase 10 — Password detail + Master key verification prompt
> **Who:** P4  
> **Goal:** When a user taps an entry, show its details. Reveal the password only after re-verifying the master key.

| # | Commit | What it does |
|---|---|---|
| 39 | `feat: build password detail screen showing site, username, masked password` | Password field shows `••••••••` by default |
| 40 | `feat: add verify master key dialog that appears before revealing password` | Small popup with a key entry field and Confirm button |
| 41 | `feat: decrypt and display password after master key is verified` | Calls `verify_key()` then `decrypt()` from crypto.py |
| 42 | `fix: auto-hide the revealed password after 30 seconds` | Resets field back to `••••••••` using `after()` Tkinter method |
| 43 | `feat: add copy-to-clipboard button for each revealed field` | One-click copy for username and password |

**P4 additional: 5 commits → P4 total: 9 commits**

---

## Phase 11 — Password generator
> **Who:** P5  
> **Goal:** Let users generate strong passwords inside the add-password form.

| # | Commit | What it does |
|---|---|---|
| 44 | `feat: build password generator screen with length slider` | Slider from 8 to 64 characters |
| 45 | `feat: add character option checkboxes (uppercase, numbers, symbols)` | Checkboxes that control what the generator includes |
| 46 | `feat: generate and preview a password from selected options` | Uses Python `secrets` module — not `random` |
| 47 | `feat: insert generated password back into add password form` | Passes value to the form's password field and closes generator |
| 48 | `fix: ensure at least one character type is always selected` | Prevents generating an empty or invalid password |

**P5 additional: 5 commits → P5 total: 8 commits**

---

## Phase 12 — Settings screen + Change master key
> **Who:** P6  
> **Goal:** A settings page with a working change-key flow.

| # | Commit | What it does |
|---|---|---|
| 49 | `feat: build settings screen with security and data section labels` | Static layout with grouped option rows |
| 50 | `feat: add change master key option that opens a three-step flow` | Step 1: enter current key, Step 2: enter new key, Step 3: confirm new key |
| 51 | `feat: re-encrypt all saved passwords when master key is changed` | Decrypts each password with old key, re-encrypts with new key, updates DB |
| 52 | `fix: show success confirmation after master key is changed` | Brief message before returning to settings |

**P6 additional: 4 commits → P6 total: 10 commits**

---

## Phase 13 — Final fixes and documentation
> **Who:** All members  
> **Goal:** Clean up, polish, and document. Every member makes at least one more commit.

| # | Who | Commit | What it does |
|---|---|---|---|
| 53 | P7 | `docs: write README with setup steps and how to run the app` | Clear instructions for installing deps, setting up `.env`, running `main.py` |
| 54 | P1 | `fix: handle database connection error with a user-facing message` | If PostgreSQL is unreachable, show a clear error instead of crashing |
| 55 | P2 | `refactor: move all raw SQL strings into named functions in db.py` | Cleaner code — screens call functions, not raw queries |
| 56 | P3 | `style: make font sizes and padding consistent across all screens` | One pass through every screen file to normalize spacing |
| 57 | P4 | `refactor: move all crypto imports to top of crypto.py only` | Other files import from crypto.py, not directly from bcrypt or cryptography |
| 58 | P5 | `fix: prevent double-click from submitting the save form twice` | Disables submit button after first click until operation completes |
| 59 | P6 | `fix: clear master key entry fields after every failed attempt` | Security measure — never leave a typed key visible after an error |
| 60 | P7 | `style: add window icon and set consistent window title across screens` | Small polish that makes the app feel complete |

---

## Summary — commits per person

| Member | Phases covered | Total commits |
|---|---|---|
| P1 | Setup · Dashboard · DB error fix | **6** |
| P2 | App skeleton · Add password form · DB refactor | **8** |
| P3 | Database schema · Password list · Style pass | **7** |
| P4 | Crypto utilities · Password detail · Crypto refactor | **9** |
| P5 | Welcome screen · Generator · Double-click fix | **8** |
| P6 | Create/Confirm/Setup screens · Settings · Key clear fix | **10** |
| P7 | Unlock screen · List + Search · README · Title polish | **8** |
| | **Total** | **56 commits** |

---

## Suggested commit order (timeline view)

```
Week 1
──────
P1: commits 1–3   (project setup)
P2: commits 4–6   (app skeleton)
P3: commits 7–9   (database tables)
P4: commits 10–13 (crypto utilities)

Week 2
──────
P5: commits 14–16 (welcome screen)
P6: commits 17–22 (create key → setup complete)
P7: commits 23–26 (unlock screen)
P1: commits 27–29 (dashboard)

Week 3
──────
P2: commits 30–34 (add password form)
P3: commits 35–38 (list + search)
P4: commits 39–43 (detail + reveal)

Week 4
──────
P5: commits 44–48 (generator)
P6: commits 49–52 (settings + change key)
P7–P1: commits 53–60 (final fixes + docs)
```

---

## Important rules for the team

1. **Pull before you push.** Always run `git pull origin main` before starting any session so you have the latest code.
2. **One feature per commit.** Don't mix two changes into one commit — keep them small and specific.
3. **Write your commit message first.** If you can't explain what your commit does in one short line, you don't understand it well enough yet.
4. **Never commit the `.env` file.** It contains your database password. The `.gitignore` handles this, but double-check.
5. **Read the crypto.py file carefully.** Every screen that saves or shows a password depends on it. Understanding it is non-negotiable.
