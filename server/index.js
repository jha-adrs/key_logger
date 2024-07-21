// Express server to recieve files from the devices
// Loads env files
const { config } = require('dotenv')
config()
const express = require('express');
const multer = require("multer");
const bodyParser = require('body-parser');
const { saveFile } = require('./scripts/storage');
const storage = multer.memoryStorage()
const uploader = multer({storage: storage});

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
//Uploads a single file
app.post("/upload", uploader.single("file"), async (req, res) => {
    //Check file type and size
    console.log("Received file", req.file);
    if (!req.file || !req.file.mimetype.includes("text")) {
        return res.status(400).send("Please upload a text file");
    }
    //Check file buffer
    if (!req.file.buffer) {
        return res.status(400).send("No file buffer found");
    }
    //Check if mac address
    if (!req.body?.mac_address) {
        return res.status(400).send("Please provide a mac address");
    }
    // Generate the file name based on devie macID
    const { mac_address } = req.body;
    const fileName = `${mac_address}-${req.file.originalname}`;

    //Store the file in cloud storage
    const response = await saveFile(req.file, mac_address);
    if (!response) {
        return res.status(500).send("Failed to save file");
    }
    return res.send("Received file");
});


app.listen(process.env.PORT, () => {
    console.log(`Server listening on port ${process.env.PORT}`);
});