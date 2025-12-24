from __future__ import annotations

import time
from datetime import timezone, timedelta
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
]

@dataclass(frozen=True)
class OAuthClient:
    client_id: str
    client_secret: Optional[str] = None
    scopes: list[str] = None  # type: ignore

    def __post_init__(self):
        if self.scopes is None:
            object.__setattr__(self, "scopes", DEFAULT_SCOPES)

class GoogleAuthError(RuntimeError):
    pass

def start_device_flow(oauth: OAuthClient) -> Dict[str, Any]:
    """
    Возвращает device_code/user_code/verification_url/expires_in/interval
    """
    url = "https://oauth2.googleapis.com/device/code"
    data = {
        "client_id": oauth.client_id,
        "scope": " ".join(oauth.scopes),
    }
    r = requests.post(url, data=data, timeout=20)
    if r.status_code != 200:
        raise GoogleAuthError(f"Device flow init failed: {r.status_code} {r.text}")
    return r.json()

def poll_device_flow_token(
    oauth: OAuthClient,
    device_code: str,
    interval: int,
    expires_in: int,
) -> Dict[str, Any]:
    """
    Блокирующая функция: ждём, пока пользователь авторизуется.
    Возвращает token response: access_token + refresh_token + expires_in + scope + token_type
    """
    token_url = "https://oauth2.googleapis.com/token"
    deadline = time.time() + expires_in

    while time.time() < deadline:
        payload = {
            "client_id": oauth.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        if oauth.client_secret:
            payload["client_secret"] = oauth.client_secret

        r = requests.post(token_url, data=payload, timeout=20)

        data = r.json()
        if r.status_code == 200 and "access_token" in data:
            return data

        err = data.get("error")
        if err in ("authorization_pending",):
            time.sleep(max(1, interval))
            continue
        if err in ("slow_down",):
            interval += 5
            time.sleep(max(1, interval))
            continue
        if err in ("expired_token", "access_denied"):
            raise GoogleAuthError(f"Device flow failed: {err}")

        raise GoogleAuthError(f"Device flow token error: {r.status_code} {r.text}")

    raise GoogleAuthError("Device flow timeout")

def refresh_access_token(oauth: OAuthClient, refresh_token: str) -> Dict[str, Any]:
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": oauth.client_id,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    if oauth.client_secret:
        payload["client_secret"] = oauth.client_secret

    r = requests.post(token_url, data=payload, timeout=20)

    if r.status_code != 200:
        raise GoogleAuthError(f"Refresh failed: {r.status_code} {r.text}")
    return r.json()

def build_google_event_payload(event) -> Dict[str, Any]:
    """
    event: parser_module.domain.models.Event
    Делает payload для Google Calendar API.
    """

    start_dt = event.date_start
    end_dt = event.date_end or event.date_start

    MSK = timezone(timedelta(hours=3))
    
    def to_rfc3339(dt):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MSK)
        return dt.isoformat()

    payload: Dict[str, Any] = {
        "summary": event.name,
        "start": {"dateTime": to_rfc3339(start_dt)},
        "end": {"dateTime": to_rfc3339(end_dt)},
    }

    desc = getattr(event, "description", None)
    if desc:
        payload["description"] = desc

    loc = getattr(event, "location", None)
    if loc:
        payload["location"] = loc

    return payload

def insert_event_to_google_calendar(access_token: str, payload: Dict[str, Any], calendar_id: str = "primary") -> Dict[str, Any]:
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )
    if r.status_code not in (200, 201):
        raise GoogleAuthError(f"Insert event failed: {r.status_code} {r.text}")
    return r.json()
