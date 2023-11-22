from credentials import CLIENT_ID, CLIENT_SECRET, SP_REDIRECT_URI, SCOPE
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from googlesearch import search
import pandas as pd
import sqlite3

def get_artist_id(artist_name: str) -> str:
    """
    Performs a google search to get the artist id from the first url

    Args:
        artist_name: artist to be searched
    """
    query = "spotify " + artist_name
    search_results = list(search(query, num_results=1))[0]
    artist_id = search_results.rsplit(sep='/', maxsplit=1)[1]

    return artist_id


def extract_album_data(artist_id: str) -> list:
    """
    Gets the last five albums from the selected artist

    Args:
        artist_id: artist spotify id
    """
    raw_album_data = sp.artist_albums(artist_id, limit=5)

    return raw_album_data if raw_album_data else []
       

def extract_album_tracks(album_ids: list) -> list:
    """
    Gets five songs based on album id
    """
    raw_tracks_data = []

    for id in album_ids:
        raw_tracks_data.append(sp.album_tracks(id, limit=5))
    
    return raw_tracks_data
    

def transform_album_data(raw_data: list):
    """
    Selects the information of interest from raw album data and remove duplicates

    Args:
        raw_data: extracted data
    """
    album_data = []
    for d in raw_data["items"]:
        album_data.append(
            {
                "artist": d["artists"][0]["name"],
                "album_name": d["name"],
                "album_id": d['id'],
                "release_date": d["release_date"],
                "total_tracks": d['total_tracks'],
                "type": d["album_type"],
            }
        )
    
    album_df = pd.DataFrame(album_data)
    album_df.drop_duplicates(inplace=True)
    
    return album_df

def transform_track_data(raw_data: list, album_ids: list):
    """
    Selects the information of interest from raw tracks data and remove duplicates

    Args:
        raw_data: extracted data
    """
    tracks_data = []

    for i in range(len(raw_data)):
        for d in raw_data[i]["items"]: 
            tracks_data.append(
                    {
                        "artist": d["artists"][0]["name"],
                        "track_name": d["name"],
                        "track_id": d['id'],
                        "duration": d["duration_ms"],
                        "album": album_ids[i],
                        "type" : d["type"]
                    }
            )
    
    tracks_df = pd.DataFrame(tracks_data)
    tracks_df.drop_duplicates(inplace=True)
    
    return tracks_df


def load_data(data_df: pd.DataFrame, table: str) -> None:
    """
    Stores transformed data

    Args:
        data_df: Data to be stored
        table: Name of the table
    """
    data_df.to_sql(name=table, con=connection, if_exists='replace', index=False)


if __name__ == "__main__":
    connection = sqlite3.connect('./spotify.db')

    sp = Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                       client_secret=CLIENT_SECRET,
                                       redirect_uri=SP_REDIRECT_URI,
                                       scope=SCOPE))
    
    artist_name = input("Enter an artist name: ")

    if not artist_name:
        print("An artist name is needed")
        exit(1)
    
    artist_id = get_artist_id(artist_name)

    raw_album_data = extract_album_data(artist_id)
    
    if not raw_album_data:
        print("Error getting artist information")
        exit(1)

    albums_df = transform_album_data(raw_album_data)

    raw_tracks_data = extract_album_tracks(albums_df['album_id'])
    tracks_df = transform_track_data(raw_tracks_data, albums_df['album_name'])

    load_data(albums_df, 'album_table')
    load_data(tracks_df, 'tracks_table')

    print('Albums:')
    print(pd.read_sql('SELECT * FROM album_table', connection))
   
    print('\nTracks:')
    print(pd.read_sql('SELECT album, GROUP_CONCAT(track_name) AS tracks FROM tracks_table GROUP BY album', connection))

    connection.close()