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
