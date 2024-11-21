// strikeouts.js
async function loadStrikeoutLeaders() {
    try {
        // Fetch the CSV file
        const response = await fetch('/data/unclean/pitch_stats_2024_sorted.csv');
        const data = await response.text();
        
        // Parse CSV data
        const rows = data.split('\n');
        const headers = rows[0].split(',');
        const specialCharRegex = /[^\x00-\x7F]/;
        
        const players = rows.slice(1) // Skip header row
            .filter(row => row.trim() !== '') // Filter out empty rows
            .map(row => {
                const name = row.match(/^(\d+),([^,]+)/g)[0].replace(/^(\d+),/, '');
                const columns = row.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g); // Regex to handle commas inside quotes
                const rawName = columns[1].replace(/^\d+,/, ''); // Remove leading number if present
                
                if(specialCharRegex.test(name)){
                    console.log('Special character found in name:', name);
                }
                
                let teams = columns[5].replace(/"/g, ''); // Remove extra quotes if present
                if (teams.includes(',')) {
                    teams = teams.split(',').join(' / '); // Join multiple teams with " / "
                }
                

                return {
                    name: name,
                    age: parseInt(columns[2]),
                    team: teams, // Display both teams if present
                    games: parseInt(columns[6]),
                    inningsPitched: parseFloat(columns[10]),
                    strikeouts: parseInt(columns[15]) || 0, // Use 0 if NaN
                    era: parseFloat(columns[18]),
                    strikeoutsPer9: parseFloat(columns[38]),
                    whip: parseFloat(columns[37])
                };
            })
            .filter(player => player.strikeouts > 0); // Filter out players with 0 or NaN strikeouts
            console.log(players);
        // Display players as usual
        displayPlayers(players.slice(0, 10));

        
        // Store all players for view more functionality
        window.allPlayers = players;
        window.currentlyShowing = 10;
    } catch (error) {
        console.error('Error loading data:', error);
        document.querySelector('.profile-container').innerHTML = 
            '<p class="error-message">Error loading strikeout leaders. Please try again later.</p>';
    }
}

function displayPlayers(players) {
    const container = document.querySelector('.profile-container');
    
    // Create leaders table
    const tableHTML = `
        <h1>MLB Strikeout Leaders</h1>
        <div class="leaders-table">
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Age</th>
                        <th>Team</th>
                        <th>G</th>
                        <th>IP</th>
                        <th class="sorted">SO ↓</th>
                        <th>ERA</th>
                        <th>K/9</th>
                        <th>WHIP</th>
                    </tr>
                </thead>
                <tbody>
                    ${players.map((player, index) => `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${player.name}</td>
                            <td>${player.age}</td>
                            <td>${player.team}</td>
                            <td>${player.games}</td>
                            <td>${player.inningsPitched.toFixed(1)}</td>
                            <td class="highlight">${player.strikeouts}</td>
                            <td>${player.era.toFixed(2)}</td>
                            <td>${player.strikeoutsPer9.toFixed(1)}</td>
                            <td>${player.whip.toFixed(3)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        <div class="view-more-container">
            <button id="viewMoreBtn" class="view-more-btn">View More</button>
        </div>
    `;
    
    container.innerHTML = tableHTML;
    
    // Add view more button functionality
    document.getElementById('viewMoreBtn').addEventListener('click', viewMore);
}

/**
 * Shows the next 10 players in the strikeout leaders table when the "View More" button is clicked.
 * Hides the button if all players have been shown.
 */
function viewMore() {
    if (window.currentlyShowing >= window.allPlayers.length) {
        document.getElementById('viewMoreBtn').style.display = 'none';
        return;
    }
    
    // Show next 10 players
    const nextBatch = window.allPlayers.slice(0, window.currentlyShowing + 10);
    displayPlayers(nextBatch);
    window.currentlyShowing += 10;
    
    // Hide button if we've shown all players
    if (window.currentlyShowing >= window.allPlayers.length) {
        document.getElementById('viewMoreBtn').style.display = 'none';
    }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadStrikeoutLeaders);