from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(
        default=None,
        max_length=500,
    )
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_attribute(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "Contact ID must start with 'AC' (Alien Contact)"
            )

        if (
            self.contact_type == ContactType.PHYSICAL
            and self.is_verified is False
        ):
            raise ValueError(
                "Physical contact reports must be verified"
            )

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if (
            self.signal_strength > 7.0
            and self.message_received is None
        ):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


if __name__ == "__main__":

    try:
        radio = AlienContact(
                contact_id="AC_2024_001",
                timestamp=datetime(2024, 8, 10, 14, 30),
                location="Area 51, Nevada",
                contact_type=ContactType.RADIO,
                signal_strength=8.5,
                duration_minutes=45,
                witness_count=5,
                message_received="Greetings from Zeta Reticuli",
                is_verified=True,
            )

        print("Alien Contact Log Validation")
        print("======================================")
        print("Valid contact report:")
        print(f"ID: {radio.contact_id}")
        print(f"Type: {radio.contact_type.value}")
        print(f"Location: {radio.location}")
        print(f"Signal: {radio.signal_strength}/10")
        print(f"Duration: {radio.duration_minutes} minutes")
        print(f"Witnesses: {radio.witness_count}")
        print(f"Message: {radio.message_received}")

        print("\n=======================================")
        print("Expected validation error:")

        telepathic = AlienContact(
            contact_id="AC_2025_001",
            timestamp=datetime(2025, 12, 10, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zita Ritecule",
            is_verified=True,
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
