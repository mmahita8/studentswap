from django.contrib import admin
from django.urls import path
from . import views

app_name='users'

urlpatterns = [

    # path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile_detail'),  # profile detail
    path('editprofile/<str:username>', views.editprofile, name='profile_edit'),  # get edit form for editing profile details
    path('saveprofile/<str:username>', views.saveprofile, name='saveprofilechanges'),  # saving profile edit details
    path('loggedin/', views.login_user, name="login"),  # login
    path('logout/', views.logout_user, name="logout"),  # logout
    path('wishlist/delete/<int:productid>/', views.wishlistdelete, name="wishlistdelete"),
    path('dashboard/<str:username>', views.dashboard, name="dashboard"),  # user dashboard
    path('home/feed', views.homeactivityfeed, name='homefeed'), #home page showing activity feed for logged in users
    path('wishlist/<int:productid>/<str:username>',views.wishlist, name="wishlist"), #to add item to wishlist
    path('wishlist/<str:username>',views.wishlistpage, name="wishlistpage"),  #to go to wishlist page

]
