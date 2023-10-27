# This script will connect to the Spotify API and pull album, artist, track, and playlist data to a dataframe that will be called in the transform stage.

# 1. get spotify client_id and client secret
# 2. install spotify in CLI
# 3. import spotify 
import spotipy
import pandas as pd

auth_manager = spotipy.oauth2.SpotifyOAuth(
    client_id='3745e7cead8f46ffb0edefcd3b9cd250',
    client_secret='5aea2ed641a74fe682d12024542be784',
    redirect_uri='http://localhost:7777/callback'
)

try:
    spotify_client = spotipy.Spotify(auth_manager=auth_manager)
    user_info = spotify_client.current_user()
    print("Connection to Spotify successful!")
except Exception as e:
    print("Connection to Spotify failed:", str(e))


# Create empty lists to store the data
album_data_list = []
artist_data_list = []
track_data_list = []
playlist_data_list = []

# Define the get_album_data function
def get_album_data(spotify_client, album_id):
    # Your code to retrieve album data goes here
    all_albums = spotify_client.current_user_saved_albums()
    for album in all_albums['items']:
        album_data = get_album_data(spotify_client, album['album']['id'])
        album_data_list.append(album_data)
    return album_data
# Retrieve all albums

def get_artist_data(spotify_client, album_id):
# Retrieve all artists
    all_artists = spotify_client.current_user_followed_artists()
    for artist in all_artists['artists']['items']:
        artist_data = get_artist_data(spotify_client, artist['id'])
        artist_data_list.append(artist_data)
    return artist_data

def get_track_data(spotify_client, album_id):
# Retrieve all tracks
    all_tracks = spotify_client.current_user_saved_tracks()
    for track in all_tracks['items']:
        track_data = get_track_data(spotify_client, track['track']['id'])
        track_data_list.append(track_data)
    return get_track_data

def get_playlist_data(spotify_client, album_id):
# Retrieve all playlists
    all_playlists = spotify_client.current_user_playlists()
    for playlist in all_playlists['items']:
        playlist_data = get_playlist_data(spotify_client, playlist['id'])
        playlist_data_list.append(playlist_data)
    return get_playlist_data

# Create DataFrames from the lists
album_df = pd.DataFrame(album_data_list)
artist_df = pd.DataFrame(artist_data_list)
track_df = pd.DataFrame(track_data_list)
playlist_df = pd.DataFrame(playlist_data_list)

# Display the DataFrames
print("Album Data:")
print(album_df)

print("Artist Data:")
print(artist_df)

print("Track Data:")
print(track_df)

print("Playlist Data:")
print(playlist_df)