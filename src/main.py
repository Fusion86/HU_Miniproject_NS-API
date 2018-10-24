import config
from nsapi import NSApi
from tkinter import *
from tkinter import messagebox, ttk
import dateutil.parser


def get_time_string(str):
    dt = dateutil.parser.parse(str)
    return dt.strftime("%H:%M")


class App:
    # Config
    stations_to_show = 5

    def __init__(self, root):
        # Setup NSApi
        self.api = NSApi(config.NSAPI_USERNAME, config.NSAPI_PASSWORD)

        # Load stations
        self.stations = self.api.get_stations()
        print("Loaded {} stations".format(len(self.stations)))

        # Setup Tkinter
        self.root = root
        root.title("NS Miniproject")
        root.resizable(False, False)  # Disable window resizing

        # Start frame setup
        frame_start = Frame(root, width=1024, height=768)
        Label(frame_start, text="Welkom bij NS").place(x=307, y=143)

        frame_start.pack()

        # Main frame setup
        frame_main = Frame(root)

        frame_main.pack()

        self.frame_start = frame_start
        self.frame_main = frame_main

        # Show start frame
        frame_main.tkraise()

        # Label(root, text="Begin station").grid(row=0, sticky="w")
        # Label(root, text="Eind station").grid(row=1, sticky="w")

        # self.txtBeginStation = Entry(root)
        # self.txtBeginStation.insert(0, "Utrecht Centraal")
        # self.txtBeginStation.grid(row=0, column=1)

        # self.txtEindStation = Entry(root)
        # self.txtEindStation.grid(row=1, column=1)

        # self.btnUpdate = Button(root, text="Update", command=self.update)
        # self.btnUpdate.grid(row=0, column=2, rowspan=2)

        # ttk.Separator(root, orient=HORIZONTAL).grid(row=2, columnspan=5, sticky="ew")

        # # Add rows (count = self.stations_to_show)
        # start_row = 2
        # for i in range(self.stations_to_show):
        #     lbl = Label(root)
        #     lbl.grid(row=start_row + i + 1, sticky="w")  # +1 because we start at zero
        #     setattr(self, "lblVertrekTijd{}".format(i), lbl)

        # # Show times for default station Utrecht Centraal
        # self.update()

    def update(self):
        """Load input from Entries and update lblVertrekTijd_ with new info"""

        beginstation = self.txtBeginStation.get()
        eindstation = self.txtEindStation.get()

        if beginstation not in self.stations:
            messagebox.showerror("Error", "Begin station bestaat niet!")
            return

        hasEindStation = eindstation is not ""  # If not empty

        if hasEindStation and eindstation not in self.stations:
            messagebox.showerror("Error", "Eind station bestaat niet!")
            return

        if hasEindStation:
            pass
        else:
            avt = self.api.actuele_vertrektijden(beginstation)
            avtdict = avt["ActueleVertrekTijden"]["VertrekkendeTrein"]

            for i in range(self.stations_to_show):
                txt = "{} - {}".format(
                    get_time_string(avtdict[i]["VertrekTijd"]),
                    avtdict[i]["EindBestemming"],
                )
                self.set_text(i, txt)

    def set_text(self, number, text):
        attr = getattr(self, "lblVertrekTijd{}".format(number))

        if attr:
            attr.config(text=text)


def main():
    # Init app
    root = Tk()
    app = App(root)

    # Start Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
