import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
import time

# Load environment variables
load_dotenv()

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authentication successful! You can close this window.")
        # Store the code from the URL
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            # Signal the server to shut down
            self.server.should_shutdown = True

def get_auth_code():
    # Start a local server to handle the callback
    server = HTTPServer(('127.0.0.1', 8000), CallbackHandler)
    server.auth_code = None
    server.should_shutdown = False
    
    def serve_forever():
        while not server.should_shutdown:
            server.handle_request()
    
    server_thread = threading.Thread(target=serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Get the authorization URL
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri="http://127.0.0.1:8000",
        scope="playlist-modify-public playlist-modify-private"
    )
    auth_url = auth_manager.get_authorize_url()
    
    # Open the browser for authentication
    print("Opening browser for authentication...")
    webbrowser.open(auth_url)
    
    # Wait for the server to get the code
    while not server.should_shutdown:
        time.sleep(0.1)
    
    return server.auth_code

# Initialize Spotify client
auth_code = get_auth_code()
auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri="http://127.0.0.1:8000",
    scope="playlist-modify-public playlist-modify-private"
)
token_info = auth_manager.get_access_token(auth_code)
sp = spotipy.Spotify(auth=token_info['access_token'])

def get_artist_top_tracks(artist_name):
    """Get top tracks for an artist"""
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if not results['artists']['items']:
        print(f"No artist found for: {artist_name}")
        return []
    
    artist_id = results['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)
    return [track['uri'] for track in top_tracks['tracks'][:3]]  # Get top 3 tracks

def create_playlist():
    """Create a playlist with tracks from all artists"""
    # Read artists from file and clean up whitespace
    with open('artists.txt', 'r') as f:
        artists = [line.strip() for line in f if line.strip()]  # This already removes empty lines
    
    # Get tracks for each artist
    all_tracks = []
    for artist in artists:
        print(f"Getting tracks for {artist}...")
        tracks = get_artist_top_tracks(artist)
        all_tracks.extend(tracks)
    
    # Create playlist
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(
        user_id,
        "My Favorite Artists Collection",
        public=True,
        description="A collection of tracks from my favorite artists"
    )
    
    # Add tracks to playlist
    for i in range(0, len(all_tracks), 100):  # Spotify API limit is 100 tracks per request
        sp.playlist_add_items(playlist['id'], all_tracks[i:i+100])
    
    print(f"Playlist created successfully! You can find it at: {playlist['external_urls']['spotify']}")

if __name__ == "__main__":
    create_playlist() 