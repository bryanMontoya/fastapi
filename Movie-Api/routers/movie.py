from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from fastapi import Path, Query, Depends
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    all_movies = MovieService(db).get_movies()
    return JSONResponse(content = jsonable_encoder(all_movies), status_code = 200)

@movie_router.get('/movie/{id}', tags = ['movies'], response_model = Movie, status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge = 0)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code = 404, content = {'message' : 'No encontrado'})
    return JSONResponse(content = jsonable_encoder(result), status_code = 201) 

@movie_router.get('/movies/', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)): #No se especifica en la url pero se reconoce como query param
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code = 404, content = {'message' : 'No se encontraron peliculas'})
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.post('/movies',tags = ['movies'], response_model = dict, status_code = 201, dependencies = [Depends(JWTBearer())]) #Body, no query param sino contenido peticion
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)    
    return JSONResponse(content = {"message" : "Pelicula registrada"}, status_code = 201)

@movie_router.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200, dependencies = [Depends(JWTBearer())])
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(content = {'message' : 'No se encontró la pelicula'}, status_code = 404)
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code = 201, content = {'message' : 'Pelicula modificada'})

@movie_router.delete('/movies/{id}', tags = ['movies'], dependencies = [Depends(JWTBearer())])
def delete_movie(id: int):
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code = 404, content = {'message':'No encontrado'})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code = 200, content = {'message' : 'Pelicula borrada'})
