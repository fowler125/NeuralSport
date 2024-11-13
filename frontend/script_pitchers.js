// Read the CSV file
fetch('data/unclean/pitch_stats_2024.csv')
  .then(response => response.text())
  .then(data => {
    // Parse the CSV data
    const rows = data.split('\n');
    const pitchers = rows.slice(1).map(row => {
      const columns = row.split(',');
      return {
        name: columns[0],
        strikeouts: parseInt(columns[1])
      };
    });

    // Sort the pitchers by strikeouts
    pitchers.sort((a, b) => b.strikeouts - a.strikeouts);

    // Get the top 4 pitchers
    const topPitchers = pitchers.slice(0, 4);

    // Display the top pitchers in the nft-list class
    const pitcherNameElement = document.getElementById('pitcher-name');
    const strikeoutsElement = document.getElementById('strikeouts');
    const totalStrikeoutsElement = document.getElementById('total-strikeouts');

    topPitchers.forEach((pitcher, index) => {
      pitcherNameElement.textContent = pitcher.name;
      strikeoutsElement.textContent = `${pitcher.strikeouts} BTC`;
      totalStrikeoutsElement.textContent = `Total Strikeouts: ${pitcher.strikeouts}`;

      // Clone the item element
      const itemElement = document.querySelector('.item').cloneNode(true);

      // Append the cloned item element to the nft-list class
      document.querySelector('.nft-list').appendChild(itemElement);
    });
  });