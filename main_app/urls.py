

# Add the include function to the import
from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('cats/', views.cats_index, name='index'),
  path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
  path('cats/create/',views.CatCreate.as_view(), name='cats_create'),
  path('cats/<int:pk>/update', views.CatUpdate.as_view(), name='cats_update'),
  path('cats/<int:pk>/delete', views.CatDelete.as_view(), name='cats_delete'),
  path('cats/<int:cat_id>add_feeding/', views.add_feeding, name ='add_feeding'),
  ##the cat id is a view function thats why we need the ID for it  
  #the name types are for the URL pathname 

  path('toys/', views.ToyIndex.as_view(), name='toy_index'),
  path('toys/create', views.ToyCreate.as_view(), name='toy_create'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy_detail'),
  path('toys/<int:pk>/update', views.ToyUpdate.as_view(), name='toy_update'),
  path('toys/<int:pk>/delete', views.ToyDelete.as_view(), name='toy_delete'),
  
  
  ## this path assoiatees toys to a specifc cat 
  path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'), 


#making urls for the photo
#viewsegments are named after the url they try to mimic the same thing thorughout the line  
path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),


#for accounts and signup
path('accounts/signup/', views.signup, name='signup'),

]

