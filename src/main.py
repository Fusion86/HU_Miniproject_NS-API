import config
from nsapi import NSApi


def main():
    api = NSApi(config.NSAPI_USERNAME, config.NSAPI_PASSWORD)

    # Load stations
    stations = api.get_stations()

    print("Loaded {} stations".format(len(stations)))

    # Test
    # print(api.actuele_vertrektijden("Utrecht"))
    # print(api.reisplanner("Utrecht", "Amersfoort"))


if __name__ == "__main__":
    main()
