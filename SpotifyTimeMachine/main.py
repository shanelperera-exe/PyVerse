from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            show_dialog=True,
            cache_path="token.txt",
            username=os.environ["SPOTIFY_DISPLAY_NAME"]
        )
    )

user_id = sp.current_user()["id"]

def main():
    date = get_date()
    songs = get_songs(date)
    year = date.split("-")[0]
    song_uris = search_spotify(songs, year)
    create_playlist(date, song_uris)

def get_date():
    while True:
        try:
            date = input("Which year do you want to travel to? (Type the date in the format, YYYY-MM-DD): ")
            valid_date = datetime.strptime(date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Error: Please enter a valid date in the correct format (YYYY-MM-DD). Try again.")
    return str(valid_date)

def get_songs(date):
    url = "https://www.billboard.com/charts/hot-100/" + date
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    response = requests.get(url=url, headers=header)
    response.raise_for_status()
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    song_name_spans = soup.select("li ul li h3")
    songs = [song.getText().strip() for song in song_name_spans]
    return songs

def search_spotify(songs, year):
    song_uris = []
    for song in songs:
        result = sp.search(q=f"track:{song}, year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            print(f"{song} found. URI: {uri}")
            song_uris.append(uri)
        except KeyError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    return song_uris

def create_playlist(date, songs):
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"{date} Billboard 100",
        public=False,
        collaborative=False,
        description=f"Top 100 Hits from {date}"
    )
    sp.playlist_add_items(playlist_id=playlist["id"], items=songs)
    print(f"\nPlaylist {date} Billboard 100 created successfully.")

if __name__ == "__main__":
    main()