from pynput import keyboard
from collections import defaultdict
import json
import os
import datetime

# Dicionário para armazenar contagem de teclas
key_count = defaultdict(int)

# Teclas atualmente pressionadas
pressed_keys = set()

# Carregar o arquivo JSON existente (se existir)
if os.path.exists('key_count.json'):
    with open('key_count.json', 'r') as file:
        key_count.update(json.load(file))

# Identificar teclado numérico
num_pad_keys = {
    96: 'num_0',
    97: 'num_1',
    98: 'num_2',
    99: 'num_3',
    100: 'num_4',
    101: 'num_5',
    102: 'num_6',
    103: 'num_7',
    104: 'num_8',
    105: 'num_9',
    110: 'num_decimal',
    107: 'num_add',
    109: 'num_subtract',
    106: 'num_multiply',
    111: 'num_divide',
    194: 'num_dot',
}

def getKey(key):
    try:
        # Convertendo a tecla para string
        if hasattr(key, 'vk') and key.vk in num_pad_keys:
            key_str = num_pad_keys[key.vk]
        else:
            key_str = key.char
        # Verifica se retorna None, quando utiliza o teclado numérico
        if key_str is not None:
            # Atribuir a tecla normal quando pressionada junto ao Shift
            if key_str == '"':
                key_str = "'"
            elif key_str == "!":
                key_str = "1"
            elif key_str == "@":
                key_str = "2"
            elif key_str == "#":
                key_str = "3"
            elif key_str == "$":
                key_str = "4"
            elif key_str == "%":
                key_str = "5"
            elif key_str == "¨":
                key_str = "6"
            elif key_str == "&":
                key_str = "7"
            elif key_str == "*":
                key_str = "8"
            elif key_str == "(":
                key_str = "9"
            elif key_str == ")":
                key_str = "0"
            elif key_str == "_":
                key_str = "-"
            elif key_str == "+":
                key_str = "="
            elif key_str == "`":
                key_str = "´"
            elif key_str == "{":
                key_str = "["
            elif key_str == "^":
                key_str = "~"
            elif key_str == "}":
                key_str = "]"
            elif key_str == "|":
                key_str = "\\"
            elif key_str == "<":
                key_str = ","
            elif key_str == ">":
                key_str = "."
            elif key_str == ":":
                key_str = ";"
            elif key_str == "?":
                key_str = "/"
        else:
            key_str = num_pad_keys[f'{key}']
    except AttributeError:
        if hasattr(key, 'vk') and key.vk in num_pad_keys:
            key_str = num_pad_keys[key.vk]
        else:
            # Tratando teclas especiais (e.g., Shift, Ctrl)
            key_str = str(key)
    return key_str


# Função chamada quando uma tecla é pressionada
def on_press(key):

    key_str = getKey(key)

    # Verifica se a tecla está sendo pressionada, evitando registrar várias vezes
    if key_str not in pressed_keys:
        pressed_keys.add(key_str)

        # Incrementando a contagem da tecla
        key_count[key_str] += 1

        # Salvando o resultado em um arquivo JSON a cada tecla pressionada (opcional)
        with open('key_count.json', 'w') as file:
            json.dump(key_count, file, ensure_ascii=False, indent=4)

        # Exibindo a tecla e sua contagem (opcional)
        print(f"{key_str}: {key_count[key_str]}")

    #print(pressed_keys)

# Função chamada quando uma tecla é liberada
def on_release(key):

    key_str = getKey(key)

    # Remove a tecla da lista de teclas pressionadas
    if key_str in pressed_keys:
        pressed_keys.remove(key_str)

    if key in pressed_keys:
        pressed_keys.remove(key)

    if str(key) in pressed_keys:
        pressed_keys.remove(str(key))

    if key == keyboard.Key.f7:
        # Parar o listener
        return False


# Configurando o listener para eventos do teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except:
        exit()