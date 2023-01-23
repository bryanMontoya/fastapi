from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi app" #Nombre documentación swagger
app.version = "0.0.1" #Swagger

class User(BaseModel):
    email: str
    password :str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "email":
            raise HTTPException(status_code = 403, detail = "No valid credentials")
        
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length = 15, min_length = 5)
    overview : str
    year: int = Field(le = 2022, ge = 1900)
    rating: float
    category: str

    class Config: #Valores por defecto
        schema_extra = {
            "example": {
                "id" : 1,
                "title" : "Pelicula",
                "overview" : "Descripcion",
                "year" : 2022,
                "rating": 5,
                "category": "Mi categoria" 
            }
        }

movies = [{
    'id': 1,
    'title': 'Avatar',
    'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    'year': '2009',
    'rating': 7.8,
    'category': 'Acción' 
},
{
    'id': 2,
    'title': 'Avatar',
    'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    'year': '2009',
    'rating': 7.8,
    'category': 'Acción' 
}]

@app.get('/', tags = ['home']) #tag swagger
def message():
    return HTMLResponse('<h1>Hello World</h1>')

#uvicorn main:app --reload --port 8080 --host 0.0.0.0
#/docs swagger

@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "email" and user.password == "pass":
        token = create_token(user.dict())
        return JSONResponse(content = token, status_code = 200)
    return JSONResponse(content = [], status_code = 400)

@app.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 201, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content = movies, status_code = 201)

@app.get('/movie/{id}', tags = ['movie'], response_model = Movie)
def get_movie(id: int = Path(ge = 1, le = 2000)) -> Movie: #mayor o = a 1, menor a 2000
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content = movie) 
    return JSONResponse(content = [], status_code = 404) 

@app.get('/movies/', tags = ['movies'])
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)): #No se especifica en la url pero se reconoce como query param
    return [movie for movie in movies if movie["category"] == category]

@app.post('/movies',tags = ['movies']) #Body, no query param sino contenido peticion
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content = {"message" : "Pelicula añadida"})

@app.put('/movies/{id}', tags = ['movies'])
def update_movie(id: int, movie: Movie):
    for movie_list in movies:
        if movie_list['id'] == id:
            movie_list['title'] = movie.title
            movie_list['overview'] = movie.overview
            movie_list['year'] = movie.year
            movie_list['category'] = movie.category
            movie_list['rating'] = movie.rating
            return movies
        return "No movie with id " + str(id)

@app.delete('/movies/{id}', tags = ['movies'])
def delete_movie(id: int):
    for movie in movies:
        movies.remove(movie)
    return movies
