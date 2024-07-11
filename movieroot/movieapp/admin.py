from django.contrib import admin

from .models import User, Movie, Genre


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "password",
        "id",
        "name",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    list_filter = ("is_superuser", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("name", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "movie_id",
        "title",
        "overview",
        "popularity",
        "vote_average",
        "release_date",
    )
    list_filter = ("release_date",)
    search_fields = ("title",)
    ordering = ("-popularity",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "genre_id",
        "name",
    )
