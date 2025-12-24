from __future__ import annotations

import base64
import hashlib
import os
import secrets
from urllib.parse import urlencode
from typing import Iterable, Dict, Any, Tuple

import requests


GOOGLE_AUTHZ_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> Tuple[str, str]:
    """Возвращает code_verifier, code_challenge для PKCE S256"""
    verifier = _b64url(os.urandom(64))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(
    *,
    client_id: str,
    redirect_uri: str,
    scopes: Iterable[str],
    state: str,
    code_challenge: str,
    access_type: str = "offline",
    prompt: str = "consent",
) -> str:
    """Формирует URL для согласия пользователя (Authorization Code + PKCE)"""

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state,
        "access_type": access_type,
        "prompt": prompt,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{GOOGLE_AUTHZ_ENDPOINT}?{urlencode(params)}"


def exchange_code_for_tokens(
    *,
    client_id: str,
    client_secret: str | None,
    redirect_uri: str,
    code: str,
    code_verifier: str,
) -> Dict[str, Any]:
    """Обменивает одноразовый code на access_token (+refresh_token при первом согласии)"""

    data = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier,
    }
    if client_secret:
        data["client_secret"] = client_secret

    r = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"Token exchange failed: {r.status_code} {r.text}")
    return r.json()


def generate_state() -> str:
    return secrets.token_urlsafe(24)
