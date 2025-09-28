import customtkinter as ctk
import keyboard
import pyautogui
import threading
import time

class Client:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_widget_scaling(1.0)

        self.root = ctk.CTk()
        self.root.title("Client")
        self.root.geometry("300x250")
        self.root.configure(fg_color="#1A1A1A")

        self.clicking = False
        self.delay = 0.1
        self.hotkey = 'f6'

        self.title_label = ctk.CTkLabel(
            self.root, 
            text="Client", 
            font=("Arial", 16), 
            text_color="#E0E0E0"
        )
        self.title_label.pack(pady=10)

        self.delay_label = ctk.CTkLabel(
            self.root, 
            text="Click Delay (seconds, 0 for max speed):", 
            text_color="#E0E0E0"
        )
        self.delay_label.pack()

        self.delay_entry = ctk.CTkEntry(
            self.root, 
            fg_color="#2A2A2A", 
            text_color="#E0E0E0", 
            border_color="#4A4A4A"
        )
        self.delay_entry.insert(0, "0.1")
        self.delay_entry.pack(pady=5)

        self.hotkey_label = ctk.CTkLabel(
            self.root, 
            text="Hotkey:", 
            text_color="#E0E0E0"
        )
        self.hotkey_label.pack()

        self.hotkey_entry = ctk.CTkEntry(
            self.root, 
            fg_color="#2A2A2A", 
            text_color="#E0E0E0", 
            border_color="#4A4A4A"
        )
        self.hotkey_entry.insert(0, "f6")
        self.hotkey_entry.pack(pady=5)

        self.apply_button = ctk.CTkButton(
            self.root, 
            text="Apply Settings", 
            command=self.apply_settings, 
            fg_color="#3A3A3A", 
            hover_color="#4A4A4A",
            text_color="#E0E0E0"
        )
        self.apply_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.root, 
            text="Status: Off", 
            text_color="#E0E0E0"
        )
        self.status_label.pack()

        keyboard.add_hotkey(self.hotkey, self.toggle_clicking)

        self.root.mainloop()

    def apply_settings(self):
        try:
            self.delay = float(self.delay_entry.get())
            if self.delay < 0:
                self.delay = 0.1
        except ValueError:
            self.delay = 0.1

        pyautogui.PAUSE = 0 if self.delay == 0 else self.delay

        new_hotkey = self.hotkey_entry.get().lower()
        if new_hotkey != self.hotkey:
            keyboard.remove_hotkey(self.hotkey)
            self.hotkey = new_hotkey
            keyboard.add_hotkey(self.hotkey, self.toggle_clicking)

    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.status_label.configure(text="Status: On")
            self.thread = threading.Thread(target=self.click_loop)
            self.thread.daemon = True
            self.thread.start()
        else:
            self.status_label.configure(text="Status: Off")

    def click_loop(self):
        while self.clicking:
            pyautogui.click()
            if self.delay > 0:
                time.sleep(self.delay)

if __name__ == "__main__":
    Client()

