from datetime import date

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


class PlayerGameLogCreate(BaseModel):
    game_date: date
    matchup: str
    team_abbreviation: str
    opponent_abbreviation: str
    minutes: float | None = None
    points: int = 0
    rebounds: int = 0
    assists: int = 0
    steals: int = 0
    blocks: int = 0
    turnovers: int = 0
    fg_made: int = 0
    fg_attempted: int = 0
    three_made: int = 0
    three_attempted: int = 0


class PlayerGameLogResponse(BaseModel):
    id: int
    player_id: int
    game_date: date
    matchup: str
    team_abbreviation: str
    opponent_abbreviation: str
    minutes: float | None
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fg_made: int
    fg_attempted: int
    three_made: int
    three_attempted: int

    model_config = ConfigDict(from_attributes=True)