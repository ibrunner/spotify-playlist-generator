# Spotify Playlist Creator

A Python script that creates a Spotify playlist with top tracks from your favorite artists.

## Features

- Creates a playlist with 3 top tracks from each artist
- Handles authentication with Spotify's API
- Supports multiple artists
- Simple text file input

## Setup

1. Create a Spotify Developer account at https://developer.spotify.com/dashboard
2. Create a new application in the Spotify Developer Dashboard
3. Add `http://127.0.0.1:8000` as a Redirect URI in your app settings
4. Copy your Client ID and Client Secret
5. Create a `.env` file with your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   ```
6. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Add your favorite artists to `artists.txt`, one per line
2. Run the script:
   ```bash
   python3 create_playlist.py
   ```
3. A browser window will open for Spotify authentication
4. After authenticating, the script will create a playlist with tracks from all artists

## Requirements

- Python 3.x
- spotipy
- python-dotenv

## Notes

- The script creates a playlist named "My Favorite Artists Collection"
- Each artist contributes their top 3 tracks
- The playlist is created in your Spotify account
- Some artist names might not be found if they don't match Spotify's database exactly
  Spotify Playlist Creator
