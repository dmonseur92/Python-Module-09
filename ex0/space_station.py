from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:

    print("Valid station created:")

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=10,
        power_level=80,
        oxygen_level=90,
        last_maintenance=datetime(2026, 8, 10, 14, 30),
        is_operational=True,
        notes="whatever",
        )

    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size}")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    print(f"Operational: {valid_station.is_operational}")

    print("\n=======================================")
    print("Expected validation error:")
    try:
        wrong_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=10,
            power_level=99,
            oxygen_level=101,
            last_maintenance=datetime(2026, 8, 10, 14, 30),
            is_operational=True,
            notes="whatever",
            )
        print(f"Crew: {wrong_station.crew_size}")
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("========================================\n")
    main()
