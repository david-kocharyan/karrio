from purplship.core import Settings as BaseSettings
from pyfedex.rate_v22 import (
    WebAuthenticationCredential,
    WebAuthenticationDetail,
    ClientDetail,
)


class Settings(BaseSettings):
    """FedEx connection settings."""

    user_key: str
    password: str
    meter_number: str
    account_number: str

    @property
    def webAuthenticationDetail(self) -> WebAuthenticationDetail:
        return WebAuthenticationDetail(
            UserCredential=WebAuthenticationCredential(
                Key=self.user_key, Password=self.password
            )
        )

    @property
    def clientDetail(self) -> ClientDetail:
        return ClientDetail(
            AccountNumber=self.account_number, MeterNumber=self.meter_number
        )
