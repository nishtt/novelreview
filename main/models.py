from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Novel(models.Model):
    name = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    averageRating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True, max_length=500)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE)
    comment = models.TextField() 
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.novel.name}"
