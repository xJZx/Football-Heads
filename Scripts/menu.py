import tkinter as tk
from game import Game


class Menu:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Football-Heads")
        self.root.geometry("")
        self.root.resizable()
        self.game_instance = Game()

        # Create buttons
        singleplayer_button = tk.Button(self.root, text="Play Offline", command=self.play_offline)
        singleplayer_button.pack(pady=10)

        multiplayer_button = tk.Button(self.root, text="Play Online", command=self.play_online)
        multiplayer_button.pack(pady=10)

        settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        settings_button.pack(pady=10)

        # Run the Tkinter event loop
        self.root.mainloop()

    def play_offline(self):
        self.root.destroy()
        self.game_instance.run_offline()
        print("Starting single player game...")

    def play_online(self):

        print("Starting multiplayer game...")

    def open_settings(self):
        print("Opening settings...")
