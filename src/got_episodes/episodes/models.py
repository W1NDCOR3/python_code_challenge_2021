from django.db import models

class Episode(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=10, unique=True)
    runtime = models.CharField(max_length=50)
    rating = models.CharField(max_length=20)

    def __str__(self):
        return self.title
