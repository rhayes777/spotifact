import json

import requests

import config


class API(object):
    def __init__(self, access_token):
        self.access_token = access_token
        self.authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    def make_request(self, endpoint):
        response = requests.get(endpoint, headers=self.authorization_header)
        return json.loads(response.text)


with open(config.CREDENTIALS_FILE) as f:
    api = API(json.loads(f.read())["access_token"])


def pprint(response_dict):
    print(json.dumps(response_dict, indent=4))


class User(object):
    def __init__(self, href):
        self.href = href

    @classmethod
    def from_dict(cls, user_dict):
        return User(user_dict["href"])

    @property
    def play_lists(self):
        response = api.make_request("{}/playlists".format(profile_data["href"]))
        return list(map(PlayList.from_dict, response["items"]))

    def playlist_with_name(self, playlist_name):
        return [playlist for playlist in self.play_lists if playlist.name == playlist_name][0]


class PlayList(object):
    def __init__(self, name, tracks_url):
        self.name = name
        self.tracks_url = tracks_url

    @classmethod
    def from_dict(cls, playlist_dict):
        return PlayList(playlist_dict["name"], playlist_dict["tracks"]["href"])

    def __repr__(self):
        return self.name

    @property
    def tracks(self):
        return api.make_request(watford_gap.tracks_url)


user_profile_api_endpoint = "{}/me".format(config.SPOTIFY_API_URL)
profile_data = api.make_request(user_profile_api_endpoint)
user = User(profile_data)
watford_gap = user.playlist_with_name("Watford Gap (Service station archives)")

pprint(watford_gap.tracks)
