from pydantic import BaseSettings


class Settings(BaseSettings):
    cookie_authorization_name: str = "Authorization"
    cookie_domain: str
    protocol: str
    full_host_name: str
    port_number: int
    client_id: str
    client_secrets_json: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    api_location = f"{protocol}{full_host_name}:{port_number}"

    class Config:
        env_file = ".env"
