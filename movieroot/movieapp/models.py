from datetime import datetime, timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Model, CharField, IntegerField, ManyToManyField, TextField, \
    BooleanField, DateField, FloatField

MAX_STR_LEN = 100


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(
            self,
            name,
            password,
    ):
        if not name:
            raise ValueError("must have name!")
        if not password:
            raise ValueError("must have password!")

        user = self.model(
            name=name,
            created_at=datetime.now(tz=timezone.utc),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        user = self.create_user(
            name=name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name


class Genre(Model):
    genre_id = models.IntegerField(primary_key=True)
    name = CharField(null=False, max_length=30)


class Movie(Model):
    adult = BooleanField(default=False)
    backdrop_path = CharField(null=True, max_length=MAX_STR_LEN)
    genre_ids = ManyToManyField(Genre)
    movie_id = IntegerField(null=False, unique=True)
    original_language = CharField(null=False, max_length=10)
    original_title = CharField(null=False, max_length=MAX_STR_LEN)
    overview = TextField(null=True)
    popularity = FloatField(null=True)
    poster_path = CharField(null=False, max_length=MAX_STR_LEN)
    release_date = DateField(null=True)
    title = CharField(null=False, max_length=MAX_STR_LEN)
    vote_average = FloatField(null=True, default=0)
    vote_count = IntegerField(null=True, default=0)

    def __str__(self):
        return "Movie: %s - %s" % (self.movie_id, self.title)
