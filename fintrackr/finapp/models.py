import requests # <- own
from django.db import models
from django.core.files.base import ContentFile

# Create your models here.

# User handles users - name, email, password 
# and user id which is used to relate and identify data indicating to that uses 
class Users(models.Model):
    
    # user_id = models.DecimalField(max_digits=6, decimal_places=0, primary_key=True)
    user_id     = models.BigAutoField(primary_key=True)
    name        = models.CharField(max_length=254)
    email       = models.EmailField(max_length=254, unique=True)
    password    = models.CharField(max_length=254)

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Download the image from the external URL and save it as the profile picture
        if not self.profile_picture and self.name:
            url = f"https://api.dicebear.com/6.x/thumbs/svg?seed={self.name}"
            response = requests.get(url)

            if response.status_code == 200:
                self.profile_picture.save(f"{self.name}.svg", ContentFile(response.content), save=False)

        super(Users, self).save(*args, **kwargs)


# Expenses tables handles data of users like amount, name, date, etc. 
# and user id used as foreignkey for identifying data on specific a user  
class Expenses_Table(models.Model):
    expenses_id     = models.BigAutoField(primary_key=True)
    user_id         = models.ForeignKey(Users, on_delete= models.CASCADE) # on_delete means it delete the data if the foreign key deleted
    # categories_id = models.ForeignKey(Categories_Table, on_delete= models.CASCADE)
    categories_name = models.CharField(max_length=254, null=True, default="")
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    date            = models.DateField(auto_now=False, auto_now_add=False)
    description     = models.CharField(max_length=254, null=True, default="")
    income          = models.BooleanField(default=False)