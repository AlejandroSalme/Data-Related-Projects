# Spotify ETL Pipeline

![image title](https://img.shields.io/badge/Python-3.9-purple.svg) ![Image title](https://img.shields.io/badge/Spotipy-2.23.0-green.svg) ![Image title](https://img.shields.io/badge/Googlesearch-1.2.3-blue.svg) ![Image title](https://img.shields.io/badge/Sqlite3-3.44.0-yellow.svg)   ![Image title](https://img.shields.io/badge/Pandas-2.1.1-red.svg)  

This simple ETL (Extract, Transform, Load) pipeline uses the Spotify API to gather information about the albums and tracks of an artist. The process is designed to be user-friendly, allowing users to input an artist's name, and it automatically fetches the required data.

### Steps
#### 1. Artist Identification
- User inputs the name of the artist. 
- The program performs a Google search to find the artist's Spotify URL.
- Extracts the artist ID from the URL.

#### 2. Album Extraction and Transformation
- Utilizes the Spotify API to fetch raw data for the artist's five latest albums.
- Transforms the data to extract relevant information (e.g., album name, release date, etc.).

#### 3. Track Extraction and Transformation
- Extract five tracks from each album.
- Get selected information (e.g., track name, duration, etc.).

#### 4. Data Storage
- As an example, the data is stored in two separate tables: one for albums and another for tracks. Alternatively, the data could be stored in CSV files or other formats.

### Ouput

![Img](https://github.com/AlejandroSalme/Data-Related-Projects/blob/master/ETL/imgs/etl_example.png)

### How to use

1. Creating a Spotify App
    - Before running the pipeline, you need to create a [Spotify Developer App](https://developer.spotify.com/documentation/web-api).
    - Create a new application to obtain your Client ID and Client Secret. (Ensure to set the Redirect URI in your Spotify App settings)

2. Authentication
    - Modify the credentials.py file with your Spotify App credentials.

3. Install depencendies
    - spotipy
    - googlesearch-python
    - pandas
