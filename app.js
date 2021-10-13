const express = require('express');
const app = express();
require('dotenv').config()
PORT = process.env.PORT || 3000

app.get('/subtitle',require('./downloadSub'))

app.listen(PORT, () => {
    console.log('listening on port '+PORT )
})