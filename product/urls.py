
from django.urls import path
from . import views
urlpatterns=[
    path('dashboard/',views.SellerDashboardView.as_view(),name='dashboard'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product/create/',views.ProductCreateView.as_view(),name='product_create'),
    path('product/update/<int:pk>',views.ProductUpdateView.as_view(),name='product_update'),
    path('comment/reply/<int:pk>/', views.ReplyCommentView.as_view(), name='reply_comment'),
    path('Details/<int:pk>', views.ProductDetailView.as_view(), name='details'),

]