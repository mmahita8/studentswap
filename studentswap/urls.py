from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),
    path('buy/items/<int:productid>/', views.productinfo, name='product_detail'), #product detail
    path('buy/items/', views.buyitem, name="buyitem"), #listitemsbycategory
    path('buy/items/all/', views.buy, name="buy"), #listallitems
    path('sell/', views.sell, name="sell"),  #addingitem
    path('searchresults/', views.searchresults, name="searchresults"),
    path('deleteconfirmation/<int:productid>/',views.deleteconfirmation,name="deleteconfirmation"),  #delete confirmation
    path('deleteitem/<int:productid>/',views.delete,name="delete"),   #actual deletion
    path('edititem/<int:productid>/',views.edit,name="edit"),#requesting edit form
    path('editingitem/<int:productid>/',views.savechanges,name="saveedit"),   #saving edited changes
    path('getsubcategories/', views.getsubcategories ,name='get_subcategories'),
    path('filter/', views.filter, name='filtered'),
    path('comment/<int:productid>/<str:username>/', views.addcomment, name='comment'), #add comment
    path('deletecomment/<int:commentid>/', views.deletecomment, name='deletecomment'),  # delete comment
    path('savecomment/<int:commentid>/', views.savecomment, name='savecomment'),  #editing and updating comment


]
