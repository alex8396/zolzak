from typing import Optional, List

from pydantic import BaseModel


class SimpleFailResponse(BaseModel):
    success: bool
    reason: str


class SimpleSuccessResponse(BaseModel):
    success: bool


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    success: bool
    token: str


class GenreResponse(BaseModel):
    genre_id: int
    name: str


class MovieResponse(BaseModel):
    movie_id: int
    title: str
    overview: Optional[str]
    release_date: Optional[str]
    popularity: Optional[float]
    vote_average: Optional[float]
    vote_count: Optional[int]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    adult: bool
    original_language: str
    original_title: str
    genres: List[GenreResponse]
