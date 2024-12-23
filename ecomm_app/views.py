from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from .models import Products, Cart, Order
from django.db.models import Q 
import random, razorpay
import pkg_resources
from django.core.mail import send_mail

def home(request):
    context={}
    p=Products.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def product_detail(request,pid):
    p=Products.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_detail.html',context)

# def top_product_detail(request,pid):
#     p=Top_Products.objects.filter(id=pid)
#     context={}
#     context['products']=p
#     return render(request,'Top_product_details.html',context)

def all_category(request):
    context={}
    p=Products.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'all_category.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        umail=request.POST['uemail']
        context={}
        if uname=='' or upass=='' or ucpass =='':
            context['errormsg']="Fields cannot be Empty"
        elif upass!=ucpass:
             context['errormsg']="Password and confirm password didn't match"
        else:
            try:
                u=User.objects.create(username=uname, email=umail, password=upass)
                u.set_password(upass)#hide password
                u.save()
                context['success']="User created Successfully, please login"
            except Exception:
                context['errormsg']="Username already Exist!!"
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
def user_login(request):
    if request.method=="POST":
       uname=request.POST['uname']
       upass=request.POST['upass']
       context={}
       if uname=='' or upass=='':
          context['errormsg']='Fields cannot be Empty'
          return render(request,'login.html',context)
       else:
          u=authenticate(username=uname, password=upass)
# authenticate : this function check username and password enterd by user with
# username and password in auth_user table and return object or row
          if u is not None:
            login(request,u)
            return redirect('/')
          else:
             context['errormsg']='Invalid username and password'  
             return render(request,'login.html',context)                 
    else:    
      return render(request,'login.html')
    

def user_logout(request):
   logout(request)
   return redirect('/')

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Products.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'all_category.html',context)

def sort(request,sv):
  if sv=='0':
    # ascending
    col='price'
  else:
    # descending
    col='-price'
  p=Products.objects.order_by(col)
  context={}
  context['products']=p
  return render(request,'all_category.html',context)

def range(request):
   min=request.GET['min']
   max=request.GET['max']
  #  print(min, max)
  # price__gte= gtreater than equal, price__gt= greater than, price__lt= less than, price__lte=less than equal
   q1=Q(price__gte=min) #greater and equal than 1000
   q2=Q(price__lte=max)  #less and equal than 2000
   q3=Q(is_active=True)
   p=Products.objects.filter(q1&q2&q3)
   context={}
   context['products']=p
   return render(request,'all_category.html',context)

def brand(request,data):
    q1=Q(brand=data)
    q2=Q(is_active=True)
    p=Products.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'all_category.html',context)

def addtocart(request,pid):
  if request.user.is_authenticated:
    userid= request.user.id 
    u=User.objects.filter(id=userid) #automatic user entry table 
    p=Products.objects.filter(id=pid) #product table
    # tp=Top_Products.objects.filter(id=pid) #top product table
    q1=Q(uid=u[0])
    q2=Q(pid=p[0])
    c=Cart.objects.filter(q1&q2)
    n=len(c)
    context={}
    #to check product already add or not
    if n == 1:
      context['msg']='Product Already exist in cart!!'
    else:
      c=Cart.objects.create(uid=u[0],pid=p[0])
      c.save()
      context['success']='Product Added Successfully to cart!'
    context['products']=p
    return render(request,'product_detail.html',context)
    # return HttpResponse('product added in cart')
  else:
    return redirect('/login')
  
def viewcart(request):
   c=Cart.objects.filter(uid=request.user.id)
   np= len(c)
   s=0
   for x in c:
      s= s + x.pid.price * x.qty
   context={}
   context['data']=c
   context['total'] =s
   context['n']=np
   return render(request,'cart.html',context)

def remove(request,cid):
   c=Cart.objects.filter(id=cid)
   c.delete() 
   return redirect('/viewcart')

def updateqty(request,qv,cid):
  c=Cart.objects.filter(id=cid)
  if qv == '1':
    #increase quantity
    t=c[0].qty + 1
    c.update(qty=t)

  else:
    #decrease quantity
    if c[0].qty > 1:
      t=c[0].qty - 1
      c.update(qty=t)
  return redirect('/viewcart')

def placeorder(request):
  #to move product from cart to place order
  userid=request.user.id
  c=Cart.objects.filter(uid=userid)
  # order id
  oid = random.randrange(1000,9999)
  for x in c:
     o=Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
     o.save()
     x.delete()
  context={}
  orders=Order.objects.filter(uid=request.user.id)
  np=len(orders)
  context['data']=orders
  context['n']=np
  s=0
  for x in orders:
    s= s + x.pid.price * x.qty
  context['total'] =s

  return render(request,'placeorder.html',context)

def removeorder(request,cid):
   c=Order.objects.filter(id=cid)
   c.delete() 
   return redirect('/placeorder')

def updateqtyorder(request,qv,cid):
  c=Order.objects.filter(id=cid)
  if qv == '1':
    #increase quantity
    t=c[0].qty + 1
    c.update(qty=t)

  else:
    #decrease quantity
    if c[0].qty > 1:
      t=c[0].qty - 1
      c.update(qty=t)
  return redirect('/placeorder')

def makepayment(request):
  orders=Order.objects.filter(uid=request.user.id)
  s=0
  for x in orders:
    s= s+ x.pid.price * x.qty
    oid=x.order_id
  client = razorpay.Client(auth=("rzp_test_cWto9CcftWaLO9", "VuuszHCxUIQkFpil0mgGp6h2"))

  data = { "amount": s * 100, "currency": "INR", "receipt": oid }
  payment = client.order.create(data=data)
  context ={}
  context['data']=payment

  uemail=request.user.email
  # print(uemail)
  context['uemail']=uemail
  return render(request,'pay.html',context)

  

# def successfully_placed(request):
  

#order place mail sen to customer 
def sendusermail(request,uemail):
  msg="Order detail are:---"
  send_mail(
    "Your order placed successfully",
    msg,
    "patilnikita062@gmail.com"  ,# from owner mail
    [uemail], # to customer mail
    fail_silently=False,
  )
  orders=Order.objects.filter(uid=request.user.id)
  for x in orders:
     x.delete()
  
  return render(request,'successfully_placed.html')
  # return HttpResponse('mail sent successfully')

def contact(request):
  return render(request,'contact.html')

def about(request):
  return render(request,'about.html')


# def addtocartoutside(request,pid):
#   if request.user.is_authenticated:
#     userid= request.user.id 
#     u=User.objects.filter(id=userid) #automatic user entry table 
#     p=Top_Products.objects.filter(id=pid) #product table
#     # tp=Top_Products.objects.filter(id=pid) #top product table
#     q1=Q(uid=u[0])
#     q2=Q(pid=p[0])
#     c=Cart.objects.filter(q1&q2)
#     n=len(c)
#     context={}
#     #to check product already add or not
#     if n == 1:
#       context['msg']='Product Already exist in cart!!'
#     else:
#       c=Cart.objects.create(uid=u[0],pid=p[0])
#       c.save()
#       context['success']='Product Added Successfully to cart!'
#     context['products']=p
#     return render(request,'Top_product_details.html',context)
#     # return HttpResponse('product added in cart')
#   else:
#     return redirect('/login')