from nsapi import NSApi


def main():
    username = ""
    password = ""

    api = NSApi(username, password)

    print(api.actuele_vertrektijden("Utrecht"))


if __name__ == "__main__":
    main()
