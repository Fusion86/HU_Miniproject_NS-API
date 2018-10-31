import config
from nsapi import NSApi
from tkinter import *
from tkinter import messagebox, ttk
import dateutil.parser
from PIL import ImageTk, Image


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
        frame_start = Frame(root, width=1024, height=768, background="#FED900")
        Label(
            frame_start,
            text="Welkom bij NS",
            foreground="#002A90",
            background="#FED900",
            font=("Tahoma", 48),
        ).place(x=307, y=143)

        Button(
            frame_start,
            text="Ik heb geen\nOV-chipkaart",
            foreground="white",
            background="#002A90",
            font=("Tahoma", 14),
        ).place(x=222, y=545)

        Button(
            frame_start,
            text="Ik wil naar\nhet buitenland",
            foreground="white",
            background="#002A90",
            font=("Tahoma", 14),
        ).place(x=442, y=545)

        Button(
            frame_start,
            text="Toon de\nvertrektijden",
            foreground="white",
            background="#002A90",
            font=("Tahoma", 14),
            command=self.show_main,
        ).place(x=662, y=545)

        # Load image and keep reference so that the GC doesn't delete it
        img = ImageTk.PhotoImage(Image.open("src/assets/chipkaart.png"))
        frame_start._img_chipkaart = img

        # Draw image on canvas
        canvas = Canvas(
            frame_start, bg="#FED900", width=424, height=225, bd=0, highlightthickness=0
        )
        canvas.place(x=310, y=240)
        canvas.create_image(424 / 2, 225 / 2, image=img)

        frame_start.grid(row=0, column=0, sticky="nsew")

        # Main frame setup
        frame_main = Frame(root, width=1024, height=768)

        # Background
        canvas = Canvas(frame_main, width=1024, height=768, background="#002A90")
        canvas.pack()
        canvas.create_rectangle(0, 184, 1026, 688, fill="#FED900", outline="")

        # Header
        Label(
            frame_main,
            text="Vertrekstation",
            background="#002A90",
            foreground="white",
            font=("Tahoma", 28),
        ).place(x=20, y=20)
        Label(
            frame_main,
            text="Eindstation",
            background="#002A90",
            foreground="white",
            font=("Tahoma", 28),
        ).place(x=20, y=104)

        self.txtBeginStation = Entry(frame_main)
        self.txtBeginStation.place(x=308, y=35)
        self.txtBeginStation.insert(0, "Utrecht Centraal")

        self.txtEindStation = Entry(frame_main)
        self.txtEindStation.place(x=308, y=120)

        Button(
            frame_main,
            text="Zoek\ntreinen",
            background="#5F5FC4",
            foreground="white",
            font=("Tahoma", 28),
            command=self.update,
        ).place(x=827, y=20)

        # Main content - yellow
        Label(
            frame_main, text="Vertrek", background="#FED900", font=("Tahoma", 28)
        ).place(x=20, y=204)
        # Label(
        #     frame_main, text="Aankomst", background="#FED900", font=("Tahoma", 28)
        # ).place(x=173, y=204)
        Label(
            frame_main, text="Bestemming", background="#FED900", font=("Tahoma", 28)
        ).place(x=300, y=204)
        Label(
            frame_main, text="Type trein", background="#FED900", font=("Tahoma", 28)
        ).place(x=700, y=204)

        # Entries
        row_height = 50
        for i in range(self.stations_to_show):
            # Vetrek
            lbl = Label(
                frame_main, text="12:00", background="#FED900", font=("Tahoma", 28)
            )
            lbl.place(x=20, y=271 + row_height * i)
            setattr(self, "lblVertrekTijd{}".format(i), lbl)

            # Aankomst
            # lbl = Label(
            #     frame_main, text="13:00", background="#FED900", font=("Tahoma", 28)
            # )
            # lbl.place(x=173, y=271 + row_height * i)
            # setattr(self, "lblAankomstTijd{}".format(i), lbl)

            # Bestemming
            lbl = Label(
                frame_main,
                text="Amsterdam Centraal",
                background="#FED900",
                font=("Tahoma", 28),
            )
            lbl.place(x=300, y=271 + row_height * i)
            setattr(self, "lblBestemming{}".format(i), lbl)

            # Type trein
            lbl = Label(
                frame_main, text="InterCity", background="#FED900", font=("Tahoma", 28)
            )
            lbl.place(x=700, y=271 + row_height * i)
            setattr(self, "lblType{}".format(i), lbl)

        # Footer
        Button(
            frame_main,
            text="Terug",
            background="#002A90",
            foreground="white",
            font=("Tahoma", 20),
            command=self.show_start,
        ).place(x=20, y=702)

        frame_main.grid(row=0, column=0, sticky="nsew")

        self.frame_start = frame_start
        self.frame_main = frame_main

        # Show start frame
        self.show_start()

        # Show times for default station Utrecht Centraal
        self.update()

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
            route = self.api.reisplanner(beginstation, eindstation)
            routedict = route["ReisMogelijkheden"]["ReisMogelijkheid"]

            for i in range(self.stations_to_show):
                self.set_text(
                    "lblVertrekTijd{}".format(i),
                    get_time_string(routedict[i]["ActueleVertrekTijd"]),
                )

                self.set_text("lblBestemming{}".format(i), eindstation)

                # Shows VervoerType for first ReisDeel, there could be more but we only show the first
                self.set_text(
                    "lblType{}".format(i), routedict[i]["ReisDeel"]["VervoerType"]
                )
        else:
            avt = self.api.actuele_vertrektijden(beginstation)
            avtdict = avt["ActueleVertrekTijden"]["VertrekkendeTrein"]

            for i in range(self.stations_to_show):
                self.set_text(
                    "lblVertrekTijd{}".format(i),
                    get_time_string(avtdict[i]["VertrekTijd"]),
                )

                self.set_text("lblBestemming{}".format(i), avtdict[i]["EindBestemming"])

                self.set_text("lblType{}".format(i), avtdict[i]["TreinSoort"])

    def set_text(self, lbl, text):
        attr = getattr(self, lbl)

        if attr:
            attr.config(text=text)

    def show_start(self):
        self.frame_start.tkraise()

    def show_main(self):
        self.frame_main.tkraise()


def main():
    # Init app
    root = Tk()
    app = App(root)

    # Start Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
