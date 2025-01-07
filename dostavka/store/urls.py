from tkinter.font import names

from rest_framework import routers
from .views import *
from django.urls import path, include


router=routers.SimpleRouter()
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'courier', CourierViewSet, basename='courier')
router.register(r'courier_review', CourierReviewViewSet, basename='courier_review')


urlpatterns = [
    path('', include(router.urls)),
    path('store/', StoreListAPIView.as_view(), name='store_list' ),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail' ),
    path('store/create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('store/create/<int:pk>/', StoreEDITAPIView.as_view(), name='store_edit'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('product/', ProductListAPIView.as_view(), name='product'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/create/<int:pk>/', ProductEDITAPIView.as_view(), name='product_edit'),
    path('combo/', ComboListAPIView.as_view(), name='combo'),
    path('combo/<int:pk>', ComboDetailAPIView.as_view(), name='combo_detail'),
    path('combo/create/', ComboCreateAPIView.as_view(), name='combo_create'),
    path('combo/create/<int:pk>', ComboEDITAPIView.as_view(), name='combo_edit'),
    path('save/', SaveListAPIView.as_view(), name='save'),
    path('save/<int:pk>/', SavePostAPIView.as_view(),  name='save_post'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('order/', OrderListAPIView.as_view(), name='order_list'),
    path(r'order/<int:pk>/', OrderEDITAPIView.as_view(), name='order_edit'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order_create'),
    path('order/courier/', OrderCourierAPIView.as_view(), name='order_courier'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
