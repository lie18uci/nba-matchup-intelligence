import time
from datetime import datetime
from nba_api.stats.endpoints import playergamelog
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.models import Player, PlayerGameLog


def parse_opponent(matchup: str) -> str:
    """
    Examples:
    'OKC vs. MEM' -> 'MEM'
    'OKC @ LAL'   -> 'LAL'
    """
    if " vs. " in matchup:
        return matchup.split(" vs. ")[1].strip()

    if " @ " in matchup:
        return matchup.split(" @ ")[1].strip()

    return "UNKNOWN"


def load_player_logs(
    db: Session,
    player_name: str,
    nba_player_id: int,
    team_abbreviation: str,
    position: str,
    season: str,
):
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    # Find or create player in our database
    player = db.query(Player).filter(Player.nba_id == nba_player_id).first()

    if player is None:
        player = Player(
            nba_id=nba_player_id,
            full_name=player_name,
            team_abbreviation=team_abbreviation,
            position=position,
        )
        db.add(player)
        db.commit()
        db.refresh(player)

    print(f"Loading game logs for {player.full_name} ({season})...")

    # Pull game logs from NBA API
    logs = playergamelog.PlayerGameLog(
        player_id=nba_player_id,
        season=season,
        season_type_all_star="Regular Season",
    )

    df = logs.get_data_frames()[0]

    print(f"Fetched {len(df)} rows")

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        game_date = datetime.strptime(row["GAME_DATE"], "%b %d, %Y").date()
        matchup = row["MATCHUP"]
        opponent = parse_opponent(matchup)

        # Avoid duplicate rows for same player/game/date
        existing = (
            db.query(PlayerGameLog)
            .filter(PlayerGameLog.player_id == player.id)
            .filter(PlayerGameLog.game_date == game_date)
            .filter(PlayerGameLog.matchup == matchup)
            .first()
        )

        if existing:
            skipped += 1
            continue

        game_log = PlayerGameLog(
            player_id=player.id,
            game_date=game_date,
            matchup=matchup,
            team_abbreviation=team_abbreviation,
            opponent_abbreviation=opponent,
            minutes=float(row["MIN"]) if row["MIN"] is not None else None,
            points=int(row["PTS"]),
            rebounds=int(row["REB"]),
            assists=int(row["AST"]),
            steals=int(row["STL"]),
            blocks=int(row["BLK"]),
            turnovers=int(row["TOV"]),
            fg_made=int(row["FGM"]),
            fg_attempted=int(row["FGA"]),
            three_made=int(row["FG3M"]),
            three_attempted=int(row["FG3A"]),
        )

        db.add(game_log)
        inserted += 1

    db.commit()

    print(f"Inserted {inserted} new rows")
    print(f"Skipped {skipped} existing rows")


def main():
    db = SessionLocal()

    try:
        # Start with one player so debugging is easy.
        # Shai Gilgeous-Alexander NBA ID = 1628983
        load_player_logs(
            db=db,
            player_name="Shai Gilgeous-Alexander",
            nba_player_id=1628983,
            team_abbreviation="OKC",
            position="Guard",
            season="2023-24",
        )

        # Be polite to the API if you add more players later.
        time.sleep(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()