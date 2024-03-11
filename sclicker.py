import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyautogui
import time
from threading import Thread
import pygame
import os

class AutoclickerApp:
    def __init__(self, master):
        self.master = master
        master.title("S7_CLICKER")
        master.configure(bg='black')
        master.iconbitmap("s7.ico")

        # Chemin vers le fichier MP3 local
        self.music_path = "GHOSTEMANE - FLESH.mp3"

        tk.Label(master, text="", bg='black').pack()
        tk.Label(master, text="", bg='black').pack()

        self.interval_label = tk.Label(master, text="Clics par seconde :", bg='black', fg='white', font=("Arial", 10, "bold"))
        self.interval_label.pack()

        self.interval_scale = tk.Scale(master, from_=1, to=380, orient=tk.HORIZONTAL, bg='black', fg='white', length=200)
        self.interval_scale.pack()

        tk.Label(master, text="", bg='black').pack()

        self.duration_label = tk.Label(master, text="Durée de l'autoclicker (en secondes) :", bg='black', fg='white', font=("Arial", 10, "bold"))
        self.duration_label.pack()

        self.duration_scale = tk.Scale(master, from_=10, to=3600, orient=tk.HORIZONTAL, bg='black', fg='white', length=200)
        self.duration_scale.pack()

        tk.Label(master, text="", bg='black').pack()

        self.volume_frame = tk.Frame(master, bg='black')
        self.volume_frame.pack()

        self.volume_label = tk.Label(self.volume_frame, text="Volume :", bg='black', fg='white', font=("Arial", 8))
        self.volume_label.pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg='black', fg='white', length=100, command=self.update_volume)
        self.volume_scale.set(50)  # Définir le volume initial à 50
        self.volume_scale.pack(side=tk.LEFT)

        tk.Label(master, text="", bg='black').pack()

        self.start_button = tk.Button(master, text="Démarrer", command=self.start_autoclicker, bg='purple', fg='white')
        self.start_button.pack()

        tk.Label(master, text="", bg='black').pack()

        self.stop_button = tk.Button(master, text="Arrêter", command=self.stop_autoclicker, state=tk.DISABLED, bg='purple', fg='white')
        self.stop_button.pack()

        tk.Label(master, text="", bg='black').pack()

        self.music_button = tk.Button(master, text="Arrêter la musique", command=self.stop_music, state=tk.DISABLED, bg='purple', fg='white')
        self.music_button.pack()

        tk.Label(master, text="", bg='black').pack()

        self.status_label = tk.Label(master, text="", bg='black', fg='white')
        self.status_label.pack()

        tk.Label(master, text="", bg='black').pack()

        self.made_by_label = tk.Label(master, text="made by LZN LA FRAPPE", font=("Arial", 10), bg='purple', fg='white')
        self.made_by_label.pack(side="bottom", fill="x")

        self.autoclicker_thread = None
        self.is_autoclicker_running = False

        # Initialiser Pygame
        pygame.mixer.init()
        self.update_volume()

    def update_volume(self, event=None):
        # Convertir le volume de l'échelle (0-100) en plage (0.0-1.0)
        volume = self.volume_scale.get() / 100
        pygame.mixer.music.set_volume(volume)  # Définir le volume

    def start_autoclicker(self):
        clicks_per_second = float(self.interval_scale.get())
        interval = 1 / clicks_per_second
        duration = int(self.duration_scale.get())
        self.autoclicker_thread = Thread(target=self.run_autoclicker, args=(interval, duration))
        self.autoclicker_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.music_button.config(state=tk.NORMAL)
        self.status_label.config(text="Autoclicker démarré.")
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play()

    def stop_autoclicker(self):
        if self.autoclicker_thread:
            self.is_autoclicker_running = False
            self.autoclicker_thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.music_button.config(state=tk.DISABLED)
            self.status_label.config(text="Autoclicker arrêté.")
            pygame.mixer.music.stop()
        else:
            self.status_label.config(text="Autoclicker non démarré.")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_button.config(state=tk.DISABLED)

    def run_autoclicker(self, interval, duration):
        self.is_autoclicker_running = True
        end_time = time.time() + duration
        while time.time() < end_time and self.is_autoclicker_running:
            pyautogui.click()
            time.sleep(interval)
        self.check_time_elapsed(end_time)

    def check_time_elapsed(self, end_time):
        if time.time() >= end_time:
            self.stop_autoclicker()
        else:
            self.master.after(100, self.check_time_elapsed, end_time)

            

def main():
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()