from django.urls import path

from . import views

urlpatterns=[
    path('addcart/<int:id>',views.AddCartView.as_view(),name='addcart'),
    path('cartview/', views.CartView.as_view(), name='cart_view'),
    path('cartremove/<int:id>', views.RemoveFromCartView.as_view(), name='cartremove'),
    path('cartdelete/<int:product_id>',views.DeleteCart.as_view(),name='cartdelete'),
    path('chekout/',views.CheckOut.as_view(),name='chekout'),
    path('orderuser/',views.OrderCancelledView.as_view(),name='orderuser'),
    path('wishles/',views.WishlisView.as_view(),name='wishles'),
    path('wishles/<int:pk>/', views.WishlisView.as_view(), name='wishles_toggle'),
    path('Orderstatus/',views.OrderStatusView.as_view(),name='orderstatus')
]