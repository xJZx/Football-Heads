class Game:

    #Properties
    import tkinter as tk

    # Create a window object
    window = tk.Tk()

    # Set the window title
    window.title("My Application")

    # Set the window size
    window.geometry("500x500")

    # Add some content to the window
    label = tk.Label(window, text="Hello, World!")
    label.pack()

    # Start the main event loop
    window.mainloop()


    #Methods

    #def __init__(self):
