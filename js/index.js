// Função para carregar o arquivo JSON com a contagem de teclas
async function loadJson() {
    try {
        const response = await fetch('./scriptPython/key_count.json')
        const data = await response.json()
        return data
    } catch (error) {
        console.error(error)
    }
}

// Função para calcular a cor baseada na frequência
function getColor(frequency) {
    let ratio = 0
    let green = 0
    let blue = 0
    let red = 0
    let yellow = 0
    if (frequency <= 500) {
        ratio = frequency / 500
        yellow = Math.min(255, Math.floor(255 * ratio))
        green = 255
        blue = 255 - yellow
    } else {
        ratio = (frequency - 500) / 500
        red = Math.min(255, Math.floor(255 * ratio))
        green = 255 - red
    }
    return `rgb(255, ${green}, ${blue})`
}

// Função principal para atualizar a cor das teclas após carregar o JSON
async function updateKeyColors() {
    const keyFrequency = await loadJson()
    for (const [key, frequency] of Object.entries(keyFrequency)) {
        const keyElement = document.getElementById(`key-${key}`);
        if (keyElement) {
            keyElement.style.backgroundColor = getColor(frequency);
        }
    }
}

// Executar a função de atualização das cores quando a página estiver totalmente carregada
window.onload = updateKeyColors;
