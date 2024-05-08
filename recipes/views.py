# recipes/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer

from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer
from .permissions import IsOwnerOrReadOnly


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.exceptions import PermissionDenied

class RecipesAPIView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    

    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        return super().post(request, *args, **kwargs)
        # serializer.save(owner=self.request.user)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user.pk:
            raise PermissionDenied("You do not have permission to perform this action.")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return self.destroy(request, *args, **kwargs)
    
# Working
# class RecipesAPIView(generics.CreateAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def post(self, request, *args, **kwargs):
#         permission_classes = [permissions.IsAuthenticated]
#         # Ensure the authenticated user is set as the owner
#         request.data['owner'] = request.user.pk
#         return super().post(request, *args, **kwargs)
    
    


    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    