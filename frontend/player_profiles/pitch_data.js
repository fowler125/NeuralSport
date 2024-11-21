document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const playerName = urlParams.get('player');
  if (playerName) {
    // Fetch pitch data
    fetch(`/data/unclean/${playerName}.csv`)
      .then(response => response.text())
      .then(data => {
        const parsedData = d3.csvParse(data);
        createPitchZone(parsedData);
      });
  }
});

const pitchTypeColors = {
  'FF': 'blue',
  'CU': 'blue',
  'SL': 'green',
  'CH': 'orange',
  'FC': 'purple',
  'SI': 'cyan',
  'KN': 'pink',
  // Add more pitch types and their corresponding colors as needed
};

function createPitchZone(data) {
  // Calculate the required dimensions based on the data
  const xValues = data.map(d => parseFloat(d.plate_x)).filter(d => !isNaN(d));
  const yValues = data.map(d => parseFloat(d.plate_z)).filter(d => !isNaN(d));
  const xMin = Math.min(...xValues);
  const xMax = Math.max(...xValues);
  const yMin = Math.min(...yValues);
  const yMax = Math.max(...yValues);

  // Check if the calculated values are valid
  if (isNaN(xMin) || isNaN(xMax) || isNaN(yMin) || isNaN(yMax)) {
    console.error('Invalid data: Unable to calculate dimensions for the pitch zone.');
    return;
  }

  const width = (xMax - xMin) * 100 + 100; // Add some padding
  const height = (yMax - yMin) * 100 + 100; // Add some padding
  const margin = { top: 20, right: 20, bottom: 20, left: 20 };

  const svg = d3.select('.model-container')
    .append('svg')
    .attr('width', 300) // Set the desired width
    .attr('height', 500) // Set the desired height
    .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`) // Set the viewBox to scale the content
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // Define the scales
  const xScale = d3.scaleLinear()
    .domain([xMin, xMax])
    .range([0, width]);

  const yScale = d3.scaleLinear()
    .domain([yMin, yMax])
    .range([height, 0]);


  // Add the pitches
  svg.selectAll('circle')
    .data(data)
    .enter()
    .append('circle')
    .attr('cx', d => xScale(d.plate_x))
    .attr('cy', d => yScale(d.plate_z))
    .attr('r', 5)
    .attr('fill', d => pitchTypeColors[d.pitch_type] || 'gray') // Use the color mapping
    .attr('opacity', 0.5);
  
    // Add the strike zone rectangle
  svg.append('rect')
  .attr('x', xScale(-0.7083))
  .attr('y', yScale(3.5))
  .attr('width', xScale(0.7083) - xScale(-0.7083))
  .attr('height', yScale(1.5) - yScale(3.5))
  .attr('stroke', 'black')
  .attr('fill', 'none');
}