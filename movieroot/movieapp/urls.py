from django.urls import path
from . import views
from .views import SignUp, SignIn, SignOut, GetMovieInfo, GetGenreInfo

urlpatterns = [
    path('', views.index, name="home"),
    path('home/', views.index, name="home"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('signin/', SignIn.as_view(), name="signin"),
    path('signout/', SignOut.as_view(), name="signout"),
    path("search/", views.search, name="search"),
    path("genre/>", views.genre, name="genre"),
    path("recom/>", views.recom, name="recom")
]
