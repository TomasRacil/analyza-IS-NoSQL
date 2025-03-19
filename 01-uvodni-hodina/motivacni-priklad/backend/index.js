const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors'); // Importujeme CORS

const app = express();
const port = 3000;
const mongoUrl = process.env.MONGO_URL || 'mongodb://localhost:27017'; // Použije proměnnou prostředí, nebo výchozí hodnotu
const dbName = 'mydatabase'; // Název databáze
const collectionName = 'items';

// Povolíme CORS pro všechny origins (pro jednoduchost; v produkci omezte!)
app.use(cors());
app.use(express.json()); // Middleware pro parsování JSON těla requestu

async function connectToMongo() {
    const client = new MongoClient(mongoUrl);
    try {
        await client.connect();
        console.log('Připojeno k MongoDB');
        return client.db(dbName);
    } catch (error) {
        console.error('Chyba při připojování k MongoDB:', error);
        throw error; // Rethrow the error to stop the application
    }
}
let db;
(async () => {
    try {
        db = await connectToMongo();
    } catch (error) {
        // Error is already logged in connectToMongo, just exit
        process.exit(1); // Exit with an error code
    }
})();

// Endpoint pro získání všech položek
app.get('/items', async (req, res) => {
    try {
        const items = await db.collection(collectionName).find({}).toArray();
        res.json(items);
    } catch (err) {
        console.error('Error fetching items:', err);
        res.status(500).send('Internal Server Error');
    }
});

// Endpoint pro přidání nové položky
app.post('/items', async (req, res) => {
    try {
        const newItem = req.body; // Získání dat z těla requestu
        // Zde by měla být validace dat!!!
        const result = await db.collection(collectionName).insertOne(newItem);
        res.status(201).json(result); // 201 Created
    } catch (err) {
        console.error('Error adding item:', err);
        res.status(500).send('Internal Server Error');
    }
});

app.listen(port, () => {
    console.log(`Server běží na portu ${port}`);
});