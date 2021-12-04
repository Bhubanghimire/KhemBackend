from django.contrib import admin
from .models import Estimation, Project, Review, Gallery, FavouriteProject,Facility


# Register your models here.
@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = ["id","project","name","value"]


@admin.register(Facility)
class EstimationAdmin(admin.ModelAdmin):
    list_display = ["id","project","name","value"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id","name","description","family_type"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id","project","comment","value","rated_by"]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id","project","review"]


@admin.register(FavouriteProject)
class FavProjectAdmin(admin.ModelAdmin):
    list_display = ["id","project","user"]