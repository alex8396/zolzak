from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib import messages

from .http_model import (
    SignUpRequest, SignInRequest, SimpleFailResponse, SimpleSuccessResponse, SignInResponse, GenreResponse,
    MovieResponse
)
from .models import User, Movie, Genre


class SignUp(APIView):
    def get(self, request):
        return render(request, 'user.html')

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not username.strip() or not password.strip() or not confirm_password.strip():
            messages.error(request, '입력 필드를 모두 채워주세요.')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request,'확인 비밀번호가 일치하지 않습니다.')
            return redirect('signup')

        data_dict = {
            "username": username,
            "password": password,
        }

        # validate input
        try:
            request_data = SignUpRequest(**data_dict)
        except ValidationError:
            messages.error(request, '유효하지 않은 요청입니다.')
            return redirect('signup')
        if User.objects.filter(name=request_data.username).exists():
            messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디로 시도해주세요.')
            return redirect('signup')

        # Create user
        try:
            User.objects.create_user(
                name=request_data.username,
                password=request_data.password,
            )
        except:
            messages.error(request, '등록하는 과정에서 오류가 발생했습니다.')
            return redirect('signup')
        messages.error(request, '성공적으로 등록되었습니다!')
        return redirect('signin')

        return JsonResponse(
            SimpleSuccessResponse(success=True).model_dump(),
            status=201,
        )


class SignIn(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username.strip() or not password.strip():
            messages.error(request, '아이디나 비밀번호를 입력하세요.')
            return redirect('signin')

        try:
            auth_info = SignInRequest(username=username, password=password)
        except ValidationError:
            messages.error(request, '유효하지 않은 요청입니다.')
            return redirect('signin')

        user = authenticate(name=auth_info.username, password=auth_info.password)
        if user:
            login(request, user)
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            return redirect('/')
        else:
            messages.error(request, '등록되지 않은 아이디나 비밀번호입니다.')
            return redirect('signin')


class SignOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        Token.objects.filter(key=request.auth).delete()
        logout(request)
        messages.error(request, '로그아웃 되었습니다.')
        return redirect('signin')


class GetMovieInfo(APIView):
    def get(self, request, movie_id):
        if movie_id:
            try:
                movie = Movie.objects.get(movie_id=movie_id)
                genres = movie.genre_ids.all()
                genre_list = [GenreResponse(genre_id=genre.genre_id, name=genre.name).dict() for genre in genres]

                movie_data = MovieResponse(
                    movie_id=movie.movie_id,
                    title=movie.title,
                    overview=movie.overview,
                    release_date=movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
                    popularity=movie.popularity,
                    vote_average=movie.vote_average,
                    vote_count=movie.vote_count,
                    poster_path=movie.poster_path,
                    backdrop_path=movie.backdrop_path,
                    adult=movie.adult,
                    original_language=movie.original_language,
                    original_title=movie.original_title,
                    genres=genre_list
                )
                return JsonResponse(movie_data.model_dump(), status=200)
            except:
                return JsonResponse(SimpleFailResponse(success=False, reason="Invalid request.").model_dump(),
                                    status=400)

def search(request):
    return render(request, 'search.html')

class GetGenreInfo(APIView):
    def get(self, request, genre_id):
        try:
            genre = Genre.objects.get(genre_id=genre_id)
            genre_data = GenreResponse(
                genre_id=genre.genre_id,
                name=genre.name
            )
            return JsonResponse(genre_data.model_dump(), status=200)
        except:
            return JsonResponse(SimpleFailResponse(success=False, reason="Invalid request.").dict(), status=400)

def genre(request):
    return render(request, 'genre.html')

def recom(request):
    return render(request, 'recom.html')

def index(request):
    return render(request, 'index.html')