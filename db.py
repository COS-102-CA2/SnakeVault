from config import supabase

# ==========================================
# 1. USER AUTHENTICATION (Login / Register)
# ==========================================

def sign_up_user(email, password):
    """Registers a new user in Supabase Auth."""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email, password):
    """Logs a user in and starts an authenticated session."""
    try:
        # Fixed: Removed .with_options() chaining error
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

def logout_user():
    """Logs out the current user and clears the session."""
    try:
        supabase.auth.sign_out()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==========================================
# 2. PASSWORD VAULT OPERATIONS
# ==========================================

def save_password(site_name, url, username, encrypted_password, category="General", notes=None):
    """Saves an ENCRYPTED password to the user's vault."""
    try:
        # Get the currently logged-in user's ID
        user_response = supabase.auth.get_user()
        if not user_response or not user_response.user:
            return {"success": False, "error": "No active user session."}
        
        user_id = user_response.user.id

        data = {
            "user_id": user_id,
            "site_name": site_name,
            "url": url,
            "username": username,
            "encrypted_password": encrypted_password,  # Stored securely as ciphertext
            "category": category,
            "notes": notes
        }

        response = supabase.table("passwords").insert(data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def fetch_user_passwords():
    """Fetches all encrypted credentials belonging to the logged-in user."""
    try:
        response = supabase.table("passwords").select("*").execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}