from django.db import models
from django.urls import reverse
# Import the User
from django.contrib.auth.models import User
# Create your models here.


class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    # dunder
    def __str__(self):
        return f'{self.color} {self.name}'

    def get_absolute_url(self):
        return reverse("toy_detail", kwargs={"pk": self.pk})
    # we use class based views here thats the onky reasib why pk was used




class Cat (models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
## heree is a many to many relationship 
    toys = models.ManyToManyField(Toy)
    #adding forgien key
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"cat_id": self.id})
    
class Feeding(models.Model):
    MEALS = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        )
    date = models.DateField('feeing date')
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    # this is similar to embeded relationships 
    # this cat right ehre is going to directly reference the one we have above ^^
#dunder method below

    def __str__(self):
        return f'{self.get_meal_display()} on {self.date}'

# feeding needs to be connected to cats. so wht does the feeding need? 

#we need a forign key that links the feeding to the model 

# below changes the ordering 
class meta: 
    ordering = ('-date',)
    
    
class Photo(models.Model):
    url = models.CharField(max_length=300)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

def __str__(self):
    return f"Photo for cat_it: {self.cat.name} @{self.url}"
# anytime a model is made then a make migration is done then a migrate 

