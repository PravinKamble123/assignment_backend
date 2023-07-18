from django.urls import path 

from . import views

urlpatterns = [
    # CATEGORY
    path('create-category/', views.create_category),
    path('get-list/', views.get_category_list),
    path('get-category/<int:pk>/', views.get_category_by_id),
    path('update-category/<int:pk>/', views.update_category),
    path('delete-category/<int:pk>/', views.delete_category),

    # PRODUCT
    path('products/', views.ProductAPIView.as_view()),
    path('products/<int:pk>/', views.ProductAPIView.as_view()),
] 