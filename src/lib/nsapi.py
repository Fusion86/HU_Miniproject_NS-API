import requests
import xmltodict


class NSApi:
    """NSApi"""

    api_url = "http://webservices.ns.nl"
    api_url_avt = api_url + "/ns-api-avt"

    def __init__(self, username, password):
        self.auth_details = (username, password)

    def actuele_vertrektijden(self, station):
        url = self.api_url_avt + "?station=" + station
        response = requests.get(url, auth=self.auth_details)
        return xmltodict.parse(response.text)
