document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('heatmapCanvas');
  const ctx = canvas.getContext('2d');

  // Colors for different zones
  const colors = {
    lightBlue: "#a7c7e7",
    lightRed: "#ffb3b3",
    darkBlue: "#6b8eb5",
    darkRed: "#f28a8a",
    white: "#ffffff",
  };

  // Initialize grid data with default values and colors
  const grid = [
    [ { value: 0, color: colors.lightBlue }, { value: 0, color: colors.darkBlue }, { value: 0, color: colors.lightBlue } ],
    [ { value: 0, color: colors.lightBlue }, { value: 0, color: colors.darkRed }, { value: 0, color: colors.lightBlue } ],
    [ { value: 0, color: colors.darkBlue }, { value: 0, color: colors.white }, { value: 0, color: colors.darkBlue } ],
  ];

  // Margins and dimensions for grid
  const margin = 30; // space for grid around the canvas
  const cellSize = 70; // size of each grid cell
  const gridSize = cellSize * 3; // size of the entire grid
  const backgroundSize = gridSize + 50; // size of the background squares (slightly bigger than the grid)

  // Function to draw the heatmap grid and the background quadrants
  function drawHeatmap(zoneCounts, totalPitches) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    // Draw the background squares
    const centerX = margin + gridSize / 2;
    const centerY = margin + gridSize / 2;
    const halfBackgroundSize = backgroundSize / 2;

    // Calculate the percentage of total pitches for each outside zone
    const percentages = {
      11: (zoneCounts[11] / totalPitches) * 100,
      12: (zoneCounts[12] / totalPitches) * 100,
      13: (zoneCounts[13] / totalPitches) * 100,
      14: (zoneCounts[14] / totalPitches) * 100,
    };

    // Set the fill color for each outside zone based on the percentage
    ctx.fillStyle = percentages[11] >= 7 ? colors.darkRed : percentages[11] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX - halfBackgroundSize, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize); // Top-left

    ctx.fillStyle = percentages[12] >= 7 ? colors.darkRed : percentages[12] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize); // Top-right

    ctx.fillStyle = percentages[13] >= 7 ? colors.darkRed : percentages[13] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX - halfBackgroundSize, centerY, halfBackgroundSize, halfBackgroundSize); // Bottom-left

    ctx.fillStyle = percentages[14] >= 7 ? colors.darkRed : percentages[14] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX, centerY, halfBackgroundSize, halfBackgroundSize); // Bottom-right

    // Draw stroke lines for the background squares
    ctx.strokeStyle = "#000"; // Set stroke color to black
    ctx.lineWidth = 2; // Set stroke width to 2
    ctx.strokeRect(centerX - halfBackgroundSize, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize); // Top-left
    ctx.strokeRect(centerX, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize); // Top-right
    ctx.strokeRect(centerX - halfBackgroundSize, centerY, halfBackgroundSize, halfBackgroundSize); // Bottom-left
    ctx.strokeRect(centerX, centerY, halfBackgroundSize, halfBackgroundSize); // Bottom-right

    // Draw the grid cells with their respective colors and values
    for (let row = 0; row < grid.length; row++) {
      for (let col = 0; col < grid[row].length; col++) {
        const cell = grid[row][col];
        const x = margin + col * cellSize;
        const y = margin + row * cellSize;
        
        // Calculate the percentage of total pitches for this cell
        const percentage = (cell.value / totalPitches) * 100;

        // Set the cell color based on the percentage
        if (percentage >= 7) {
          cell.color = colors.darkRed;
        } else if (percentage < 5) {
          cell.color = colors.darkBlue;
        } else {
          cell.color = colors.lightRed; // Default color for other percentages
        }

        // Draw the cell background color
        ctx.fillStyle = cell.color;
        ctx.fillRect(x, y, cellSize, cellSize);

        // Draw the cell value
        ctx.fillStyle = "#000"; // Text color
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(cell.value, x + cellSize / 2, y + cellSize / 2);

        // Draw the cell border
        ctx.strokeStyle = "#000"; // Set stroke color to black
        ctx.lineWidth = 2; // Set stroke width to 2
        ctx.strokeRect(x, y, cellSize, cellSize);
      }
    }

    // Draw the outside zone numbers (11-14)
    ctx.fillStyle = "#000"; // Text color
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Zone 11 (Top-left)
    ctx.fillText(zoneCounts[11], 40, 20);

    // Zone 12 (Top-right)
    ctx.fillText(zoneCounts[12], 220, 20);

    // Zone 13 (Bottom-left)
    ctx.fillText(zoneCounts[13], 40, 255);

    // Zone 14 (Bottom-right)
    ctx.fillText(zoneCounts[14], 220, 255);
    console.log(zoneCounts[11], zoneCounts[12], zoneCounts[13], zoneCounts[14]);
  }

  // Fetch and parse the CSV file based on first and last name
  const urlParams = new URLSearchParams(window.location.search);
  const playerName = urlParams.get('player');
  if (playerName) {
    

    fetch(`/data/unclean/${playerName}.csv`)
      .then(response => response.text())
      .then(data => {
        const parsedData = d3.csvParse(data);

        // Count the number of pitches in each zone (1-14)
        const zoneCounts = Array(15).fill(0);
        parsedData.forEach(d => {
          const zone = +d.zone;
          if (zone >= 1 && zone <= 14) {
            zoneCounts[zone]++;
          }
        });

        const totalPitches = parsedData.length;
        console.log(totalPitches);

        // Update the grid cells with the counts of pitches in each zone
        grid[0][0].value = zoneCounts[1];
        grid[0][1].value = zoneCounts[2];
        grid[0][2].value = zoneCounts[3];
        grid[1][0].value = zoneCounts[4];
        grid[1][1].value = zoneCounts[5];
        grid[1][2].value = zoneCounts[6];
        grid[2][0].value = zoneCounts[7];
        grid[2][1].value = zoneCounts[8];
        grid[2][2].value = zoneCounts[9];

        // Draw the heatmap
        drawHeatmap(zoneCounts,totalPitches);
      });
  }
});