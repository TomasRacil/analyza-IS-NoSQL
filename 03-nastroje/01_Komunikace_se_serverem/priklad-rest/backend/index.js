// Importujeme Express framework
const express = require('express');
// Vytvoříme instanci Express aplikace
const app = express();
// Port, na kterém bude server naslouchat
const port = 3000;

// Middleware pro parsování JSON těla požadavků
// Umožňuje nám číst data poslaná v těle POST/PUT požadavků ve formátu JSON
app.use(express.json());

// Jednoduchá databáze v paměti pro ukládání úkolů
// V reálné aplikaci by zde byla integrace s databází (SQL, NoSQL)
let tasks = [
    { id: 1, title: 'Příklad úkolu 1', completed: false },
    { id: 2, title: 'Příklad úkolu 2', completed: true },
];
// Proměnná pro generování unikátních ID pro nové úkoly
let nextId = tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1;

// --- Definice API endpointů (Routes) ---

// GET /tasks - Získání všech úkolů
app.get('/tasks', (req, res) => {
    // Odešle seznam všech úkolů jako JSON odpověď
    res.json(tasks);
});

// GET /tasks/:id - Získání konkrétního úkolu podle ID
app.get('/tasks/:id', (req, res) => {
    // Získáme ID z parametrů URL a převedeme ho na číslo
    const taskId = parseInt(req.params.id, 10);
    // Najdeme úkol v poli 'tasks'
    const task = tasks.find(t => t.id === taskId);

    if (task) {
        // Pokud úkol existuje, odešleme ho jako JSON odpověď
        res.json(task);
    } else {
        // Pokud úkol neexistuje, odešleme stavový kód 404 (Not Found)
        res.status(404).send('Úkol nebyl nalezen.');
    }
});

// POST /tasks - Vytvoření nového úkolu
app.post('/tasks', (req, res) => {
    // Získáme data nového úkolu z těla požadavku (očekáváme JSON)
    const { title, completed = false } = req.body; // completed je volitelné, výchozí hodnota false

    // Jednoduchá validace - název úkolu musí být přítomen
    if (!title) {
        return res.status(400).send('Název úkolu (title) je povinný.');
    }

    // Vytvoříme nový objekt úkolu
    const newTask = {
        id: nextId++, // Přiřadíme unikátní ID a inkrementujeme nextId pro další úkol
        title,
        completed
    };

    // Přidáme nový úkol do našeho pole 'tasks'
    tasks.push(newTask);
    // Odešleme nově vytvořený úkol jako JSON odpověď se stavovým kódem 201 (Created)
    res.status(201).json(newTask);
});

// PUT /tasks/:id - Aktualizace existujícího úkolu
app.put('/tasks/:id', (req, res) => {
    const taskId = parseInt(req.params.id, 10);
    const { title, completed } = req.body;
    const taskIndex = tasks.findIndex(t => t.id === taskId);

    if (taskIndex !== -1) {
        // Pokud úkol existuje, aktualizujeme jeho vlastnosti
        // Použijeme existující hodnoty, pokud nejsou v požadavku specifikovány nové
        tasks[taskIndex].title = title !== undefined ? title : tasks[taskIndex].title;
        tasks[taskIndex].completed = completed !== undefined ? completed : tasks[taskIndex].completed;
        res.json(tasks[taskIndex]);
    } else {
        res.status(404).send('Úkol nebyl nalezen pro aktualizaci.');
    }
});

// DELETE /tasks/:id - Smazání úkolu
app.delete('/tasks/:id', (req, res) => {
    const taskId = parseInt(req.params.id, 10);
    const initialLength = tasks.length;
    // Odfiltrujeme úkol, který má být smazán
    tasks = tasks.filter(t => t.id !== taskId);

    if (tasks.length < initialLength) {
        // Pokud byl úkol úspěšně smazán (délka pole se zmenšila)
        // Odešleme stavový kód 204 (No Content), který signalizuje úspěšné smazání bez těla odpovědi
        res.status(204).send();
    } else {
        // Pokud úkol s daným ID nebyl nalezen
        res.status(404).send('Úkol nebyl nalezen pro smazání.');
    }
});

// Spuštění serveru a naslouchání na zadaném portu
app.listen(port, () => {
    console.log(`API server běží na http://localhost:${port}`);
});
