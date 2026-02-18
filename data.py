import urllib.request
import zipfile
import pandas as pd
import config

def download():
    if config.DATA_DIR.exists():
        return
    
    config.DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
    zip_path = config.DATA_DIR.parent / "ml-100k.zip"
    urllib.request.urlretrieve(config.MOVIELENS_URL, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(config.DATA_DIR.parent)
    zip_path.unlink()

def load():
    download()
    
    # Ratings
    ratings = pd.read_csv(
        config.DATA_DIR / 'u.data',
        sep='\t',
        names=['userId', 'movieId', 'rating', 'timestamp']
    )
    
    # Movies
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
              'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
              'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    
    movies = pd.read_csv(config.DATA_DIR / 'u.item', sep='|', encoding='latin-1', header=None)
    movies.columns = ['movieId', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown'] + genres
    movies = movies[['movieId', 'title'] + genres]
    
    return ratings, movies, genres