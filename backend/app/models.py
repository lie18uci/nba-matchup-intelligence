from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nba_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), index=True)
    team_abbreviation: Mapped[str | None] = mapped_column(String(10), nullable=True)
    position: Mapped[str | None] = mapped_column(String(20), nullable=True)

class PlayerGameLog(Base):
    __tablename__ = "player_game_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("players.id"),
        index=True,
        nullable=False,
    )

    game_date: Mapped[Date] = mapped_column(Date, index=True)
    matchup: Mapped[str] = mapped_column(String(50))

    team_abbreviation: Mapped[str] = mapped_column(String(10))
    opponent_abbreviation: Mapped[str] = mapped_column(String(10))

    minutes: Mapped[float | None] = mapped_column(Float, nullable=True)

    points: Mapped[int] = mapped_column(Integer, default=0)
    rebounds: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    steals: Mapped[int] = mapped_column(Integer, default=0)
    blocks: Mapped[int] = mapped_column(Integer, default=0)
    turnovers: Mapped[int] = mapped_column(Integer, default=0)

    fg_made: Mapped[int] = mapped_column(Integer, default=0)
    fg_attempted: Mapped[int] = mapped_column(Integer, default=0)
    three_made: Mapped[int] = mapped_column(Integer, default=0)
    three_attempted: Mapped[int] = mapped_column(Integer, default=0)