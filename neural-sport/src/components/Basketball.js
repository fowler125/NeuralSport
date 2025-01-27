import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Basketball.css';

const teamLogos = {
    "Nets": "/assets/team_logos/brooklyn_nets.png",
    "Magic": "/assets/team_logos/orlando_magic.png",
    "Grizzlies": "/assets/team_logos/memphis_grizzlies.png",
    "Pacers": "/assets/team_logos/indiana_pacers.png",
    "Cavaliers": "/assets/team_logos/cleveland_cavaliers.png",
    "Celtics": "/assets/team_logos/boston_celtics.png",
    "Knicks": "/assets/team_logos/new_york_knicks.png",
    "Pelicans": "/assets/team_logos/new_orleans_pelicans.png",
    "Raptors": "/assets/team_logos/toronto_raptors.png",
    "Heat": "/assets/team_logos/miami_heat.png",
    "Rockets": "/assets/team_logos/houston_rockets.png",
    "Thunder": "/assets/team_logos/oklahoma_city_thunder.png",
    "Lakers": "/assets/team_logos/los_angeles_lakers.png",
    "Jazz": "/assets/team_logos/utah_jazz.png",
    "Mavericks": "/assets/team_logos/dallas_mavericks.png",
    "Trail Blazers": "/assets/team_logos/portland_trail_blazers.png",
    "Kings": "/assets/team_logos/sacramento_kings.png",
    "Spurs": "/assets/team_logos/san_antonio_spurs.png",
    "Nuggets": "/assets/team_logos/denver_nuggets.png",
    "Clippers": "/assets/team_logos/los_angeles_clippers.png",
    "Bucks": "/assets/team_logos/milwaukee_bucks.png",
    "Warriors": "/assets/team_logos/golden_state_warriors.png",
    "Hawks": "/assets/team_logos/atlanta_hawks.png",
    // Add other teams as needed
};

const Basketball = () => {
    const [games, setGames] = useState([]);
    const [hoveredGame, setHoveredGame] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:5000/games')
            .then(response => {
                console.log('Fetched games:', response.data); // Log the fetched data
                const gamesData = response.data[0].scoreboard.games; // Access the nested games array
                setGames(gamesData);
            })
            .catch(error => {
                console.error('There was an error fetching the games!', error);
            });
    }, []);

    const handleMouseEnter = (index) => {
        setHoveredGame(index);
    };

    const handleMouseLeave = () => {
        setHoveredGame(null);
    };

    return (
        <div>
            <div className="basketball-header">
                <h1>Basketball</h1>
            </div>
            <div className="basketball">
                <div className="category">
                    <a href="#">Live Games</a>
                    <a href="#">Upcoming Games</a>
                    <Link to="/stats">Stats</Link>
                </div>
                <div className="placques">
                    {games.map((game, index) => {
                        const homeScoreClass = game.homeTeam.score > game.awayTeam.score ? 'team-score bold' : 'team-score';
                        const awayScoreClass = game.awayTeam.score > game.homeTeam.score ? 'team-score bold' : 'team-score';

                        return (
                            <div
                                className={`game ${hoveredGame === index ? 'expanded' : 'collapsed'}`}
                                key={index}
                                onMouseEnter={() => handleMouseEnter(index)}
                                onMouseLeave={handleMouseLeave}
                            >
                                <div className="game-info">
                                    <div className="team-info">
                                        <img src={teamLogos[game.homeTeam.teamName]} alt={game.homeTeam.teamName} className="team-logo" />
                                        <div className="team-details">
                                            <h2>{game.homeTeam.teamName}</h2>
                                            <p className={homeScoreClass}>{game.homeTeam.score}</p>
                                        </div>
                                    </div>
                                    <div className="game-status">
                                        <p>{game.gameStatusText}</p>
                                    </div>
                                    <div className="team-info">
                                        <div className="team-details">
                                            <p className={awayScoreClass}>{game.awayTeam.score}</p>
                                            <h2>{game.awayTeam.teamName}</h2>
                                        </div>
                                        <img src={teamLogos[game.awayTeam.teamName]} alt={game.awayTeam.teamName} className="team-logo" />
                                    </div>
                                </div>
                                <div className="periods-container">
                                    <div className="periods-header">
                                        <div></div> {/* Empty div for spacing */}
                                        <div>Q1</div>
                                        <div>Q2</div>
                                        <div>Q3</div>
                                        <div>Q4</div>
                                    </div>
                                    <div className="periods">
                                        <div className="team-name">{game.homeTeam.teamName}</div>
                                        {game.homeTeam.periods.map((period, idx) => (
                                            <div key={idx} className="period-box">{period.score}</div>
                                        ))}
                                    </div>
                                    <div className="periods">
                                        <div className="team-name">{game.awayTeam.teamName}</div>
                                        {game.awayTeam.periods.map((period, idx) => (
                                            <div key={idx} className="period-box">{period.score}</div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}

export default Basketball;