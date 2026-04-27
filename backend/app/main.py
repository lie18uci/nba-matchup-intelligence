from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import Player
from app.schemas import PlayerCreate, PlayerResponse

Base.metadata.create_all(bind=engine)
app = FastAPI(title="NBA Matchup Intelligence API")

@app.get("/")
def root():
    return {"message": "NBA API is connected to Postgres"}


@app.post("/players", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    new_player = Player(
        nba_id=player.nba_id,
        full_name=player.full_name,
        team_abbreviation=player.team_abbreviation,
        position=player.position,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player


@app.get("/players", response_model=list[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.id).all()
    return players