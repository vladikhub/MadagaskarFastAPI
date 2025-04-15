import phonenumbers
from pydantic import BaseModel, Field, field_validator


class ClientAdd(BaseModel):
    name: str = Field(description="Введите имя")
    phone: str = Field(description="Введите номер телефона")

    @field_validator('phone')
    def validate_phone(cls, v):
        try:
            parsed = phonenumbers.parse(v, "RU")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone format")

class Client(ClientAdd):
    id: int