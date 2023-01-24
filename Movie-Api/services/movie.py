from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie_by_id(self, id: int):
        movies = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movies

    def get_movie_by_category(self, category: str):
        movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movies
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
    
    def update_movie(self, id: int, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.rating = data.rating
        movie.year = data.year
        movie.category = data.category
        self.db.commit()
    
    def delete_movie(self, id:int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
    