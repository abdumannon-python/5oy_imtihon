from django.urls import path

from . import views

urlpatterns=[
    path('addcart/<int:id>',views.AddCartView.as_view(),name='addcart'),
    path('cartview/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cartremove/<int:id>', views.RemoveFromCartView.as_view(), name='cartremove'),
    path('cartdelete/<int:product_id>',views.DeleteCart.as_view(),name='cartdelete'),
    path('chekout/',views.CheckOut.as_view(),name='chekout'),
    path('orderitem/',views.OrderItemView.as_view(),name='order_view'),
    path('orderuser/',views.OrderUserView.as_view(),name='orderuser'),
    path('wishles/',views.WishlisView.as_view(),name='wishles'),
]