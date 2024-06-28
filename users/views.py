from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Details
from studentswap.models import Item
from actions.models import Action
from django.contrib.auth import authenticate
from django.http import HttpResponse
from comments.models import Comment

# Create your views here.

def register(request):
    if request.method=="POST":

        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        campus=request.POST.get('incampus')
        user = User.objects.create_user(username, email, password, first_name=firstname,last_name=lastname)
        details,created=Details.objects.get_or_create(user=user)
        details.campus=campus
        details.save()
        # session variables
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.INFO,
                             "You successfully registered with the username %s !" % user.username)  # success msg
        return redirect('users:profile_detail',username=username )
    else:
        return render(request, "users/user/register.html", )

def profile(request,username):
    user=get_object_or_404(User,username=username)
    return render(request, "users/user/profile.html",{"user": user} )

def editprofile(request,username):
    user = get_object_or_404(User, username=username)
    return render(request, "users/user/editprofile.html",{"user": user} )

def saveprofile(request,username):
    if request.method == "POST":
        u = User.objects.get(username=username)
        details=Details.objects.get(user=u)
        u.first_name = request.POST.get('firstname')
        u.last_name = request.POST.get('lastname')
        u.email = request.POST.get('email')
        newpassword=request.POST.get('password')
        if newpassword:
            u.set_password(newpassword)
            # log the action
        role=request.POST.get('role')
        if role:
            details.role=role
            details.save()
            action = Action(user=u, verb="'s role was changed by Admin. Click here to see -", target=u)
            action.save()
        details.campus=request.POST.get('incampus')
        u.save()
        details.save()
        return redirect('users:profile_detail',username=username)


# views for logging in and logging out for both regular and admin users
def login_user(request):
    username=request.POST.get("username")
    pwd=request.POST.get("password")

    user= authenticate(username=username, password=pwd)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        return redirect('users:profile_detail',username=username )
    else:
        # prompt the user if entered password or username are incorrect
        messages.add_message(request, messages.WARNING, "Incorrect password or username. Please try again" )
        return redirect('home')  # a landing page with welcome message will be shown if the user is not logged in



def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('home')


# adding item to wishlist
def wishlist(request,productid,username):
    comments = Comment.objects.all()
    u = User.objects.get(username=username)
    i = get_object_or_404(Item, pk=productid)
    for comment in comments:
        if comment.user == u.id and comment.item == i.id:
            comment.is_wishlist = True
            comment.save()
            break
    return HttpResponse(status=204)


#go to wishlist page and show all the items in wishlist
def wishlistpage(request,username):
    comments = Comment.objects.all()
    wishlist=[]
    for comment in comments:
        if comment.user.username == username and comment.is_wishlist==True:
            wishlist.append(comment)
    return render(request, "users/user/wishlist.html", {"productlist": wishlist})
#
# # dashboard view- where the user can edit  and delete (only admin) their listings
#shows recently viewed and mylistings


# to remove item from wishlist, change the boolean to false
def wishlistdelete(request,productid):
    itemList = Item.objects.all()
    for item in itemList:
        if item.id == productid:
            item.is_wishlist=False
            item.save()
            break
    messages.add_message(request, messages.WARNING, "You successfully deleted the item %s from wishlist!" % item.itemname)
    return redirect('users:wishlistpage')


def dashboard(request,username):
    user = User.objects.get(username=request.session.get("username"))
    actions=Action.objects.all()
    actionList = actions.filter(user = user).order_by('-created')
    itemlist=Item.objects.all().order_by('-date_posted')
    mylistings=[]
    recentlyviewed=[]
    for item in itemlist:
        if username == item.user.username:
            if item.is_sold:
                mylistings.append(item)
            # if item.recently_viewed:
            #     recentlyviewed.append(item)
    mylists= {"mylistings":mylistings,
              "recentlyviewed":recentlyviewed}
    return render(request, "users/user/dashboard.html", {"actions" : actionList, "mylistings":mylistings})
#

def homeactivityfeed(request):
    actions = Action.objects.all().order_by('-created')
    return render(request, "studentswap/product/homepagefeed.html",{"actions" : actions})