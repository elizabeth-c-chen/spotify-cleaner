# Spotify Library and Playlist Cleaner Tool

## Purpose of Tool
This tool seeks to tidy up your Spotify collection by replacing multiple song versions (identical track from artist but different album name) with just one of the song versions throughout all playlists and your saved songs. 
* If more than one copy of a song exists and the tracks are technically identical but the album name is different (e.g. artist released track as a single and on a complete album, or produced a deluxe/extended/etc. version in addition to the regular album, or artist includes a previously released track as part of a compilation)
    * This tool gives preference to the track belonging to the larger album (e.g. the deluxe version) and replaces all instances of the regular album track with the deluxe version
    * This tool gives preference to the album version over the compilation version
    * This tool modifies compilation tracks **one-way** ONLY: 
        * Some inventoried tracks belong to a compilation and are also part of an inventoried album (whether or not that album track is also inventoried): the compilation tracks will be *CHANGED* into the album version
        * Some inventoried tracks belong to a compilation and but not found anywhere else in your inventoried tracks (whether or not they are present on other albums by the artist): compilation tracks will *REMAIN UNCHANGED*

* More to come...

### DISCLAIMER
This tool does NOT guarantee perfect results! I've tried to brainstorm potential edge cases, but don't assume I thought of everything. **Please use the cleaner tool at your own risk.**

## How To Use
### Setup
1. Create virtual environment and install required packages (tekore, pandas, numpy).
2. Create Spotify developer credentials and either directly modify the values in config_to_file.py or save them in your shell environment as `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI`.
3. Run python config_to_file.py and log in with your Spotify account.

### Export your playlists and other saved content
It's useful to store the information on disk to avoid retrieving the data more times than necessary if anything goes wrong during the cleaning stage. 
1. Run python export.py
2. Run python cleanup.py or use the functions in a Jupyter notebook to work interactively (safer).