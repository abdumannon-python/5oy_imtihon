
from django.urls import path
from . import views
urlpatterns=[
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product/create/',views.ProductCreateView.as_view(),name='product_create'),
    path('product/update/<int:pk>/',views.ProductUpdateView.as_view(),name='product_update'),
    path('details/<int:pk>/', views.ProductDetailView.as_view(), name='details'),
]