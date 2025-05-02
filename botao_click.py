import pyautogui
import time
import threading
from pynput import keyboard
import sys
import os

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

def loop_principal():
    print("Aperte F8 para Iniciar/Parar o programa")
    time.sleep(3)

    global executando
    while True:
        with lock:
            if executando:
                refresh_btn = None
                foguete_btn = None

                try:
                    refresh_btn = pyautogui.locateCenterOnScreen(refresh_img, confidence=0.9)
                except pyautogui.ImageNotFoundException:
                    pass

                try:
                    foguete_btn = pyautogui.locateCenterOnScreen(foguete_img, confidence=0.9)
                except pyautogui.ImageNotFoundException:
                    pass

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
