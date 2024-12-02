import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Papa from 'papaparse';
import * as d3 from 'd3';
import './PlayerProfile.css';

const PlayerProfile = () => {
  const { playerName } = useParams();
  const [playerData, setPlayerData] = useState(null);
  const [pitchArsenalData, setPitchArsenalData] = useState(null);
  const [zoneData, setZoneData] = useState(null);

  useEffect(() => {
    // Fetch and parse the CSV file for player stats
    fetch('/data/pitch_stats_2024_sorted.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            const playerStats = results.data.find(row => row.Name && row.Name.trim().toLowerCase() === playerName.trim().toLowerCase());
            if (playerStats) {
              setPlayerData(playerStats);
            } else {
              console.log('Player stats not found');
            }
          }
        });
      });

    // Fetch and parse the CSV file for pitch arsenal
    fetch('/data/pitch_arsenal_2024.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          dynamicTyping: true,
          complete: (results) => {
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
              setPitchArsenalData(playerData);
            } else {
              console.log('Player pitch arsenal not found');
            }
          }
        });
      });

    // Fetch and parse the CSV file for pitch data
    fetch(`/data/${playerName}.csv`)
      .then(response => response.text())
      .then(data => {
        const parsedData = d3.csvParse(data);
        createPitchZone(parsedData);
      });

    // Fetch and parse the CSV file for zone data
    fetch(`/data/${playerName}.csv`)
      .then(response => response.text())
      .then(data => {
        const parsedData = d3.csvParse(data);
        const zoneCounts = Array(15).fill(0);
        parsedData.forEach(d => {
          const zone = +d.zone;
          if (zone >= 1 && zone <= 14) {
            zoneCounts[zone]++;
          }
        });

        const totalPitches = parsedData.length;
        setZoneData({ zoneCounts, totalPitches });
      });

  }, [playerName]);

  useEffect(() => {
    if (zoneData) {
      drawHeatmap(zoneData.zoneCounts, zoneData.totalPitches);
    }
  }, [zoneData]);

  const displayPitchArsenal = (data) => {
    const pitchTypeMapping = {
      n_ff: 'Four-Seam Fastball',
      n_si: 'Sinker',
      n_fc: 'Cutter',
      n_sl: 'Slider',
      n_ch: 'Changeup',
      n_cu: 'Curveball',
      n_fs: 'Splitter',
      n_kn: 'Knuckleball',
      n_st: 'Sweeper',
      n_sv: 'Screwball'
    };

    return (
      <div className="pitch-arsenal">
        {Object.entries(data).map(([key, value]) => {
          if (key !== "last_name, first_name" && key !== "pitcher" && value) {
            const pitchName = pitchTypeMapping[key] || key;
            const pitchClass = key.replace('n_', 'pitch-');
            return <div key={key} className={`pitch-box ${pitchClass}`}><p>{pitchName}: {value}%</p></div>;
          }
          return null;
        })}
      </div>
    );
  };

  const createPitchZone = (data) => {
    const pitchTypeColors = {
      'FF': 'blue',
      'CU': 'orange',
      'SL': 'red',
      'CH': 'brown',
      'FC': 'purple',
      'SI': 'cyan',
      'KN': 'pink',
    };

    // Remove existing SVG if it exists
    d3.select('.model-container svg').remove();

    const xValues = data.map(d => parseFloat(d.plate_x)).filter(d => !isNaN(d));
    const yValues = data.map(d => parseFloat(d.plate_z)).filter(d => !isNaN(d));
    const xMin = Math.min(...xValues);
    const xMax = Math.max(...xValues);
    const yMin = Math.min(...yValues);
    const yMax = Math.max(...yValues);

    if (isNaN(xMin) || isNaN(xMax) || isNaN(yMin) || isNaN(yMax)) {
      console.error('Invalid data: Unable to calculate dimensions for the pitch zone.');
      return;
    }

    const width = (xMax - xMin) * 100 + 100;
    const height = (yMax - yMin) * 100 + 100;
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };

    const svg = d3.select('.model-container')
      .append('svg')
      .attr('width', 300)
      .attr('height', 500)
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleLinear()
      .domain([xMin, xMax])
      .range([0, width]);

    const yScale = d3.scaleLinear()
      .domain([yMin, yMax])
      .range([height, 0]);

    svg.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => xScale(d.plate_x))
      .attr('cy', d => yScale(d.plate_z))
      .attr('r', 5)
      .attr('fill', d => pitchTypeColors[d.pitch_type] || 'gray')
      .attr('opacity', 0.2);

    svg.append('rect')
      .attr('x', xScale(-0.7083))
      .attr('y', yScale(3.5))
      .attr('width', xScale(0.7083) - xScale(-0.7083))
      .attr('height', yScale(1.5) - yScale(3.5))
      .attr('stroke', 'black')
      .attr('fill', 'none');
  };

  const drawHeatmap = (zoneCounts, totalPitches) => {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) {
      console.error('Canvas element not found');
      return;
    }
    const ctx = canvas.getContext('2d');

    const colors = {
      lightBlue: "#a7c7e7",
      lightRed: "#ffb3b3",
      darkBlue: "#6b8eb5",
      darkRed: "#f28a8a",
      white: "#ffffff",
    };

    const grid = [
      [ { value: zoneCounts[1], color: colors.lightBlue }, { value: zoneCounts[2], color: colors.darkBlue }, { value: zoneCounts[3], color: colors.lightBlue } ],
      [ { value: zoneCounts[4], color: colors.lightBlue }, { value: zoneCounts[5], color: colors.darkRed }, { value: zoneCounts[6], color: colors.lightBlue } ],
      [ { value: zoneCounts[7], color: colors.darkBlue }, { value: zoneCounts[8], color: colors.white }, { value: zoneCounts[9], color: colors.darkBlue } ],
    ];

    const margin = 30;
    const cellSize = 70;
    const gridSize = cellSize * 3;
    const backgroundSize = gridSize + 50;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const centerX = margin + gridSize / 2;
    const centerY = margin + gridSize / 2;
    const halfBackgroundSize = backgroundSize / 2;

    const percentages = {
      11: (zoneCounts[11] / totalPitches) * 100,
      12: (zoneCounts[12] / totalPitches) * 100,
      13: (zoneCounts[13] / totalPitches) * 100,
      14: (zoneCounts[14] / totalPitches) * 100,
    };

    ctx.fillStyle = percentages[11] >= 7 ? colors.darkRed : percentages[11] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX - halfBackgroundSize, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize);

    ctx.fillStyle = percentages[12] >= 7 ? colors.darkRed : percentages[12] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize);

    ctx.fillStyle = percentages[13] >= 7 ? colors.darkRed : percentages[13] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX - halfBackgroundSize, centerY, halfBackgroundSize, halfBackgroundSize);

    ctx.fillStyle = percentages[14] >= 7 ? colors.darkRed : percentages[14] < 5 ? colors.darkBlue : colors.lightRed;
    ctx.fillRect(centerX, centerY, halfBackgroundSize, halfBackgroundSize);

    ctx.strokeStyle = "#000";
    ctx.lineWidth = 2;
    ctx.strokeRect(centerX - halfBackgroundSize, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize);
    ctx.strokeRect(centerX, centerY - halfBackgroundSize, halfBackgroundSize, halfBackgroundSize);
    ctx.strokeRect(centerX - halfBackgroundSize, centerY, halfBackgroundSize, halfBackgroundSize);
    ctx.strokeRect(centerX, centerY, halfBackgroundSize, halfBackgroundSize);

    for (let row = 0; row < grid.length; row++) {
      for (let col = 0; col < grid[row].length; col++) {
        const cell = grid[row][col];
        const x = margin + col * cellSize;
        const y = margin + row * cellSize;
        
        const percentage = (cell.value / totalPitches) * 100;

        if (percentage >= 7) {
          cell.color = colors.darkRed;
        } else if (percentage < 5) {
          cell.color = colors.darkBlue;
        } else {
          cell.color = colors.lightRed;
        }

        ctx.fillStyle = cell.color;
        ctx.fillRect(x, y, cellSize, cellSize);

        ctx.fillStyle = "#000";
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(cell.value, x + cellSize / 2, y + cellSize / 2);

        ctx.strokeStyle = "#000";
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, cellSize, cellSize);
      }
    }

    ctx.fillStyle = "#000";
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.fillText(zoneCounts[11], 40, 20);
    ctx.fillText(zoneCounts[12], 220, 20);
    ctx.fillText(zoneCounts[13], 40, 255);
    ctx.fillText(zoneCounts[14], 220, 255);
  };

  if (!playerData) {
    return <div>Loading...</div>;
  }

  const playerImage = `/assets/${playerData.Name.replace(/\s+/g, ' ')}.png`;

  return (
    <div className="content-container">
      <div className="profile-container">
        <img id="player-image" src={playerImage} alt={playerData.Name} className="player-image" />
        <div>
          <h1 id="player-name">{playerData.Name}</h1>
          <div id="player-stats" className="stats-container">
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
        </div>
      </div>
      <div className="arsenal-and-model-container">
        <div id="pitch-arsenal-container" className="pitch-arsenal-container">
          <h2 className="centered-title">Pitch Arsenal</h2>
          {pitchArsenalData && displayPitchArsenal(pitchArsenalData)}
        </div>
        <div className="model-container">
          <h2 className="centered-title">Spray Chart</h2>
        </div>
        <div className="zone-graphic-container">
          <h2 className="centered-title">Zone Graphic</h2>
          <canvas id="heatmapCanvas" width="300" height="300"></canvas>
          <div id="zone-graphic"></div>
        </div>
      </div>
    </div>
  );
};

export default PlayerProfile;