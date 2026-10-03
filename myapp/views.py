import datetime


from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect


from myapp.models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from datetime import datetime
from django.db.models import Avg, Count
from textblob import TextBlob
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
# ------------------------------------signup------------------------------

def admin_check(user):
    return user.is_authenticated and user.is_staff



# =========================================================
# ADMIN CHECK
# =========================================================

def admin_check(request):

    if not request.user.is_authenticated:
        return redirect('/myapp/login/')

    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access Admin.")
        return redirect('/myapp/login/')

    return None


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard(request):

    check = admin_check(request)

    if check:
        return check

    user_count = customer.objects.count()
    seller_count = seller.objects.count()
    return render(request, 'admin_dashboard.html', {
    'user_count': user_count,
    'seller_count': seller_count,
        })


# =========================================================
# VIEW USERS
# =========================================================

def admin_users(request):

    check = admin_check(request)

    if check:
        return check

    users = customer.objects.all()

    return render(request, 'admin_users.html', {
    'users': users
})


# =========================================================
# VIEW USER DETAILS
# =========================================================

def admin_user_view(request, id):

    check = admin_check(request)

    if check:
        return check

    user = customer.objects.get(id=id)

    return render(request, 'admin_user_view.html', {
    'user': user
})

# =========================================================
# BAN USER
# =========================================================

def admin_ban_user(request, id):

    check = admin_check(request)

    if check:
        return check

    user = customer.objects.get(id=id)

    user.LOGIN.is_active = False
    user.LOGIN.save()

    messages.success(request, "User banned successfully.")

    return redirect('admin_users')


# =========================================================
# UNBAN USER
# =========================================================

def admin_unban_user(request, id):

    check = admin_check(request)

    if check:
        return check

    user = customer.objects.get(id=id)

    user.LOGIN.is_active = True
    user.LOGIN.save()

    messages.success(request, "User unbanned successfully.")

    return redirect('admin_users')


# =========================================================
# VIEW SELLERS
# =========================================================

def admin_sellers(request):

    check = admin_check(request)

    if check:
        return check

    sellers = seller.objects.all()

    return render(request, 'admin_sellers.html', {
    'sellers': sellers
})

# =========================================================
# VIEW SELLER DETAILS
# =========================================================

def admin_seller_view(request, id):

    check = admin_check(request)

    if check:
        return check

    seller_obj = seller.objects.get(id=id)

    return render(
        request,
        'admin_seller_view.html',
        {
            'seller': seller_obj
        }
    )


# =========================================================
# VERIFY SELLER
# =========================================================

def admin_verify_seller(request, id):

    check = admin_check(request)

    if check:
        return check

    seller_obj = seller.objects.get(id=id)

    seller_obj.LOGIN.is_active = True
    seller_obj.LOGIN.save()

    messages.success(request, "Seller verified successfully.")

    return redirect('admin_sellers')


# =========================================================
# REJECT SELLER
# =========================================================

def admin_reject_seller(request, id):

    check = admin_check(request)

    if check:
        return check

    seller_obj = seller.objects.get(id=id)

    seller_obj.LOGIN.is_active = False
    seller_obj.LOGIN.save()

    messages.success(request, "Seller rejected.")

    return redirect('admin_sellers')


# =========================================================
# BAN SELLER
# =========================================================

def admin_ban_seller(request, id):

    check = admin_check(request)

    if check:
        return check

    seller_obj = seller.objects.get(id=id)

    seller_obj.LOGIN.is_active = False
    seller_obj.LOGIN.save()

    messages.success(request, "Seller banned successfully.")

    return redirect('admin_sellers')


# =========================================================
# UNBAN SELLER
# =========================================================

def admin_unban_seller(request, id):

    check = admin_check(request)

    if check:
        return check

    seller_obj = seller.objects.get(id=id)

    seller_obj.LOGIN.is_active = True
    seller_obj.LOGIN.save()

    messages.success(request, "Seller unbanned successfully.")

    return redirect('admin_sellers')


# =========================================================
# ADMIN LOGOUT
# =========================================================

def admin_logout(request):

    logout(request)

    return redirect('/myapp/login/')

def signup(request):
    return render(request,'signup.html')

def logout_function(request):
    logout(request)
    return redirect('/myapp/login/')

def signupost(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    password=request.POST['password']
    image=request.FILES['image']


    a=User.objects.create_user(username=email,password=password)
    a.groups.add(Group.objects.get(name='user'))


    
    ob=customer()
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.image=image
    ob.LOGIN=a
    ob.save()
    return redirect('/myapp/login/')

def useremailcheck(request):
    email=request.GET.get('email')
    if customer.objects.filter(email=email).exists():
        return JsonResponse({'status':'yes'})
    else:
        return JsonResponse({'status':'no'})

def seller_signup(request):
    return render(request,'seller_signup.html')

    
def seller_signup_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    password=request.POST['password']

    if User.objects.filter(username=email).exists():
        messages.warning(request,'Username Already Exists')
        return redirect('/myapp/seller_signup/')

    a=User.objects.create_user(username=email,password=password)
    a.groups.add(Group.objects.get(name='seller'))

    ob=seller()
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.LOGIN=a
    ob.save()
    return redirect('/myapp/login/')

# --------------------------------login---------------------------------------


def login_load(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ADMIN
            if user.is_staff:
                return redirect('admin_dashboard')

            # SELLER
            elif seller.objects.filter(LOGIN=user).exists():
                return redirect('seller_home')

            # CUSTOMER
            elif customer.objects.filter(LOGIN=user).exists():
                return redirect('user_home')

            else:
                logout(request)

                messages.error(
                    request,
                    "User role not found."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, 'login_page.html')


@login_required(login_url='/myapp/login/')
def home(request):
    return render(request,'Index.html')

@login_required(login_url='/myapp/view_profile/')
def view_profile(request):
    ob=customer.objects.get(LOGIN=request.user)
    return render(request,'profile.html',{'data':ob})

@login_required(login_url='/myapp/view_seller_profile/')
def view_seller_profile(request):
    ob=seller.objects.get(LOGIN_id=request.user)
    return render(request,'seller_profile.html',{"data":ob})

@login_required(login_url='/myapp/seller_edit_profile/')
def seller_edit_profile(request,id):
    ob=seller.objects.get(LOGIN__id=request.user.id)
    return render(request,'seller_edit_profile.html',{"data":ob})

@login_required(login_url='/myapp/seller_edit_profile')
def seller_edit_profile_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    
    ob=seller.objects.get(LOGIN=request.user)
    obj=ob.LOGIN
    obj.username=email
    obj.save()
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.save()
    return redirect('/myapp/view_seller_profile')

@login_required(login_url='/myapp/edit_profile/')
def edit_profile(request,id):
    ob=customer.objects.get(LOGIN_id=request.user.id)
    return render(request,'edit_profile.html',{"data":ob})


def edit_profile_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    
    ob=customer.objects.get(LOGIN=request.user)
    obj=ob.LOGIN
    obj.username=email
    obj.save()
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
   


    if 'image' in request.FILES:
        ob.image = request.FILES['image']


    ob.save()
    return redirect('/myapp/home/')

# -----------------------------------------change password-----------------------------------------
@login_required(login_url='/myapp/change_password/')
def change_password(request):
    return render(request,'change_password.html')

def change_password_post(request):
    current_password=request.POST['currentpass']
    new_password=request.POST['newpass']
    confirm_password=request.POST['confirmpass']
    a=request.user
    if a.check_password(current_password):
        if new_password==confirm_password:
            a.set_password(new_password)
            a.save()
            logout(request)
            return redirect('/myapp/login/')
        else:
            messages.success(request, "not match")
            return redirect('/myapp/change_password/')
    else:
        
        messages.error(request, "Invalid Current password.")
        return redirect('/myapp/change_password/')

# -------------------------------products----------------------------
@login_required(login_url='/myapp/login/')
def seller_home(request):
    return render(request,'seller_home.html')

@login_required(login_url='/myapp/login/')
def add_products(request):
    return render(request,'add_products.html')


def add_product_post(request):
    ProductName=request.POST['productname']
    ProductPrice=request.POST['productprice']
    ProductImage=request.FILES['productimage']
    ProductQuantity=request.POST['productquantity']
    ProductDescription=request.POST['productdescription']
    ProductStock=request.POST['productstock']


    ob=products()
    ob.ProductName=ProductName
    ob.SELLER=seller.objects.get(LOGIN__id=request.user.id)
    ob.ProductPrice=ProductPrice
    ob.ProductImage=ProductImage
    ob.ProductQuantity=ProductQuantity
    ob.ProductDescription=ProductDescription
    ob.ProductStock=ProductStock
    ob.save()


    return redirect('/myapp/seller_home')

@login_required(login_url='/myapp/login/')
def view_products(request):
    ob=products.objects.filter(SELLER__LOGIN__id=request.user.id)
    for i in ob:
        obb=offer.objects.filter(PRODUCT__id=i.id).order_by("-id")
        i.status="0"
        if len(obb)>0:
            i.status="1"
            i.offer=obb[0].offer
            i.off=obb[0].off
    return render(request,'view_products_seller.html',{"data":ob})

@login_required(login_url='/myapp/login/')
def edit_product(request,id):
    ob=products.objects.get(id=id)
    # request.session['pid']=id
    return render(request,'edit_products.html',{"data":ob})

def edit_product_post(request):
    ProductName=request.POST['productname']
    ProductPrice=request.POST['productprice']
    ProductQuantity=request.POST['productquantity']
    ProductDescription=request.POST['productdescription']
    ProductStock=request.POST['productstock']
    id=request.POST['id']


    ob=products.objects.get(id=id)

    ob.ProductName=ProductName
    ob.ProductPrice=ProductPrice

    if 'ProductImage' in request.FILES:
            ProductImage=request.FILES['productimage']
            ob.ProductImage=ProductImage
            
    ob.ProductQuantity=ProductQuantity
    ob.ProductDescription=ProductDescription
    ob.ProductStock=ProductStock
    ob.save()

    return redirect('/myapp/view_products/')

@login_required(login_url='/myapp/login/')
def delete_product(request,id):
    ob=products.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/view_products/')

@login_required(login_url='/myapp/login/')
def view_user_products(request):
    ob=products.objects.all()
    for i in ob:
        obb=offer.objects.filter(PRODUCT__id=i.id).order_by("-id")
        i.status="0"
        if len(obb)>0:
            i.status="1"
            i.offer=obb[0].offer
            i.off=obb[0].off   
        obf = Feedback.objects.filter(PRODUCT__id=i.id,USER=request.user)

        i.fs="0"
        if len(obf)>0:
            i.fs=obf[0]

        avg=Feedback.objects.filter(PRODUCT=i).aggregate(Avg('review'))
        count=Feedback.objects.filter(PRODUCT=i).aggregate(Count('review'))
        if avg['review__avg']:
            i.avg_rating =avg['review__avg']
            i.count=count['review__count']
        else:
            i.avg_rating = 0
            i.count=""
        
    return render(request,'view_products.html',{"products":ob})

# --------------------------------------------place order--------------------------------------


@login_required(login_url='/myapp/login/')
def addtocartget(request,id):
     obj=products.objects.get(id=id)
     off=offer.objects.get(PRODUCT_id=id).offer
     return render(request,'add_to_cart.html',{'data':obj,"off":off})
     
@login_required(login_url='/myapp/login/')
def purchase(request,id):
    request.session['pid']=id
    ob=products.objects.get(id=id)
    offerprice=offer.objects.get(PRODUCT_id=id).offer
    print(offerprice)
    return render(request,'purchase.html',{'product':ob,'offerprice':offerprice})

def AddtoCart_post(request):
    quantity=request.POST['quantity']
    id=request.POST['pid']
    off=int(request.POST['off'])
    
    obj=cart()
    obj.quantity=quantity
    obj.PRODUCT=products.objects.get(id=id)
    obj.USER=request.user
    obj.date=datetime.now().date()
    obj.price=int(quantity)*off
    obj.save()
    return redirect('/myapp/view_cart/')

@login_required(login_url='/myapp/login/')
def view_cart(request):
    ob=cart.objects.filter(USER=request.user)
    off=offer.objects.all()

    l=ob.count()
    yes=''
    if l>1:
         return render (request,'view_cart.html',{'cart':ob,'off':off,'yes':yes})
    else:
        return render (request,'view_cart.html',{'cart':ob,'off':off})

def remove_cart(request,id):
    cart.objects.get(id=id).delete()
    return redirect("/myapp/view_cart/")


def total_buy(request):
    obj=cart.objects.filter(USER=request.user)
    for i in obj:
        ob=order()
        ob.USER=customer.objects.get(LOGIN=request.user)
        ob.orderDate=datetime.now()
        ob.amount=i.price
        ob.status='paid'
        ob.save()
        obf=orderDetails()
        obf.ORDER=ob
        obf.PRODUCT=i.PRODUCT
        obf.quantity=i.quantity
        obf.save()
        cart.objects.get(id=i.id).delete()
    return redirect('/myapp/view_OrderDetails/')





def buyproduct(request,id,pid,amount,quantity):
    from datetime import datetime
    
    totalamount=amount*quantity
    print(totalamount,type(totalamount))
    obj=order()
    obj.USER=customer.objects.get(LOGIN_id=request.user.id)
    obj.orderDate=datetime.now()
    obj.amount=totalamount
    obj.status='paid'
    obj.save()
    abj=orderDetails()
    abj.ORDER=order.objects.get(id=obj.id)
    abj.PRODUCT=products.objects.get(id=pid)
    abj.date=datetime.now()
    abj.quantity=quantity
    abj.save()
    mycart=cart.objects.get(id=id)
    mycart.delete()
    return redirect('/myapp/view_cart/')

# User.objects.get(username='seller@gmail.com').delete()

# def buy_product_user(request,pid,amount,quantity):
#     from datetime import datetime
#     totalamount=amount*quantity
#     obj=order()
#     obj.USER=request.user
#     obj.orderDate=datetime.now()
#     obj.amount=totalamount
#     obj.status='paid'
#     obj.save()

#     abj=orderDetails()
#     abj.ORDER=order.objects.get(id=obj.id)
#     abj.PRODUCT=products.objects.get(id=pid)
#     abj.date=datetime.now()
#     abj.quantity=quantity
#     abj.save()
#     return redirect('/myapp/view_OrderDetails/')

def buy_product_user(request, pid, amount, quantity):
    from datetime import datetime

    totalamount = int(amount) * int(quantity)

    obj = order()
    obj.USER = request.user
    obj.orderDate = datetime.now()
    obj.amount = totalamount
    obj.status = 'paid'
    obj.save()

    abj = orderDetails()
    abj.ORDER = obj   
    abj.PRODUCT = products.objects.get(id=pid)
    abj.quantity = quantity
    abj.save()
    Stock=Stock-quantity
    obb=products.objects.get(id=id)
    obb.ProductStock=Stock
    obb.save()

    return redirect('/myapp/view_OrderDetails/')

@login_required(login_url='/myapp/login/')
def view_OrderDetails(request):
    ob=orderDetails.objects.filter(ORDER__USER__LOGIN=request.user)
    for i in ob:
        obf = Feedback.objects.filter(PRODUCT__id=i.PRODUCT.id,USER=request.user)
        i.fs="0"
        if len(obf)>0:
            i.fs=obf[0]
        
        
        avg=Feedback.objects.filter(PRODUCT=i.PRODUCT).aggregate(Avg('review'))
        count=Feedback.objects.filter(PRODUCT=i.PRODUCT).aggregate(Count('review'))
        if avg['review__avg']:
            i.avg_rating =avg['review__avg']
            i.count=count['review__count']
        else:
            i.avg_rating = 0
            i.count=""
    print(ob)
    of=offer.objects.all()
    return render(request,'view_order.html',{'details':ob,'of':of})

def view_seller_order_details(request):
    ob=orderDetails.objects.filter(PRODUCT__SELLER__LOGIN=request.user)
    return render(request,'view_seller_orderdetails.html',{'data':ob})

def direct_buy(request, id):
    pid = request.session['pid']

    qty = int(request.POST['quantity'])
    offerprice = float(request.POST['offerprice'])

    product = products.objects.get(id=pid)
    stock = int(product.ProductStock)

    totalamount = offerprice * qty

    if stock >= qty:

        ob = order()
        ob.USER = customer.objects.get(LOGIN_id=request.user.id)
        ob.orderDate = datetime.now()
        ob.amount = totalamount
        ob.status = 'paid'
        ob.save()

        obj = orderDetails()
        obj.ORDER = ob
        obj.PRODUCT = product
        obj.quantity = qty
        obj.save()

        product.ProductStock = stock - qty
        product.save()

        return redirect('/myapp/view_OrderDetails/')

    else:
        return HttpResponse('<h1>Product Out Of Stock</h1>')
    
@login_required(login_url='/myapp/login/')
def add_feedback(request,id):
    a=orderDetails.objects.get(id=id)
    return render(request,'feedback.html',{'data':a})

def add_feedback_post(request):
    feedback=request.POST['feedback']
    pid=request.POST['pid']
    review=request.POST['star']
    print(feedback)
    blob=TextBlob(feedback)
    result=blob.sentiment.polarity
    print(result)
    if not review:
        return HttpResponse("Please select a rating")
    ob=Feedback()
    ob.feedback=feedback
    ob.USER=request.user
    ob.review=int(review)
    ob.PRODUCT=products.objects.get(id=pid)
    if result>0:
        print('helloooooooooooooooooo')
        ob.type='positive'
    elif result<0:
        ob.type='negative'
    else:
        ob.type='normal'
    ob.save()
    return redirect('/myapp/view_OrderDetails/')

@login_required(login_url='/myapp/login/')
def add_feedback_product(request,id):
    a=products.objects.get(id=id)
    return render(request,'product_feedback.html',{'data':a})


def add_feedback_product_post(request):
    feedback=request.POST['feedback']
    pid=request.POST['pid']
    review=request.POST['star']
    blob=TextBlob(feedback)
    result=blob.sentiment.polarity
    if not review:
        return HttpResponse("Please select a rating")
    ob=Feedback()
    ob.feedback=feedback
    ob.USER=request.user
    ob.review=int(review)
    ob.PRODUCT=products.objects.get(id=pid)
    if result>0:
        print('helloooooooooooooooooo')
        ob.type='positive'
    elif result<0:
        ob.type='negative'
    else:
        ob.type='normal'
    ob.save()
    return redirect('/myapp/view_user_products/')



@login_required(login_url='/myapp/login/')
def Return_Order(request,id):
    ob=orderDetails.objects.get(id=id)
    return render(request,'return.html',{'orders':ob})

def Return_Order_post(request):
    oid=request.POST['oid']
    reason=request.POST['reason']
    od_ob=orderDetails.objects.get(id=oid)
    ob=ReturnOrder()
    ob.ORDER_DETAILS=od_ob
    ob.reason=reason
    ob.status='paid'
    ob.save()
    obb = orderDetails.objects.get(id=oid)
    obb.ORDER.status = 'return initiated'
    obb.ORDER.save()
    
    return redirect('/myapp/view_OrderDetails/')

@login_required(login_url='/myapp/login/')
def seller_return(request):
    ob=ReturnOrder.objects.filter(ORDER_DETAILS__PRODUCT__SELLER__LOGIN_id=request.user.id)
    return render(request,'view_return_seller.html',{'returns':ob})

@login_required(login_url='/myapp/login/')
def view_return(request):
    ob=ReturnOrder.objects.filter(ORDER_DETAILS__ORDER__USER__LOGIN_id=request.user.id)
    return render(request,'view_return_details.html',{'return':ob})


def delete_return(request,id):
    ob=ReturnOrder.objects.get(id=id).delete()
    return redirect("/myapp/seller_return/")

def delete_all_return(request):
    ob=orderDetails.objects.all().delete()
    return redirect("/myapp/view_OrderDetails/")

def accept(request, id):
    
    ob = ReturnOrder.objects.get(id=id)
    if ob.status=='paid':
        ob.status = 'accepted'
        ob.save()

    ob.ORDER_DETAILS.ORDER.status = 'return accepted'
    ob.ORDER_DETAILS.ORDER.save()

    return redirect('/myapp/seller_return/')

def reject(request, id):
    ob = ReturnOrder.objects.get(id=id)
    if ob.status=='paid':
        ob.status = 'rejected'
        ob.save()

    ob.ORDER_DETAILS.ORDER.status = 'return rejected'
    ob.ORDER_DETAILS.ORDER.save()

    return redirect('/myapp/seller_return/')


    
# =========================================used products==============================================
@login_required(login_url='/myapp/login/')
def view_used_products(request):
    return render(request,'usedproduct.html')

@login_required(login_url='/myapp/login/')
def manage_myproduct(request):
    return render(request,'manage_myproduct.html')

@login_required(login_url='/myapp/login/')
def view_myproducts(request):
    ob=used_product.objects.filter(USER__LOGIN_id=request.user.id)
    return render(request,'view_myproducts.html',{"usedproduct":ob})

@login_required(login_url='/myapp/login/')
def add_myproducts(request):
    return render(request,'add_myproducts.html')
def add_myproducts_post(request):
    product_name=request.POST['product_name']
    product_image=request.FILES['product_image']
    product_price=request.POST['product_price']
    product_description=request.POST['product_description']

    ob=used_product()
    ob.USER=customer.objects.get(LOGIN=request.user)
    ob.product_name=product_name
    ob.product_image=product_image
    ob.product_price=product_price
    ob.product_description=product_description
    ob.save()
    return redirect('/myapp/manage_myproduct/')

def delete_myproduct(request,id):
    ob=used_product.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/manage_myproduct')

@login_required(login_url='/myapp/login/')
def view_others_products(request):
    ob=used_product.objects.all().exclude(USER__LOGIN=request.user)
    print(ob)
    return render(request,'view_others_products.html',{"usedproduct":ob})

def send_request(request,id):
    if UsedProductRequest.objects.filter(UsedProduct_id=id , USER__LOGIN=request.user):
        messages.success(request, "Request Already sented!")
    else:
        ob=UsedProductRequest()
        ob.USER=customer.objects.get(LOGIN=request.user)
        
        ob.DateTime=datetime.now()
        ob.UsedProduct=used_product.objects.get(id=id)
        ob.status='requested'
        ob.save()
        messages.success(request, "Request sent successfully!")
        return redirect('/myapp/view_others_products/')
    return redirect('/myapp/view_others_products/')

@login_required(login_url='/myapp/login/')
def view_request(request):
    ob=UsedProductRequest.objects.filter(USER__LOGIN=request.user)
    return render(request,'request.html',{'data':ob})

def accept_request(request,id):
    ob=UsedProductRequest.objects.get(id=id)
    if ob.status=='requested':
        ob.status='Request Accepted'
        ob.save()
    return redirect('/myapp/view_request/')
def reject_request(request,id):
    ob=UsedProductRequest.objects.get(id=id)
    if ob.status=='requested':
        ob.status='Request Rejcted'
        ob.save()
    return redirect('/myapp/view_request/')

@login_required(login_url='/myapp/login/')
def view_used_purchase_status(request):
    ob=UsedProductRequest.objects.filter(USER__LOGIN=request.user)
    return render(request,'view_used_purchase.html',{'data':ob})



def view_contacts(request):
    return render(request,'contacts.html')

# =================================OFFERS=======================
def add_offers(request,id):
    ob=products.objects.get(id=id)
    return render(request,'Addoffer.html',{'data':ob})

def add_offers_post(request):
    id=request.POST['id']
    offerprice=int(request.POST['offer'])
    a=products.objects.get(id=id)
    p_price=a.ProductPrice
    discount=(p_price*offerprice)/100
    o_price=p_price-discount

    ob=offer()
    ob.PRODUCT=products.objects.get(id=id)
    ob.offer=o_price
    ob.off=offerprice
    ob.save()
    return redirect('/myapp/view_products/')

def change_offers(request, id):
    ob=offer.objects.get(PRODUCT__id=id)
    return render(request, 'changeoffer.html', {'offerss': ob})


def change_offer_post(request):
    id = request.POST['id']
    offerprice = int(request.POST['offer'])

    product = products.objects.get(id=id)

    p_price = product.ProductPrice
    discount = (p_price * offerprice) // 100
    o_price = p_price - discount

    ob = offer.objects.get(PRODUCT=product)
    ob.offer = o_price
    ob.off = offerprice
    ob.save()

    return redirect('/myapp/view_products/')



























