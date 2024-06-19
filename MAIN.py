import customtkinter as ctk
import subprocess
import threading

def offline_play(root):
    print("Starting offline play...")
    subprocess.Popen(["python", "PONG_OFFLINE.py"])
    root.destroy()

def online_play(root):
    print("Starting online play...")
    subprocess.Popen(["python", "PONG_ONLINE.py"])
    root.destroy()

def start_game(root, choice):
    if choice == 1:
        offline_play(root)
    elif choice == 2:
        online_play(root)
    else:
        ctk.CTkMessagebox(title="Error", message="Invalid choice")

def main():
    root = ctk.CTk()
    root.title("GAME-MODE-SELECTION")
    root.geometry("615x300")
    root.resizable(False, False)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    welcome_label = ctk.CTkLabel(
        root, 
        text="Welcome to the 'PONG GAME-MODE-SELECTION'!\nSelect your game mode:",
        font=("Helvetica", 24, "bold"),
        text_color="White"
    )
    welcome_label.pack(pady=20)

    button_offline = ctk.CTkButton(
        root, 
        text="Offline Play", 
        font=("Helvetica", 16),
        width=250,
        height=75,
        command=lambda: start_game(root, 1)
    )
    button_offline.pack(pady=10)

    button_online = ctk.CTkButton(
        root, 
        text="Online Play", 
        font=("Helvetica", 16),
        width=250,
        height=75,
        command=lambda: start_game(root, 2)
    )
    button_online.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
