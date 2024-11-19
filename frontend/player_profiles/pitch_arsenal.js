document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const playerName = urlParams.get('player');
  console.log(playerName);
  if (playerName) {
    fetch('/data/unclean/pitch_arsenal_2024.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          dynamicTyping: true,
          complete: (results) => {
            // Remove the first column (row number) from each row
            const cleanedData = results.data.map(row => {
              delete row[""];
              return row;
            });

            const playerData = cleanedData.find(row => {
              const playerField = row["last_name, first_name"];
              if (playerField) {
                const [lastName, firstName] = playerField.split(', ');
                return playerField.includes(playerName) || `${firstName} ${lastName}`.includes(playerName);
              }
              return false;
            });

            if (playerData) {
              displayPitchArsenal(playerData);
            } else {
              console.log('Player pitch arsenal not found');
            }
          }
        });
      });
  }
});

const pitchTypeMapping = {
  n_ff: 'Four-Seam Fastball',
  n_si: 'Sinker',
  n_fc: 'Cutter',
  n_sl: 'Slider',
  n_ch: 'Changeup',
  n_cu: 'Curveball',
  n_fs: 'Splitter',
  n_kn: 'Knuckleball',
  n_st: 'Strike',
  n_sv: 'Screwball'
};

function displayPitchArsenal(data) {
  const pitchArsenalContainer = document.getElementById('pitch-arsenal-container');
  pitchArsenalContainer.innerHTML = `
    <h2>Pitch Arsenal</h2>
    <div class="pitch-arsenal">
      ${Object.entries(data).map(([key, value]) => {
        if (key !== "last_name, first_name" && key !== "pitcher" && value) {
          const pitchName = pitchTypeMapping[key] || key;
          const pitchClass = key.replace('n_', 'pitch-');
          return `<div class="pitch-box ${pitchClass}"><p>${pitchName}: ${value}%</p></div>`;
        }
        return '';
      }).join('')}
    </div>
  `;
}