import express from 'express'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { createServer } from 'node:http'

const app = express()
const server = createServer(app)

const __dirname = dirname(fileURLToPath(import.meta.url))
app.use(express.static(__dirname)) // Servir o diretório atual

app.get('/', (req, res) => {
    res.sendFile(join(__dirname, 'index.html'))
})

server.listen(3000, () => {
    console.log('Servidor rodando na porta 3000')
})
