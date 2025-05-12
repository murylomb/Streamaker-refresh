import pyautogui
import time
import threading
from pynput import keyboard
import sys
import os
from PIL import Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Caminhos das imagens originais
refresh_img_path = resource_path('refresh.png')
foguete_img_path = resource_path('foguete.png')

# Carregar e redimensionar com escala fixa de 1.25
escala = 1.25
def redimensionar_e_salvar(imagem_path, nome_temp):
    imagem = Image.open(imagem_path)
    nova_largura = int(imagem.width * escala)
    nova_altura = int(imagem.height * escala)
    imagem_redimensionada = imagem.resize((nova_largura, nova_altura))
    imagem_temp_path = f"{nome_temp}_temp.png"
    imagem_redimensionada.save(imagem_temp_path)
    return imagem_temp_path

# Criar versões redimensionadas uma vez
refresh_img_scaled = redimensionar_e_salvar(refresh_img_path, "refresh")
foguete_img_scaled = redimensionar_e_salvar(foguete_img_path, "foguete")

executando = False
lock = threading.Lock()

def toggle_script():
    global executando
    with lock:
        executando = not executando
        print("Programa Iniciado" if executando else "Programa Encerrado")

def detectar_tecla():
    def on_press(key):
        if key == keyboard.Key.end:
            toggle_script()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def localizar_botao(imagem_path):
    try:
        return pyautogui.locateCenterOnScreen(imagem_path, confidence=0.8, grayscale=True)
    except Exception as e:
        print(f"Erro ao localizar {imagem_path}: {e}")
        return None

def loop_principal():
    print("Aperte End para Iniciar/Parar o programa")
    time.sleep(2)

    global executando
    while True:
        with lock:
            if executando:
                refresh_btn = localizar_botao(refresh_img_scaled)
                foguete_btn = localizar_botao(foguete_img_scaled)

                if refresh_btn:
                    pyautogui.click(refresh_btn)
                    print("Cliquei no botão Refresh!")
                    time.sleep(0.7)
                elif foguete_btn:
                    pyautogui.click(foguete_btn)
                    print("Cliquei no Especial!")
                    time.sleep(0.7)
                else:
                    print("Nenhum botão encontrado...")
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

# Inicia o listener de teclado em thread separada
threading.Thread(target=detectar_tecla, daemon=True).start()
loop_principal()
