from django.db import models

# Create your models here.
class Novel(models.Model):
    name = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    averageRating = models.FloatField()

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name