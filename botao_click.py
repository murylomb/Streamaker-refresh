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

refresh_img = resource_path('refresh.png')
foguete_img = resource_path('foguete.png')

executando = False
lock = threading.Lock()

def toggle_script():
    global executando
    with lock:
        executando = not executando
        print("Programa Iniciado" if executando else "Programa Encerrado")

def detectar_tecla():
    def on_press(key):
        if key == keyboard.Key.f8:
            toggle_script()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def localizar_botao_multiescala(imagem_path, escalas=[1.0, 1.10]):
    imagem_original = Image.open(imagem_path)
    for escala in escalas:
        largura = int(imagem_original.width * escala)
        altura = int(imagem_original.height * escala)
        imagem_redimensionada = imagem_original.resize((largura, altura))
        imagem_temp_path = "temp_scaled_image.png"
        imagem_redimensionada.save(imagem_temp_path)

        try:
            local = pyautogui.locateCenterOnScreen(imagem_temp_path, confidence=0.8)
            if local:
                return local
        except pyautogui.ImageNotFoundException:
            continue  # Se não encontrar, tenta com a próxima escala
        except Exception as e:
            print(f"Erro ao procurar imagem em escala {escala}: {e}")
            continue
    return None

def loop_principal():
    print("Aperte F8 para Iniciar/Parar o programa")
    time.sleep(3)

    global executando
    while True:
        with lock:
            if executando:
                refresh_btn = localizar_botao_multiescala(refresh_img)
                foguete_btn = localizar_botao_multiescala(foguete_img)

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

# Rodar listener em thread separada
threading.Thread(target=detectar_tecla, daemon=True).start()
loop_principal()
