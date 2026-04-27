from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

# Players
# - id
# - nba_id
# - full_name
#  team_abbreviation
# - position

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nba_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), index=True)
    team_abbreviation: Mapped[str | None] = mapped_column(String(10), nullable=True)
    position: Mapped[str | None] = mapped_column(String(20), nullable=True)