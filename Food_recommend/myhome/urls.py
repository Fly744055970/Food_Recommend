from django.contrib import admin
from django.urls import path
from myhome import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('foodlist/', views.foodlist, name='foodlist'),
    path('user_view/', views.user_view, name='user_view'),
    path('change_password/', views.change_password_view, name='change_password_view'),
    path('detail/<int:foodid>', views.detail, name='myhome_fooddetail'),
    path('comment/<int:foodid>', views.comment, name='myhome_comment'),

    path('add_wishlist/<int:foodid>/', views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist/<int:foodid>/', views.remove_wishlist, name='remove_wishlist'),

    path('food_rec/', views.food_rec, name='food_rec'),

    path('keshihua/', views.keshihua, name='keshihua'),
    path('wordcloud/', views.wordcloud_page, name='wordcloud_page'),
    path('get_wordcloud_data/', views.wordcloud_view, name='get_wordcloud_data'),

    path('logout/', views.logout, name='logout')
]
