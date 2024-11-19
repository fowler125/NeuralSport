// Get all the buttons in the .nft-list class
const buttons = document.querySelectorAll('.nft-list .item .bid a');

// Add an event listener to each button
buttons.forEach((button) => {
  button.addEventListener('click', (event) => {
    // Prevent the default link behavior
    event.preventDefault();

    const playerName = button.parentNode.parentNode.querySelector('.info h5').textContent;

    // Perform the desired action (e.g. navigate to a different page)
    console.log(`Button clicked for ${playerName}!`);
    window.location.href = 'player_profiles/players.html?player=' + encodeURIComponent(playerName);
  });
});

// Check if the current page is players.html
if (window.location.pathname.includes('players.html')) {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('players.html loaded');
    const urlParams = new URLSearchParams(window.location.search);
    const playerName = urlParams.get('player');
    console.log('Player name from URL:', playerName);
    if (playerName) {
      const playerNameElement = document.getElementById('player-name');
      playerNameElement.textContent = playerName;

      // Load and parse the CSV file
      fetch('/data/unclean/pitch_stats_2024_sorted.csv')
        .then(response => response.text())
        .then(csvText => {
          Papa.parse(csvText, {
            header: true,
            complete: (results) => {
              const playerStats = results.data.find(row => row.Name === playerName);
              if (playerStats) {
                displayPlayerStats(playerStats);
              } else {
                console.log('Player stats not found');
              }
            }
          });
        });
    }
  });
}

function displayPlayerStats(stats) {
  const playerStatsElement = document.getElementById('player-stats');
  playerStatsElement.innerHTML = `
    <div class="stat-box"><p>Age: ${stats.Age}</p></div>
    <div class="stat-box"><p>Team: ${stats.Tm}</p></div>
    <div class="stat-box"><p>Games: ${stats.G}</p></div>
    <div class="stat-box"><p>Wins: ${stats.W}</p></div>
    <div class="stat-box"><p>Losses: ${stats.L}</p></div>
    <div class="stat-box"><p>ERA: ${stats.ERA}</p></div>
    <div class="stat-box"><p>Strikeouts: ${stats.SO}</p></div>
    <div class="stat-box"><p>Innings Pitched: ${stats.IP}</p></div>
    <div class="stat-box"><p>mlbID: ${stats.mlbID}</p></div>
    <!-- Add more stats as needed -->
  `;
}