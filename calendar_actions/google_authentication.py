"""
не логиним по паролю, вместо это используем связку токенов
(обновление токена доступа с помощью refresh-токена)

1. бот отсылает 'get_authorization_url(..., state=...)'
2. гугл редиректит на 'redirect_uri' с 'code` + `state'
3. мы зовем 'exchange_code_for_credentials(code, ...)'
4. сохраняем refresh_token + access_token bound to telegram_user_id
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, Dict, Any
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json


DEFAULT_SCOPES = (
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
)


class GoogleAuthNotInstalled(RuntimeError):
    pass


@dataclass(frozen=True)
class OAuthClient:
    """
    Представляет OAuth-учётные данные *приложения*
    (не учётные данные пользователя!!!!)

    Может быть создан:
      - из файла client_secret.json скачанного из Google Cloud (оч желательно)
      - либо из словаря с такой же структурой
    """
    client_secrets_file: Optional[str] = None
    client_config: Optional[Dict[str, Any]] = None

    def validate(self) -> None:
        if not self.client_secrets_file and not self.client_config:
            raise ValueError("Provide either client_secrets_file or client_config.")
        if self.client_secrets_file and self.client_config:
            raise ValueError("Provide only one of client_secrets_file or client_config.")


def get_authorization_url(
    oauth_client: OAuthClient,
    redirect_uri: str,
    state: str,
    scopes: Iterable[str] = DEFAULT_SCOPES,
    access_type: str = "offline",
    include_granted_scopes: bool = True,
    prompt: str = "consent",
) -> Tuple[str, str]:
    """
    state должен быть криптографической штукой (строкой и тп) который мапится на telegram_user_id.
    access_type="offline" + prompt="consent"  помогают получать refresh_token.
    """

    oauth_client.validate()

    if oauth_client.client_secrets_file:
        flow = Flow.from_client_secrets_file(
            oauth_client.client_secrets_file,
            scopes=list(scopes),
            redirect_uri=redirect_uri,
        )
    else:
        flow = Flow.from_client_config(
            oauth_client.client_config,  # type: ignore[arg-type]
            scopes=list(scopes),
            redirect_uri=redirect_uri,
        )

    authorization_url, returned_state = flow.authorization_url(
        access_type=access_type,
        include_granted_scopes=include_granted_scopes,
        prompt=prompt,
        state=state,
    )
    return authorization_url, returned_state


def exchange_code_for_credentials(
    oauth_client: OAuthClient,
    redirect_uri: str,
    code: str,
    scopes: Iterable[str] = DEFAULT_SCOPES,
) -> Credentials:
    """
    обмениваем одноразовый код на  OAuth credentials.
    """

    oauth_client.validate()

    if oauth_client.client_secrets_file:
        flow = Flow.from_client_secrets_file(
            oauth_client.client_secrets_file,
            scopes=list(scopes),
            redirect_uri=redirect_uri,
        )
    else:
        flow = Flow.from_client_config(
            oauth_client.client_config,  # type: ignore[arg-type]
            scopes=list(scopes),
            redirect_uri=redirect_uri,
        )

    flow.fetch_token(code=code)
    return flow.credentials


def refresh_credentials(creds: Credentials) -> Credentials:
    """
    рефрешим токен
    """
    if not creds.refresh_token:
        raise ValueError("No refresh_token in credentials; cannot refresh.")
    creds.refresh(Request())
    return creds


def credentials_to_json_dict(creds: Credentials) -> Dict[str, Any]:
    """
     credentials to a JSON для удобного хранения в бд
    """
    return json.loads(creds.to_json())


def credentials_from_json_dict(data: Dict[str, Any], scopes: Iterable[str] = DEFAULT_SCOPES) -> "Credentials":
    """
    восстанавливаем credentials из  dict (обратная credentials_to_json_dict).
    """
    return Credentials.from_authorized_user_info(info=data, scopes=list(scopes))
