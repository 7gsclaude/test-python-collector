from django.forms import ModelForm 
from .models import Feeding


# djandgos form models is designed to make a html5 form from a model 
# and thats it

class FeedingForm(ModelForm): 
    class Meta: 
        # informs the form what model it will be for and what fields we ant inputs for 
        model = Feeding
        fields = ('date', 'meal')
        # if we dont specify these two fields it will default to my cat 
        