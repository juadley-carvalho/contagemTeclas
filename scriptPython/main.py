from pynput import keyboard
from collections import defaultdict
import json
import os

# Dicionário para armazenar contagem de teclas
key_count = defaultdict(int)

# Teclas atualmente pressionadas (evitar vários registros de uma tecla mantida pressionada)
pressed_keys = set()

# Tecla para parada do script
stop_key = keyboard.Key.f7

# Carregar o arquivo JSON, se existir, ou cria um arquivo vazio
if os.path.exists('key_count.json'):
    with open('key_count.json', 'r', encoding='windows-1252') as file:
        key_count.update(json.load(file))
else:
    with open('key_count.json', 'w', encoding='utf-8') as file:
        file.write('{}')

# Identificar teclado numérico
# e teclas que são pressionadas junto ao Ctrl
num_pad_keys = {
    65: 'a',
    67: 'c',
    83: 's',
    86: 'v',
    88: 'x',
    90: 'z',
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
        # print(f'Key: {str(key)} {str(key) == "<97>"}')
        # if hasattr(key, 'vk'):
        #     print(f'Vk: {key.vk}')
        # if hasattr(key, 'char'):
        #     print(f'Char: {key.char}')
        # if hasattr(key, 'name'):
        #     print(f'Name: {key.name}')
        # return
        # Convertendo a tecla para string
        # Caso seja uma tecla presente em num_pad_keys, retorna o valor correspondente
        # print(key.vk)
        if hasattr(key, 'vk') and key.vk in num_pad_keys:
            key_str = num_pad_keys[key.vk]
        else:
            key_str = key.char

        # Verifica se retorna None (ao utilizar Shift, Ctrl, etc.)
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

    key_str = getKey(key).lower()

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

    key_str = getKey(key).lower()

    # Remove a tecla da lista de teclas pressionadas
    if key_str in pressed_keys:
        pressed_keys.remove(key_str)

    if key in pressed_keys:
        pressed_keys.remove(key)

    if str(key).lower() in pressed_keys:
        pressed_keys.remove(str(key).lower())

    if key == stop_key:
        # Parar o listener
        return False

print('Monitorando as teclas...')
# Configurando o listener para eventos do teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except:
        exit()