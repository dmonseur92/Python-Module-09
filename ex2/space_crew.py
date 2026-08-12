from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        leader: bool = False
        experienced: int = 0
        for member in self.crew:
            if member.rank is Rank.COMMANDER or member.rank is Rank.CAPTAIN:
                leader = True
            if member.years_experience >= 5:
                experienced += 1
            if member.is_active is False:
                raise ValueError('All crew members must be active')
        if leader is False:
            raise ValueError('Must have at least one Commander or Captain')
        if self.duration_days > 365 and experienced < len(self.crew)/2:
            raise ValueError('Long missions (> 365 days) need '
                             '50% experienced crew (5+ years)')
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    Sarah = CrewMember(
        member_id="SC001",
        name="Sarah Connor",
        rank=Rank.COMMANDER,
        age=30,
        specialization="Mission Command",
        years_experience=15,
        is_active=True
    )

    John = CrewMember(
        member_id="JS007",
        name="John Smith",
        rank=Rank.LIEUTENANT,
        age=40,
        specialization="Navigation",
        years_experience=20,
        is_active=True
    )

    Alice = CrewMember(
        member_id="AL202",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=21,
        specialization="Engineering",
        years_experience=2,
        is_active=True
    )

    mars_attack = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 8, 10, 14, 30),
        duration_days=900,
        crew=[Sarah, John, Alice],
        mission_status="planned",
        budget_millions=2500.0
    )
    print("Valid mission created:")
    print(f"Mission: {mars_attack.mission_name}")
    print(f"ID: {mars_attack.mission_id}")
    print(f"Destination: {mars_attack.destination}")
    print(f"Duration: {mars_attack.duration_days}")
    print(f"Budget: ${mars_attack.budget_millions}M")
    print(f"Crew size: ${len(mars_attack.crew)}")
    print("Crew members: ")
    for member in mars_attack.crew:
        print(f"- {member.name}({member.rank.value})"
              f" - {member.specialization}")

    print("=========================================")
    print("Expected validation error:")
    try:
        # Alice2 = CrewMember(
        #         member_id="A",
        #         name="Alice Johnson",
        #         rank=Rank.OFFICER,
        #         age=21,
        #         specialization="Engineering",
        #         years_experience=2,
        #         is_active=True
        #     )

        invalid_mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime(2024, 8, 10, 14, 30),
                duration_days=100,
                crew=[Alice, Alice, Alice],
                mission_status="planned",
                budget_millions=2500.0
            )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
