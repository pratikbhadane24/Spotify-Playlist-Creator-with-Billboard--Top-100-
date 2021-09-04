from os import name
from typing import final
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input(
    "What year's Top songs do you want? Enter a date in YYYY-MM-DD format: ")
url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url=url)
billboard_web_pg = response.text

soup = BeautifulSoup(billboard_web_pg, "html.parser")
songs = soup.find_all(
    name="span", class_="chart-element__information__song text--truncate color--primary")
songs_list = [song.text for song in songs]


# Spotify Devs Authentication
CLIENT_ID = ""
CLIENT_SECRET = ""
URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(
    user=user_id, name=f"{date} Billboard 100", public=False)

# Adding songs into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# Final Playlist
final_playlist = playlist["uri"]
print(f"Here is your playlist: {final_playlist}")
