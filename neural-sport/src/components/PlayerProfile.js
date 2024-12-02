import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Papa from 'papaparse';

const PlayerProfile = () => {
  const { playerName } = useParams();
  const [playerData, setPlayerData] = useState(null);

  useEffect(() => {
    // Fetch and parse the CSV file
    fetch('/data/pitch_stats_2024_sorted.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            console.log('Parsed CSV data:', results.data); // Log the parsed CSV data
            const playerStats = results.data.find(row => row.Name && row.Name.trim().toLowerCase() === playerName.trim().toLowerCase());
            if (playerStats) {
              setPlayerData(playerStats);
            } else {
              console.log('Player stats not found');
              console.log('Player name:', playerName);
            }
          }
        });
      });
  }, [playerName]);

  if (!playerData) {
    return <div>Loading...</div>;
  }

  // Construct the image path based on the player's name
  const playerImage = `/assets/${playerData.Name.replace(/\s+/g, ' ')}.png`;

  return (
    <div>
      <h1>{playerData.Name}</h1>
      <img src={playerImage} alt={playerData.Name} className="player-image" />
      <div className="stat-box"><p>Age: {playerData.Age}</p></div>
      <div className="stat-box"><p>Team: {playerData.Tm}</p></div>
      <div className="stat-box"><p>Games: {playerData.G}</p></div>
      <div className="stat-box"><p>Wins: {playerData.W}</p></div>
      <div className="stat-box"><p>Losses: {playerData.L}</p></div>
      <div className="stat-box"><p>ERA: {playerData.ERA}</p></div>
      <div className="stat-box"><p>Strikeouts: {playerData.SO}</p></div>
      <div className="stat-box"><p>Innings Pitched: {playerData.IP}</p></div>
      <div className="stat-box"><p>mlbID: {playerData.mlbID}</p></div>
    </div>
  );
};

export default PlayerProfile;