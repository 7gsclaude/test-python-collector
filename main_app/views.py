from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import boto3
import uuid
# this is for a unique identifier that gets uploaded to AWS 

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
#not sure where to get this 
BUCKET = 'catcollector-2023-claudebucket'

# whenever buckets are set up they are typically assigned to a region. 
# for the base url we need to know what region our bucket is located in. 


#these models and forms are importred uphere 
# Add the following import
from django.http import HttpResponse

# Define the home view




# Add the Cat class & list and view function below the imports
# class Cat:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age


# cats = [
#     Cat('Lolo', 'tabby', 'foul little demon', 3),
#     Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#     Cat('Raven', 'black tripod', '3 legged cat', 4)
# ]
# Add new view



# def intro(request):
#   return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def home(request):
  return render(request, 'home.html')


def about(request):
    return render(request, "about.html")


#you place the login requred before the function you want to limit it forces people to go to the login  
@login_required
def cats_index(request):
    #.filter(user=request.user) only displays what is created by a certain user. 
    
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
#    here we get by id. this is set up as a single object and passed into a dictionary 
#they key here gets passed trhu tyhe param
   cat = Cat.objects.get(id=cat_id)
   feeding_form = FeedingForm()
   ##creating a list of toys that cats dont have 
   toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))
   return render(request,'cats/detail.html', {
      'cat':cat,
      'feeding_form': feeding_form,
      'toys':toys_cat_doesnt_have
      })
@login_required
def add_feeding(request, cat_id):
   #above there are two arements to be put here, it would be the cat_id and the request
   #in here i need to capture submitted form inputs 
   #capture subbmitted form input
   form = FeedingForm(request.POST)
   #doingn this validates teh form using a model form will validate the form, and the user inputed data
   if form.is_valid(): 
   # validate form inputs 
   # save a termporary copy of a new feeding using the form submission 
    new_feeding= form.save(commit=False) #saves in mnemory but no commit to the database 
   # associate the new feeding to the cat using the corresponding cat id 
    new_feeding.cat_id = cat_id
   # save teh enw feeding to the database 
    new_feeding.save()
   # return with a response to redirect
    return redirect('detail', cat_id=cat_id)


@login_required
def add_photo(request,cat_id):
    #capture photo file from the form submission
    photo_file = request.FILES.get('photo-file', None) #this name will be included with the form from the form input tag 
    # check if the file was included upon upload 
    if photo_file: 
    #if a file is incldued 
    #initialize a s3 client object
        s3 = boto3.client('s3')
        # the request in thie function will create photo files names to correspond with that 
    # create an indentifer for the photo file we need to know which photo uploaded that beloinged to which user 
        key = uuid.uuid4().hex[:6] + photo_file.name [photo_file.name.rfind('.'):] #rfind in strings will replace the index position of the thing your looking for 
        # 27d711 via this 6 code will add the name together 
        # 27d711.pgn is the goal here 
    # upload photo through amazon s3
    try:
        s3.upload_fileobj(photo_file, BUCKET, key) # this should start the upload process, 
    # generate a special url to a ccess the photo remotely 
        url = f'{S3_BASE_URL}{BUCKET}/{key}'
    # instantiatte an instance of the photo model 
        photo = Photo(url=url, cat_id=cat_id)
    #save the photo mmodel instance
        photo.save()
    # if something goes wrong, print error 
    #generates exception object as an error that way we can reference the error 
    except Exception as error:
        print('something went wrong with uploading to s3')
        print(error)
    # return  aresponse as a redirect back to the cat show page 
    return redirect ('detail', cat_id=cat_id) 
    


# this ass needs 3 args
def assoc_toy(request, cat_id,toy_id):
  Cat.obejcts.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)


def signup(request):
    error_message = 'none'
    #django view functions can hdnle post and get requests 
    # the way you check is with an if
    if request.method == 'POST': 
        #if get we anna present the user with a signup form and post/ handle a subission fromthe signup from . 
        #if not then send a new form to the template 
        
        #capture form inputs from submission
        form = UserCreationForm(request.POST)
        # validate the from inputs
        if form.is_valid(): 
        # save the new user
            user = form.save()
        #login the new user + redirectino 
            login(request, user)
            return redirect('index')
        #if invlaid then error message 
    else: 
        error_message = 'invalid credentials'
        
    form = UserCreationForm()
    return render(request,"registration/signup.html", {
        'form':form,
        'error': error_message
    })


@login_required
class CatCreate(LoginRequiredMixin ,CreateView):
   model = Cat
   fields = ('name','age', 'breed', 'description')
   success_url = '/cats/'
   
   #this form takes the self anf form 
#    renders a form with the users instance from the selfs user request 
   def form_valid(self, form):
       form.instance.user = self.request.user
       #to hand this back to wehere its pulled you involk super
       return super().form_valid(form)
       
   
   ### this all makes sure that it creates all new fields 
#    this create view basically says what are the fields to the form 
#what does it mean to pass an argument into a class, inheritance example 


class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']


class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'

###below is the toy index crud


class ToyIndex(LoginRequiredMixin, ListView):
  model = Toy


class ToyCreate (LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'


class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy


class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = '__all__'