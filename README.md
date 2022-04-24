# IN PROGRESS!!! Library and Playlist Cleaner Tool for Spotify

## Purpose of Tool
This tool seeks to tidy up your Spotify collection by replacing multiple song versions (identical track from artist but different album name) with just one of the song versions throughout all playlists and your saved songs. For people like me who get annoyed by those kinds of things :)

### DISCLAIMER
This tool does NOT guarantee perfect results! I've tried to brainstorm potential edge cases, but don't assume I thought of everything. **Please use the cleaner tool at your own risk.**

### Fully implemented
* Exporter Tool: Download all playlists/saved tracks/saved albums (information) in your Spotify library
    * I anticipate making changes to the relevant information that gets saved as needed

### In the works
* Cleaner Tool: Eliminate duplicate copies of songs (identical track that may be from various locations, such as the original album and the deluxe version of the album, and other similar situations) by replacing instances with a single prioritized version
* More to come....

## How To Use
### Setup
1. Create virtual environment and install required packages (`requirements.txt` file provided).
2. Create Spotify developer credentials (Visit https://developer.spotify.com/dashboard/ and Create an App) and either directly modify the values in config_to_file.py or save them in your shell environment as `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI`.
    * Client ID and Client Secret are given by the API on the App-Specific Dashboard
    * Redirect URI is chosen by you
        * I use `http://localhost:8787/` for simplicity. After you authenticate (in Step 3) and allow the app to access your Spotify library, it will redirect to a page saying "Server Not Found" (or something along those lines, depending on your OS) since there is no locally running web server for the callback. This is not a problem; just copy the current URL in your address bar and paste that into the terminal or Jupyter notebook text box when prompted.
3. Run `python config_to_file.py` and log in with your Spotify account to authenticate.

### Export your playlists and other saved content
1. Run `python export.py`
2. (Don't do this yet -- it won't do anything useful) Run `python cleanup.py` or use the functions in a Jupyter notebook to work interactively (safer).

## License
Code is provided under GNU GPLv3, see LICENSE for more info.