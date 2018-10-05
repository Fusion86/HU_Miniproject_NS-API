from nsapi import NSApi


def main():
    username = ""
    password = ""

    api = NSApi(username, password)

    # Load stations
    stations = api.get_stations()

    print("Loaded {} stations".format(len(stations)))

    # Test
    # print(api.actuele_vertrektijden("Utrecht"))
    # print(api.reisplanner("Utrecht", "Amersfoort"))


if __name__ == "__main__":
    main()
