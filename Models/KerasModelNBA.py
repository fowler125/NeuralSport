from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import *
from nba_api.stats.static import *
from datetime import datetime,timezone
from dateutil import parser
import pandas as pd
from pymongo import MongoClient
connection_string = 'connection_string_here'

def insert_games_to_db():
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client['nba']
        collection = db['games']

        # Fetch the latest scoreboard data
        board = scoreboard.ScoreBoard()
        games = board.get_dict()

        # Update the collection with the latest data
        collection.update_one({}, {"$set": games}, upsert=True)
        print("Games updated in MongoDB")
    except Exception as e:
        print("An error occured updating the games in MongodDB (Model File)", e)
    
def fetch_games_from_db():
    # Connect to MongoDB
    client = MongoClient(connection_string)
    db = client['nba']
    collection = db['games']

    # Fetch data from the collection
    games = list(collection.find())

    return games

def grabScoreboard():
    f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

    board = scoreboard.ScoreBoard()
    print("ScoreBoardDate: " + board.score_board_date)
    games = board.games.get_dict()
    for game in games:
        gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
    return games

def grabTeamID(tm):
    nba_teams = teams.get_teams()
    try:
        team = [team for team in nba_teams if team['full_name'] == tm][0]
    except:
        raise Exception(f"Team {tm} not found")
    
    return team['id']

def gameFinder(teamID):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamID)
    games = gamefinder.get_data_frames()[0]
    return games
def liveGames(gameID):
    box = boxscore.BoxScore(gameID)
    game_dict = box.game.get_dict()
    print("Full Games Keys:",game_dict.keys())
    print("Home Team Keys:",game_dict['homeTeam'].keys())
    periods = game_dict['homeTeam']['periods']
    periods_df = pd.DataFrame(periods)
    print(periods_df)
    

def main():
    board = grabScoreboard() # This will print out the data from the NBA API
    ID = grabTeamID("Los Angeles Lakers") # This will print out the team ID for the Los Angeles Lakers
    gameFinder(ID)


    

    # Insert games into MongoDB
    insert_games_to_db()

    # Fetch games from MongoDB
    games = fetch_games_from_db()
    

if __name__ == "__main__":  
    main()
