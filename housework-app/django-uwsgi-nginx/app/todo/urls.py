from django.urls import path, include
from todo.common import views

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('shopping_list/', include('todo.shopping_list.urls')),
    path('recipe_collection/', include('todo.recipe_collection.urls')),
    path('meal_plans/', include('todo.meal_plans.urls')),
]
