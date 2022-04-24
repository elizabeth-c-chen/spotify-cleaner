import os
import math
import string
import unicodedata
import tekore as tk
import pandas as pd


def clean_filename(filename, replace=' '):
    """
    Modification of Safe Filename String Converter by wassname on GitHub
    Original Source: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    """
    char_limit = 255
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    


def get_num_subsets(x, chunk_size):
    return int(math.ceil(x / chunk_size))


# Helper function to return track information as a dictionary
def get_track_info(track_item):
    info = {
        'id': track_item.id,
        'name': track_item.name,
        'artist': track_item.artists[0].name,
        'album': track_item.album.name,
        'explicit': track_item.explicit
    }
    return info


# Helper function to return album information as a dictionary
def get_album_info(album_item):
    info = {
        'id': album_item.id,
        'name': album_item.name,
        'artist': album_item.artists[0].name,
        'type': album_item.type,
        'release_date': album_item.release_date
    }
    return info


class SpotifyExporter:
    def __init__(self, conf):
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)  
        self.spotify = tk.Spotify(token, chunked_on=True)
        self.user_id = self.spotify.current_user().id
        self.root_dir = 'Spotify_Data-' + self.user_id # Name of folder to store exported data
        self.make_dirs()
        
    def make_dirs(self):
        root_dir = os.path.relpath(self.root_dir)
        playlists_dir = os.path.join(root_dir, "Playlists")
        library_dir = os.path.join(root_dir, "Saved_Library")
        for dir_path in [root_dir, playlists_dir, library_dir]:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path) # Create the folder on OS

    # Exports all playlists with tracks to individual CSV files
    def download_playlists(self):
        playlist_ids = self.get_all_playlist_ids() # Get all playlist IDs
        print(f"Downloading {len(playlist_ids)} playlists")
        for playlist_id in playlist_ids:
            # This first part sets up the dictionary needed for storing the data subsets.
            # We have to store the data as subsets to account for playlists longer than 
            # 100 tracks. Spotify's API limits the number of tracks you can retrieve in 
            # an API call to just 100 tracks. 
            playlist_name = self.get_playlist_name(playlist_id)
            print(f"{playlist_name}")
            num_items = self.get_playlist_length(playlist_id)
            num_subsets = get_num_subsets(num_items, 100)
            playlist_tracks = []
            # Retrieve each subset of tracks
            for index in range(num_subsets):
                playlist_tracks += self.spotify.playlist_items(playlist_id, limit=100, offset=100*index).items
            # Now we are just taking all the track IDs 
            all_track_ids = [p_track.track.id for p_track in playlist_tracks]
            # tekore's Spotify library for Python has a great feature chunked() which 
            # groups together a bunch of API calls and prevents us from getting a
            # TooManyRequests error.
            with self.spotify.chunked():  
                all_track_info = self.spotify.tracks(all_track_ids)
            df_playlist = []
            # For each track, append the data to an array.
            for track_item in all_track_info:
                row = get_track_info(track_item)
                df_playlist.append(row)
            df = pd.DataFrame(df_playlist)
            filename = clean_filename(playlist_name)
            df.to_csv(f"{self.root_dir}/Playlists/{filename}.csv", index=False)
        print("Success! All playlists retrieved.")

    # Exports all liked tracks with relevant information to CSV
    def download_liked_tracks(self):
        all_tracks = self.get_all_liked_tracks()
        df_tracks = []
        for track_item in all_tracks:
            row = get_track_info(track_item)
            df_tracks.append(row)
        df = pd.DataFrame(df_tracks)
        df.to_csv(f"{self.root_dir}/Saved_Library/Liked_Songs.csv", index=False)
        print("Success! All liked song info retrieved.")

    # Exports all liked albums with relevant information to CSV
    def download_liked_albums(self):
        all_albums = self.get_all_liked_albums()
        df_albums = []
        for album_item in all_albums:
            row = get_album_info(album_item)
            df_albums.append(row)
        df = pd.DataFrame(df_albums)
        df.to_csv(f"{self.root_dir}/Saved_Library/Liked_Albums.csv", index=False)
        print("Success! All liked album info retrieved.")

    # Helper function to get the length of a playlist (for subsetting).
    def get_playlist_length(self, playlist_id):
        playlist_items = self.spotify.playlist_items(playlist_id, fields=['total'])
        return playlist_items['total']

    # Helper function to get playlist name for writing data to file.
    def get_playlist_name(self, playlist_id):
        playlist = self.spotify.playlist(playlist_id, fields=['name'])
        return playlist['name']

    # Helper function to retrieve all playlist IDs belonging to current user.
    def get_all_playlist_ids(self):
        total_playlists = self.spotify.playlists(self.user_id).total
        num_subsets = get_num_subsets(total_playlists, 50)
        all_playlists = []
        for index in range(num_subsets):
            all_playlists += self.spotify.playlists(self.user_id, limit=50, offset=50*index).items
        return [playlist.id for playlist in all_playlists]

    # Helper function to retrieve all IDs of liked tracks belonging to current user
    def get_all_liked_tracks(self):
        total_tracks = self.spotify.saved_tracks(limit=50).total
        num_subsets = get_num_subsets(total_tracks, 50)
        all_tracks = []
        for index in range(num_subsets):
            all_tracks += self.spotify.saved_tracks(limit=50, offset = 50*index).items
        return [l_track.track for l_track in all_tracks]

    # Helper function to retrieve all IDs of liked albums belonging to current user
    def get_all_liked_albums(self):
        total_albums = self.spotify.saved_albums(limit=50).total
        num_subsets = get_num_subsets(total_albums, 50)
        all_albums = []
        for index in range(num_subsets):
            all_albums += self.spotify.saved_albums(limit=50, offset = 50*index).items
        return [l_album.album for l_album in all_albums]


if __name__ == '__main__':
    conf = tk.config_from_file('tekore.cfg')
    Exporter = SpotifyExporter(conf)
    Exporter.download_playlists()
    Exporter.download_liked_albums()
    Exporter.download_liked_tracks()