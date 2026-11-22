
from pydantic import BaseModel, field_validator


class TickerRequest(BaseModel):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, value):
        value = value.strip().upper()

        if not value:
            raise ValueError("Ticker cannot be empty.")

        if len(value) > 20:
            raise ValueError("Ticker is too long.")

        if not value.replace(".", "").replace("-", "").isalnum():
            raise ValueError("Ticker contains invalid characters.")

        return value
