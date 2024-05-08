# recipes/urls.py

from django.urls import path
from .views import RegistrationAPIView, LoginAPIView,RecipesAPIView, CreateRecipeAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    
    path('recipes/', RecipesAPIView.as_view(), name='recipe-list-create'), # public
    # path('myrecipes/', MyRecipesAPIView.as_view(), name='recipe-detail'), #require auth
    path('create/', CreateRecipeAPIView.as_view(), name='create recipe')
]
