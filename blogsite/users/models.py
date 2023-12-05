from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from PIL import Image

# class AuthCustomUser(AbstractUser):
#     authentication_id = models.CharField(max_length=8, unique=True)
    
#     def __str__(self):
#         return self.username
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        """ 
        instead of super().save() -> this throws an error of force_insert 
        we can also use super(Profile,self).save(*args, **kwargs) -> unnecessary
        """
        img = Image.open(self.image.path)
        if img.height>300 and img.width>300:
            output_size = (100,100)
            img.thumbnail(output_size)
            img.save(self.image.path)
    

class Authentication(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    authentication_id = models.TextField()
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Authentication"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
    
    