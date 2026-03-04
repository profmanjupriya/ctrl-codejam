"""
Simple HMAC-signed auth token so the frontend can send Authorization: Bearer <token>
and the backend can authenticate when the session cookie is not sent (e.g. cross-origin).
"""
import base64
import hmac
import json
import time

from config import SECRET_KEY

TOKEN_EXPIRY_SEC = 24 * 3600  # 24 hours


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64_decode(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


def make_token(user_id: int, username: str, is_admin: bool) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "is_admin": is_admin,
        "exp": time.time() + TOKEN_EXPIRY_SEC,
    }
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    payload_b64 = _b64_encode(raw)
    sig = hmac.new(SECRET_KEY.encode("utf-8"), raw, "sha256").digest()
    sig_b64 = _b64_encode(sig)
    return f"{payload_b64}.{sig_b64}"


def verify_token(token: str) -> dict | None:
    if not token or "." not in token:
        return None
    try:
        payload_b64, sig_b64 = token.split(".", 1)
        raw = _b64_decode(payload_b64)
        payload = json.loads(raw.decode("utf-8"))
        if payload.get("exp", 0) < time.time():
            return None
        sig = _b64_decode(sig_b64)
        expected = hmac.new(SECRET_KEY.encode("utf-8"), raw, "sha256").digest()
        if not hmac.compare_digest(sig, expected):
            return None
        return payload
    except Exception:
        return None


def get_bearer_token(request) -> str | None:
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def current_user_from_request(request, session) -> dict | None:
    """
    Return {"user_id": int, "username": str, "is_admin": bool} or None.
    Checks Authorization: Bearer <token> first, then Flask session.
    """
    token = get_bearer_token(request)
    if token:
        payload = verify_token(token)
        if payload:
            return {
                "user_id": payload["user_id"],
                "username": payload["username"],
                "is_admin": payload.get("is_admin", False),
            }
    if session.get("username"):
        return {
            "user_id": session.get("user_id"),
            "username": session["username"],
            "is_admin": session.get("is_admin", False),
        }
    return None
