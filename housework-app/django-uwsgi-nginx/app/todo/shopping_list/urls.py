from django.urls import path
from todo.shopping_list import views

urlpatterns = [
    path('shopping_list/', views.ShowShoppingItemView.as_view(), name='show_shopping_item'),
    path('get_shopping_item/', views.get_shopping_item, name='get_shopping_item'),
    path('post_update_shopping_item/', views.post_update_shopping_item, name='post_update_shopping_item'),
    path('post_delete_shopping_item/', views.post_delete_shopping_item, name='post_delete_shopping_item'),
    path('shop_and_shopping_item_picture_setting/', views.show_shop_and_shopping_item_picture_setting,
         name='show_shop_and_shopping_item_picture_setting'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('create_shopping_item_picture/', views.create_shopping_item_picture, name='create_shopping_item_picture'),
    path('delete_shop/<shop_id>', views.delete_shop, name='delete_shop'),
    path('delete_shopping_item_picture/<pic_id>', views.delete_shopping_item_picture,
         name='delete_shopping_item_picture'),
]
