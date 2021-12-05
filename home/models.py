from django.db import models
from django.contrib.auth import get_user_model
from common.models import ConfigChoice
User = get_user_model()


# Create your models here.
class Estimation(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.ForeignKey(ConfigChoice, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="estimation_logo/")
    value = models.CharField(max_length=200)



class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    family_type = models.ForeignKey(ConfigChoice, on_delete=models.CASCADE)


class Facility(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    bedroom = models.CharField(max_length=200)
    floor = models.CharField(max_length=200)
    area = models.CharField(max_length=200)


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField()
    value = models.DecimalField(max_digits=3, decimal_places=2)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery/")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)


class FavouriteProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

