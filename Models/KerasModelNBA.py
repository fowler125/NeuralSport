from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import *
from nba_api.stats.static import *
from datetime import datetime,timezone
from dateutil import parser
import pandas as pd
def grabScoreboard():
    f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

    board = scoreboard.ScoreBoard()
    print("ScoreBoardDate: " + board.score_board_date)
    games = board.games.get_dict()
    for game in games:
        gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))

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
    print(games)
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
    grabScoreboard() # This will print out the data from the NBA API
    ID = grabTeamID("Los Angeles Lakers") # This will print out the team ID for the Los Angeles Lakers
    gameFinder(ID)
    liveGames('0022400286')

if __name__ == "__main__":  
    main()
