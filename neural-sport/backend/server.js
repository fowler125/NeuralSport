const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

mongoose.connect('mongodb+srv://jabarif123:LQbjdqm0kp7kyJYn@cluster0.gzmna.mongodb.net/nba?retryWrites=true&w=majority', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => {
    console.log('Connected to MongoDB');
    app.listen(port, () => {
        console.log(`Server is running on port: ${port}`);
    });
})
.catch((error) => {
    console.error('Error connecting to MongoDB:', error);
});

// Define the schema and model
const gameSchema = new mongoose.Schema({
    gameId: String,
    homeTeam: {
        teamName: String,
        score: Number,
        periods: Array
    },
    awayTeam: {
        teamName: String,
        score: Number,
        periods: Array
    }
});

const Game = mongoose.model('Game', gameSchema);

// Define the /games endpoint
app.get('/games', async (req, res) => {
    try {
        const games = await Game.find();
        res.json(games);
    } catch (error) {
        console.error('Error fetching games:', error);
        res.status(500).send(error);
    }
});

// Add a default route to check if the server is running
app.get('/', (req, res) => {
    res.send('Server is running');
});