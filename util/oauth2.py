from typing import Optional

from fastapi import Request, HTTPException, status
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel, get_authorization_scheme_param


class OAuth2ClientTokenBearer(OAuth2):
    def __init__(
            self,
            token_url: str,
            scheme_name: str = None,
            scopes: dict = None,
            auto_error: bool = True
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)

        if header_scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        return header_param
