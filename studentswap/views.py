from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Item, User
from actions.models import Action
from comments.models import Comment
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse


import random

# Create your views here.

# home view
def home(request):
    return render(request, "studentswap/index.html")

def buy(request):
    itemList = Item.objects.all().order_by('-date_posted')
    return render(request, "studentswap/product/buy.html", {"productlist": itemList})


#list view
def buyitem(request):
    itemList=Item.objects.all().order_by('-date_posted')
    listbycategory=[]
    itemcategory=request.GET.get('category', None)
    if itemcategory is not None:
        for item in itemList:
            if item.category.strip() == itemcategory.strip():
                listbycategory.append(item)
        return render(request, "studentswap/product/buy.html", {"productlist": listbycategory})
    else:
        return render(request, "studentswap/product/buy.html", {"productlist": itemList})



#add view- form to fill in details
def sell(request):
    if request.method=="POST":
        category, subcategory = request.POST.get('subcategoryfilters').split("-")
        name = request.POST.get('itemname')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        category = category
        subcategory = subcategory
        is_listing=True
        user=User.objects.get(username=request.session.get("username"))

        # assigning default images to categories,subcategories as the application right now doesn't have scope for the user to upload their pictures.
        # all pictures taken from unsplash.com
        if category=="Furniture" :
            if subcategory=='Living Room Furniture':
                imageurl="images/furniture/phillip-goldsberry-fZuleEfeA1Q-unsplash.jpg"
            elif subcategory=='Dining Room Furniture':
                imageurl="images/furniture/samantha-gades-XDaa1RPb6n8-unsplash.jpg"
            elif subcategory=='Bedroom Furniture':
                imageurl="images/furniture/christopher-jolly-GqbU78bdJFM-unsplash.jpg"
            elif subcategory=='Home Office Furniture':
                imageurl="images/furniture/gian-paolo-aliatis-6AWuKs10_M4-unsplash.jpg"
            elif subcategory=='Other':
                imageurl="images/furniture/di_an_h-g_8MrEZAvyE-unsplash.jpg"

        elif category=="Electronic devices":
            if subcategory=='Computer & Accessories':
                imageurl="images/electronic-devices/clement-helardot-95YRwf6CNw8-unsplash.jpg"
            elif subcategory=='Mobile devices & Accessories':
                imageurl="/images/electronic-devices/charlesdeluvio-GXNo-OJynTQ-unsplash.jpg"
            elif subcategory=='Home Appliances':
                imageurl="images/electronic-devices/louis-hansel-ktVKZRYUP4Y-unsplash.jpg"
            elif subcategory=='Audio & Music':
                imageurl="images/electronic-devices/caleb-woods-VVuRLhyTmXM-unsplash.jpg"
            elif subcategory=='Other':
                imageurl="images/electronic-devices/photo-1496181133206-80ce9b88a853.avif"

        elif category=="Home Accessories":
            if subcategory=='Lighting':
                imageurl="images/home accessories/sincerely-media-VDPauwJ_sHo-unsplash.jpg"
            elif subcategory=='Bedding & Linens':
                imageurl="images/home accessories/susan-wilkinson-9I4gTSe3_Po-unsplash.jpg"
            elif subcategory=='Bathroom Accessories':
                imageurl="images/home accessories/curology-cI_LU-uAkcE-unsplash.jpg"
            elif subcategory=='Kitchen Accessories':
                imageurl="images/home accessories/annie-spratt-QOBHnWEg-mk-unsplash.jpg"
            elif subcategory == 'Desk Accessories':
                imageurl = "images/home accessories/freddie-marriage-vSchPA-YA_A-unsplash.jpg"

            elif subcategory=='Other':
                imageurl="images/home accessories/patrick-tomasso-1NTFSnV-KLs-unsplash.jpg"

        elif category == "Books":
            if subcategory=='Textbooks':
                imageurl = "images/books/Structure-and-Interpretation.jpg"
            elif subcategory == 'Notebooks':
                    imageurl = "images/books/Structure-and-Interpretation.jpg"
            elif subcategory == 'Study guides':
                    imageurl = "images/books/Structure-and-Interpretation.jpg"
            elif subcategory == 'Interview Prep':
                    imageurl = "images/books/Structure-and-Interpretation.jpg"
            elif subcategory == 'Other':
                    imageurl = "images/books/Structure-and-Interpretation.jpg"

        elif category == "Kitchenware":
            if subcategory=='Cookware':
                imageurl="images/kitchenware/cooker-king-AOVtEuU9UGc-unsplash.jpg"
            elif subcategory=='Cutlery':
                imageurl="images/kitchenware/anna-kumpan-e8SpIvBceJw-unsplash.jpg"
            elif subcategory=='Kitchen Tools & Utensils':
                imageurl="images/kitchenware/becca-tapert-A_L2xNKgENg-unsplash.jpg"
            elif subcategory=='Kitchen Appliances':
                imageurl="images/kitchenware/alexandre-boucey-IZF51fI0p5w-unsplash.jpg"
            elif subcategory=='Other':
                imageurl="images/kitchenware/cooker-king-zEgp30gYpKk-unsplash.jpg"

        else:
            imageurl='images/miscellaneous/daniel-norris-ZN_86cZrSN0-unsplash.jpg'


        newitem = Item(itemname=name, price=price, description=desc, category=category, subcategory=subcategory,imageurl=imageurl,imagealt=name,user=user,is_sold=is_listing)
        newitem.save()
        #log the action
        action=Action(user=user, verb=f"sold an item -{name} ", target=newitem)
        action.save()
        messages.add_message(request, messages.SUCCESS, "You successfully sold the item %s !" % newitem.itemname)
        return redirect("product_detail", productid=newitem.id)
    else:
        return render(request, "studentswap/product/sell.html",)


# displaying search results based on sample keywords entered by user
def searchresults(request):
    searchresultlist = []
    if request.method=='GET':
        keyword=request.GET.get('searchitems','')
        itemList = Item.objects.all().order_by('-date_posted')
        for item in itemList:
                    if (keyword in ["electronics","computers","devices"]) and item.category == "Electronic devices":
                        searchresultlist.append(item)
                    elif (keyword in ["furniture","bed","table"]) and item.category == "Furniture":
                        searchresultlist.append(item)
                    elif (keyword in ["books","textbooks"]) and item.category == "Books":
                        searchresultlist.append(item)
                    elif (keyword in ["kitchen","cutlery","utensils"]) and item.category == "Kitchenware":
                        searchresultlist.append(item)
                    elif (keyword in ["lights","desk accessories"]) and item.category == "Home Accessories":
                        searchresultlist.append(item)
        return render(request, "studentswap/product/searchresults.html", {"productlist": searchresultlist})



# detail view - if the user sees the product detail, add it to recently viewed list
def productinfo(request,productid):
    itemList = Item.objects.all().order_by('-date_posted')
    comments=Comment.objects.filter(item=productid).order_by('-datecommented')
    for item in itemList:
        if item.id==productid:
            item.save()
            break
    return render(request, "studentswap/product/product.html", {"item": item, 'comments':comments})


#
# # edit view- edit view renders the form where the user can make changes
def edit(request,productid):
    itemList = Item.objects.all()
    for item in itemList:
        if(productid==item.id):
            return render(request,"studentswap/product/editlisting.html",{"item": item})
#
#
#savechanges view actually saves the changes once the form is submitted
def savechanges(request,productid):
    itemList = Item.objects.all()
    category, subcategory = request.POST.get('subcategoryfilters').split("-")
    category = category
    subcategory = subcategory
    print( category, subcategory)
    #logging the user action
    user = User.objects.get(username=request.session.get("username"))


    for item in itemList:
        if(productid==item.id):

            if request.POST.get('desc')!=item.description:
                action = Action(user=user, verb=f"edited the item's description to '{ request.POST.get('desc')}'", target=item)
                action.save()
            item.itemname=request.POST.get('itemname')
            if request.POST.get('itemname')!=item.itemname:
                action = Action(user=user, verb=f"edited the item's name to '{request.POST.get('itemname')}'", target=item)
                action.save()
            item.description=request.POST.get('desc')
            item.price=request.POST.get('price')
            item.category=category
            item.subcategory=subcategory
            item.save()
            break
    messages.add_message(request, messages.INFO, "You successfully edited the item %s !" % item.itemname) #success msg
    return redirect("product_detail", productid=item.id)


# delete views- for confirming the deletion and actually deleting it
def deleteconfirmation(request,productid):
    return render(request, "studentswap/product/deleteconfirmation.html",{"productid":productid})

# search for the item using it's id and delete it from the database
def delete(request,productid):
    itemList = Item.objects.all()
    # logging the user action
    user = User.objects.get(username=request.session.get("username"))
    for item in itemList:
        if item.id == productid:
            item_name = item.itemname
            action = Action(user=user, verb=f"deleted the item {item_name}", target=None)
            action.save()
            item.delete()
            break
    messages.add_message(request, messages.WARNING, "You successfully deleted the item %s !" % item.itemname)
    return redirect('buy')

# sending subcategories for a chosen category
def getsubcategories(request):
    is_ajax= request.headers.get('x-requested-with')== 'XMLHttpRequest'
    if is_ajax and request.method =="GET":
        try:
            category=request.GET.get('category')
            subcategories=[]
            if category=="Furniture":
                subcategories=['Living Room Furniture','Dining Room Furniture','Bedroom Furniture',
                           'Home Office Furniture','Other']
            elif category=="Electronic devices":
                subcategories=['Computer & Accessories','Mobile devices & Accessories','Home Appliances',
                           'Audio & Music','Other']
            elif category == "Home Accessories":
                subcategories = ['Lighting', 'Bedding & Linens', 'Bathroom Accessories', 'Kitchen Accessories',
                         'Desk Accessories',
                         'Other']
            elif category == "Kitchenware":
                subcategories = ['Cookware', 'Cutlery', 'Kitchen Tools & Utensils', 'Kitchen Appliances',
                         'Other']
            elif category == "Books":
                subcategories = ['Textbooks', 'Notebooks', 'Study guides','Interview Prep',
                         'Other']
            return JsonResponse({'subcategories' : subcategories})
        except:
            return JsonResponse({'error': 'error'}, status=200)
    else:
        return JsonResponse({'error': 'error'}, status=400)


# filter side navigation bar. Applying various filters based on what the user selected.
def filter(request):
    price = request.GET.get('price',None)
    category=request.GET.get('category',None)
    subcategory=request.GET.get('subcategory',None)
    date=request.GET.get('date',None)
    itemList = Item.objects.all()

 # filter subcategory for the selected category
    if category :
        itemList = Item.objects.filter(category=category)
    if subcategory:
        itemList = itemList.filter(subcategory=subcategory)
    if category and subcategory:
        itemList = itemList.filter(category=category, subcategory=subcategory)

    # splitting the price range into lower and upper values
    if price:
        low_price,high_price=price.split("-")
        low_price = low_price.strip("")
        high_price = high_price.strip("")

        itemList = itemList.filter(Q(price__gte=low_price) & Q(price__lte=high_price))

   # if date is selected then order it by latest or oldest
    if date is not None:
        if date == "Sort by Latest":
            itemList=itemList.order_by('-date_posted')
        elif date == "Sort by Oldest":
            itemList=itemList.order_by('date_posted')

    return render(request, "studentswap/product/buy.html", {"productlist": itemList})

# view to add comments and update the UI along with the existing comments

def addcomment(request,productid,username):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        comment = request.POST.get('comment')
        # print(comment)
        try:
            u = User.objects.get(username=username)
            i = get_object_or_404(Item, pk=productid)
            comment=Comment(user=u,item=i,comment=comment)
            action = Action(user=u, verb="commented on the item ", target=i)
            action.save()
            comment.save()
            # return the comment to be shown on the UI with it's details
            return JsonResponse({'success': True, 'message': comment.comment,'author': comment.user.username, 'date': comment.datecommented, 'id':comment.id})
        except:
            return JsonResponse({'error' :'error'},status=200)
    else:
        return JsonResponse({'error': 'error'}, status=400)

# view to delete a particular comment
def deletecomment(request,commentid):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            comment= Comment.objects.get(pk=commentid)
            commentid=comment.id
            comment.delete()
            # return success message on deleting the comment
            return JsonResponse({'success': True, 'id':commentid})
        except:
            return JsonResponse({'error' :'error'},status=200)
    else:
        return JsonResponse({'error': 'error'}, status=400)

def savecomment(request, commentid):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    updatedcomment= request.POST.get('comment')
    if is_ajax and request.method == "POST":
        comment = request.POST.get('comment')
        print(comment)
        try:
            comment = Comment.objects.get(pk=commentid)
            comment.comment=updatedcomment
            comment.save()
            # edit the comment
            return JsonResponse({'success': True, 'message': comment.comment,'author': comment.user.username, 'date': comment.datecommented,'id':comment.id})
        except:
            return JsonResponse({'error' :'error'},status=200)
    else:
        return JsonResponse({'error': 'error'}, status=400)

