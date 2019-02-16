import configparser
import pathlib

parser = configparser.ConfigParser()
parser.read(pathlib.Path(__file__).parent / "config.ini")

CLIENT_ID = parser.get("client", "CLIENT_ID")
CLIENT_SECRET = parser.get("client", "CLIENT_SECRET")

CREDENTIALS_FILE = parser.get("path", "CREDENTIALS_FILE")

HOST = parser.get("redirect", "HOST")
PORT = parser.get("redirect", "PORT")
ENDPOINT = parser.get("redirect", "ENDPOINT")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
