from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace the empty strings below with your own Spotify API credentials
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""
SPOTIFY_ID = ""
song_uris = []

# Prompt the user for the date they want to visit
input_response = input("Which day of the past do you wanna visit? (DD-MM-YYYY)\n")
split_input = input_response.split("-")
year = split_input[2]
month = split_input[1]
day = split_input[0]
website = f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}"

# Retrieve the webpage content
response = requests.get(website)
soup = BeautifulSoup(response.text, "html.parser")

# Extract the song names from the webpage
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Set up Spotify API client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public"))

# Get the user ID
user_id = sp.current_user()["id"]

# Search for each song and retrieve its URI
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

# Create a new playlist on the user's Spotify account
playlist = sp.user_playlist_create(
    user_id,
    name=f"TOP 100 ({day}/{month}/{year})", 
    description=f"The Billboard Top 100 songs of {day}/{month}/{year}")

# Add the songs to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# Print the URL of the created playlist
print(f'Your playlist is here: {playlist["external_urls"]["spotify"]}')
