from config import supabase


def sign_up_user(email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}


def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}


def logout_user():
    try:
        supabase.auth.sign_out()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_current_user_id():
    try:
        user_response = supabase.auth.get_user()
        if not user_response or not user_response.user:
            return None
        return user_response.user.id
    except Exception:
        return None


def save_master_key(key_hash):
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        existing = (
            supabase.table("users")
            .select("id")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        data = {
            "user_id": user_id,
            "key_hash": key_hash,
        }

        if existing.data:
            response = (
                supabase.table("users")
                .update(data)
                .eq("user_id", user_id)
                .execute()
            )
        else:
            response = supabase.table("users").insert(data).execute()

        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_master_key():
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        response = (
            supabase.table("users")
            .select("key_hash")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return {"success": True, "data": None}

        return {"success": True, "data": response.data[0]["key_hash"]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_password(site_name, url, username, encrypted_password, category="General", notes=None):
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        data = {
            "user_id": user_id,
            "site_name": site_name,
            "url": url,
            "username": username,
            "encrypted_password": encrypted_password,
            "category": category,
            "notes": notes,
        }

        response = supabase.table("passwords").insert(data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_user_passwords():
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        response = (
            supabase.table("passwords")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_password(entry_id, site_name, url, username, encrypted_password, category="General", notes=None):
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        data = {
            "site_name": site_name,
            "url": url,
            "username": username,
            "encrypted_password": encrypted_password,
            "category": category,
            "notes": notes,
        }

        response = (
            supabase.table("passwords")
            .update(data)
            .eq("id", entry_id)
            .eq("user_id", user_id)
            .execute()
        )

        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_password(entry_id):
    try:
        user_id = get_current_user_id()
        if not user_id:
            return {"success": False, "error": "No active user session."}

        response = (
            supabase.table("passwords")
            .delete()
            .eq("id", entry_id)
            .eq("user_id", user_id)
            .execute()
        )

        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}