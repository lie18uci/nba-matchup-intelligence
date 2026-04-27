from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import Player, PlayerGameLog
from app.schemas import (
    PlayerCreate,
    PlayerGameLogCreate,
    PlayerGameLogResponse,
    PlayerResponse,
)

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


@app.post(
    "/players/{player_id}/game-logs",
    response_model=PlayerGameLogResponse,
)
def create_player_game_log(
    player_id: int,
    game_log: PlayerGameLogCreate,
    db: Session = Depends(get_db),
):
    player = db.get(Player, player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    new_game_log = PlayerGameLog(
        player_id=player_id,
        game_date=game_log.game_date,
        matchup=game_log.matchup,
        team_abbreviation=game_log.team_abbreviation,
        opponent_abbreviation=game_log.opponent_abbreviation,
        minutes=game_log.minutes,
        points=game_log.points,
        rebounds=game_log.rebounds,
        assists=game_log.assists,
        steals=game_log.steals,
        blocks=game_log.blocks,
        turnovers=game_log.turnovers,
        fg_made=game_log.fg_made,
        fg_attempted=game_log.fg_attempted,
        three_made=game_log.three_made,
        three_attempted=game_log.three_attempted,
    )

    db.add(new_game_log)
    db.commit()
    db.refresh(new_game_log)

    return new_game_log


@app.get(
    "/players/{player_id}/game-logs",
    response_model=list[PlayerGameLogResponse],
)
def get_player_game_logs(
    player_id: int,
    db: Session = Depends(get_db),
):
    player = db.get(Player, player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    game_logs = (
        db.query(PlayerGameLog)
        .filter(PlayerGameLog.player_id == player_id)
        .order_by(PlayerGameLog.game_date.desc())
        .all()
    )

    return game_logs