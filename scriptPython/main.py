from pynput import keyboard
from collections import defaultdict
import json
import os
import datetime

#Dicionário para armazenar contagem de teclas
key_count = defaultdict(int)

# Carregar o arquivo JSON existente (se existir)
if os.path.exists('key_count.json'):
    with open('key_count.json', 'r') as file:
        key_count.update(json.load(file))

#Identificar teclado numérico
num_pad_keys = {
    "<96>": 'num_0',
    "<97>": 'num_1',
    "<98>": 'num_2',
    "<99>": 'num_3',
    "<100>": 'num_4',
    "<101>": 'num_5',
    "<102>": 'num_6',
    "<103>": 'num_7',
    "<104>": 'num_8',
    "<105>": 'num_9',
    "<110>": 'num_decimal',
    "<107>": 'num_add',
    "<109>": 'num_subtract',
    "<106>": 'num_multiply',
    "<111>": 'num_divide',
}


# Função chamada quando uma tecla é pressionada
def on_press(key):
    try:
        # Convertendo a tecla para string
        key_str = key.char
        if key_str is not None:
            pass
        else:
            key_str = num_pad_keys[f'{key}']
    except AttributeError:
        if hasattr(key, 'vk') and key.vk in num_pad_keys:
            key_str = num_pad_keys[key.vk]
        else:
            # Tratando teclas especiais (e.g., Shift, Ctrl)
            key_str = str(key)

    # Incrementando a contagem da tecla
    key_count[key_str] += 1

    # Salvando o resultado em um arquivo JSON a cada tecla pressionada (opcional)
    with open('key_count.json', 'w') as file:
        json.dump(key_count, file, ensure_ascii=False, indent=4)

    # Exibindo a tecla e sua contagem (opcional)
    print(f"{key_str}: {key_count[key_str]}")


# Função chamada quando uma tecla é liberada
def on_release(key):
    if key == keyboard.Key.f7:
        # Parar o listener
        return False


# Configurando o listener para eventos do teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
'''

count_cedilha = 0
count_numerico = 0
log_file = 'log.txt'

def on_press(key):
    global count_cedilha
    global count_numerico
    try:
        with open(log_file, 'a') as f:
            f.write(f'{key.char} {keyboard.Key} {key} - {datetime.datetime.now()}\n')

        if key.char == 'ç':
            count_cedilha += 1
            print(f'Tecla ç pressionada {count_cedilha} vezes')
        if key.char in [';', '*', '-', '+', '.', 'None']:
            count_numerico += 1
            print(f'Teclado numérico utilizado {count_numerico} vezes')


    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(f'{key} - {datetime.datetime.now()}\n')

def on_release(key):
    if key == keyboard.Key.f7:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except:
        if key == keyboard.Key.f7:
            print(f'Tecla F7 pressionada. Saindo da aplicação...')
            exit()
        print(f'Tecla inválida pressionada...')'''