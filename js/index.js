// Inclui eventos de mouse nas teclas
document.querySelectorAll('.key').forEach( key => {
    key.addEventListener('mouseover', showCount)
    key.addEventListener('mouseout', restoreKey)
})

// Funções para mostrar contagem das teclas
function showCount(event) {
    const keyElement = event.target
    const originalText = keyElement.innerHTML
    const count = keyElement.getAttribute('data-count')
    keyElement.setAttribute('data-original', originalText)
    keyElement.innerHTML = count
}

function restoreKey(event) {
    const keyElement = event.target
    keyElement.innerHTML = keyElement.getAttribute('data-original')
}

// Função para carregar o arquivo JSON com a contagem de teclas
async function loadJson() {
    try {
        // const response = await fetch('./scriptPython/key_count.json')
        // const blob = await response.blob()
        // const text = await blob.text()
        // const decoder = new TextDecoder('utf-8')
        // const decodedText = decoder.decode(new TextEncoder().encode(text))
        // //const data = await response.json()
        // const data = JSON.parse(decodedText)
        // return data
        const response = await fetch('./scriptPython/key_count.json');
        const arrayBuffer = await response.arrayBuffer();
        const decoder = new TextDecoder('windows-1252');
        const decodedText = decoder.decode(arrayBuffer);
        const data = JSON.parse(decodedText);
        return data;
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
        console.log(`${key} : ${frequency}`)
        const keyElement = document.getElementById(`key-${key}`)
        if (keyElement) {
            keyElement.style.backgroundColor = getColor(frequency)
            keyElement.setAttribute('data-count', frequency)
        }
    }
}

// Executar a função de atualização das cores quando a página estiver totalmente carregada
window.onload = updateKeyColors
