from django.urls import path
from ecomm_app import views
from django.conf.urls.static import static
from ecomm import settings
urlpatterns = [
    path('',views.home),
    path('allcategory',views.all_category),
    path('pdetails/<pid>',views.product_detail),
    # path('tpdetails/<pid>',views.top_product_detail),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('brand/<data>',views.brand),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('removeorder/<cid>',views.removeorder),
    path('updateqtyorder/<qv>/<cid>',views.updateqtyorder),
    path('makepayment',views.makepayment),
    # path('successfullyplaced',views.successfully_placed),
    path('sendmail/<uemail>',views.sendusermail),
    path('contact',views.contact),
    path('about',views.about),
    # path('addtocartoutside/<pid>',views.addtocartoutside)
]

# only when DBUG = true in setting.py
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

