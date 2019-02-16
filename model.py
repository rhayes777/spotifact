import json
import logging

import requests

import config


class API(object):
    def __init__(self, access_token):
        self.access_token = access_token
        self.authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    def make_request(self, endpoint):
        response = requests.get(endpoint, headers=self.authorization_header)
        return json.loads(response.text)

    def items_from_endpoint(self, endpoint):
        response = self.make_request(endpoint)

        while True:
            for item in response["items"]:
                yield item
            next_endpoint = response["next"]
            if next_endpoint is None:
                break
            response = self.make_request(next_endpoint)


with open(config.CREDENTIALS_FILE) as f:
    api = API(json.loads(f.read())["access_token"])


def pprint(response_dict):
    print(json.dumps(response_dict, indent=4))


class User(object):
    def __init__(self, href):
        self.href = href
        self.__play_lists = None

    @classmethod
    def from_dict(cls, user_dict):
        return User(user_dict["href"])

    @property
    def play_lists(self):
        if self.__play_lists is None:
            response = api.make_request("{}/playlists".format(profile_data["href"]))
            self.__play_lists = list(map(PlayList.from_dict, response["items"]))
        return self.__play_lists

    def playlist_with_name(self, playlist_name):
        return [playlist for playlist in self.play_lists if playlist.name == playlist_name][0]


class PlayList(object):
    def __init__(self, name, tracks_url):
        self.name = name
        self.tracks_url = tracks_url
        self.__tracks = None

    @classmethod
    def from_dict(cls, playlist_dict):
        return PlayList(playlist_dict["name"], playlist_dict["tracks"]["href"])

    def __repr__(self):
        return self.name

    @property
    def tracks(self):
        if self.__tracks is None:
            self.__tracks = list(map(PlayListTrack.from_dict, api.items_from_endpoint(watford_gap.tracks_url)))
        return self.__tracks

    def __getitem__(self, item):
        return self.tracks[item]


class PlayListTrack(object):
    def __init__(self, track, added_at, added_by):
        self.track = track
        self.added_at = added_at
        self.added_by = added_by

    @classmethod
    def from_dict(cls, playlist_track_dict):
        return PlayListTrack(Track.from_dict(playlist_track_dict["track"]),
                             playlist_track_dict["added_at"],
                             playlist_track_dict["added_by"])


class Track(object):
    def __init__(self, name, artist_hrefs):
        self.name = name
        self.artist_hrefs = artist_hrefs

    @classmethod
    def from_dict(cls, track_dict):
        return Track(track_dict["name"],
                     [artist["href"] for artist in track_dict["artists"]])

    @property
    def artists(self):
        return list(filter(None, map(Artist.from_href, self.artist_hrefs)))

    @property
    def genres(self):
        return {genre for artist in self.artists for genre in artist.genres}


class Artist(object):
    def __init__(self, name, genres):
        self.name = name
        self.genres = genres

    href_cache = {}

    @classmethod
    def from_href(cls, href):
        try:
            if href not in Artist.href_cache:
                Artist.href_cache[href] = Artist.from_dict(api.make_request(href))
            return Artist.href_cache[href]
        except Exception as e:
            logging.exception(e)

    @classmethod
    def from_dict(cls, artist_dict):
        return Artist(artist_dict["name"], artist_dict["genres"])


user_profile_api_endpoint = "{}/me".format(config.SPOTIFY_API_URL)
profile_data = api.make_request(user_profile_api_endpoint)
user = User(profile_data)

watford_gap = user.playlist_with_name("Watford Gap (Service station archives)")