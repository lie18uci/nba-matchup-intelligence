from pydantic import BaseModel, ConfigDict


class PlayerCreate(BaseModel):
    nba_id: int | None = None
    full_name: str
    team_abbreviation: str | None = None
    position: str | None = None


class PlayerResponse(BaseModel):
    id: int
    nba_id: int | None
    full_name: str
    team_abbreviation: str | None
    position: str | None
    model_config = ConfigDict(from_attributes=True)