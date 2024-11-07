from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    sqlalchemy_url: SecretStr
    rpc_monero_login: SecretStr
    rpc_monero_password: SecretStr
    rpc_monero_port: SecretStr
    transaction_priority_monero: int  # Приоритет транзакции Monero
    # Параметры для Monero демона
    demon_monero_host: SecretStr
    demon_monero_port: SecretStr
    demon_monero_user: SecretStr
    demon_monero_password: SecretStr
    monero_withdraw_fee: float

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

config = Settings()