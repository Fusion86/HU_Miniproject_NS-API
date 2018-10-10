import config
from nsapi import NSApi
from tkinter import *


class App:
    def __init__(self, root):
        # Setup NSApi
        self.api = NSApi(config.NSAPI_USERNAME, config.NSAPI_PASSWORD)

        # Load stations
        self.stations = self.api.get_stations()
        print("Loaded {} stations".format(len(self.stations)))

        # Setup Tkinter
        self.root = root
        root.title("NS Miniproject")
        root.resizable(False, False) # Disable window resizing


def main():
    # Init app
    root = Tk()
    app = App(root)

     # Start Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
