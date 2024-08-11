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
    with open('key_count.json', 'r', encoding='utf-8') as file:
        key_count.update(json.load(file))
else:
    with open('key_count.json', 'w', encoding='utf-8') as file:
        file.write('{}')

# Identificar teclado numérico
num_pad_keys = {
    "0": 'num_0',
    "1": 'num_1',
    "2": 'num_2',
    "3": 'num_3',
    "4": 'num_4',
    "5": 'num_5',
    "6": 'num_6',
    "7": 'num_7',
    "8": 'num_8',
    "9": 'num_9',
    ",": 'num_decimal',
    "+": 'num_add',
    "-": 'num_subtract',
    "*": 'num_multiply',
    "/": 'num_divide',
}

def get_key_representation(key):
    try:
        if hasattr(key, 'vk'):
            print(f'Vk: {key.vk}')

            # Verifica se tecla é do teclado numérico
            if key.vk in [None, 65437, 65439]:
                if key.vk == None:
                    return num_pad_keys[key.char]
                elif key.vk == 65437:
                    return num_pad_keys["5"]
                elif key.vk == 65439:
                    return num_pad_keys[","]
                print(f'Teclado numérico! {key.char}')

            elif key.vk == 65027:
                return 'alt_gr'

        # Se for uma tecla de caractere, retorna o caractere
        if hasattr(key, 'char') and key.char:
            print(f'Key.char: {key.char}')
            return key.char.lower()
        elif hasattr(key, 'name'):
            print(f'Key.name: {key.name}')
            return key.name.lower()
        else:
            print(f'str(key): {str(key)}')
    except AttributeError:
        print(f'Except str(key): {str(key)}')
        return str(key)

def getKey(key):
    try:
        # Convertendo a tecla para string
        # Caso seja uma tecla presente em num_pad_keys, retorna o valor correspondente
        print(key.vk)
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
    key_str = get_key_representation(key)
    #return
    #key_str = getKey(key).lower()

    # Verifica se a tecla está sendo pressionada, evitando registrar várias vezes
    if key_str not in pressed_keys:
        pressed_keys.add(key_str)

        # Incrementando a contagem da tecla
        key_count[key_str] += 1

        # Salvando o resultado em um arquivo JSON a cada tecla pressionada (opcional)
        with open('key_count.json', 'w', encoding='utf-8') as file:
            json.dump(key_count, file, ensure_ascii=False, indent=4)

        # Exibindo a tecla e sua contagem (opcional)
        print(f"{key_str}: {key_count[key_str]}")

    #print(pressed_keys)

# Função chamada quando uma tecla é liberada
def on_release(key):

    key_str = get_key_representation(key)
    #return
    #key_str = getKey(key).lower()

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


# Configurando o listener para eventos do teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except:
        exit()
