import tkinter as tk
from game import Game
from threading import Thread

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

        multiplayer_host_button = tk.Button(self.root, text="Host Online", command=self.host_online)
        multiplayer_host_button.pack(pady=10)

        multiplayer_join_button = tk.Button(self.root, text="Join Online", command=self.join_online)
        multiplayer_join_button.pack(pady=10)

        settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        settings_button.pack(pady=10)

        # Run the Tkinter event loop
        self.root.mainloop()

    def play_offline(self):
        self.root.destroy()
        self.game_instance.run_offline()
        print("Starting single player game...")

    def host_online(self):
        self.root.destroy()
        # trzeba func reference LOL
        # game_thread = Thread(target=self.game_instance.run_online_host)
        tcp_thread = Thread(target=self.game_instance.run_server_thread)

        # game_thread.start()
        tcp_thread.start()
        self.game_instance.run_online_host()
        # game_thread.join()
        tcp_thread.join()
        # start thread for a TCP server
        # start thread for running the game
        print("Starting multiplayer game...")

    def join_online(self):
        self.root.destroy()
        # game_thread = Thread(target=self.game_instance.run_online_client)
        tcp_thread = Thread(target=self.game_instance.run_client_thread)

        # game_thread.start()
        tcp_thread.start()
        self.game_instance.run_online_client()
        # game_thread.join()
        tcp_thread.join()
        # start thread for a TCP client
        # start thread for running the game
        print("Joining...")

    def open_settings(self):

        print("Opening settings...")
