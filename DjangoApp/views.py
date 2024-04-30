


from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, Post, Pictures, Category, Care, Advice

from .serializers import CustomUserSerializer, PostSerializer, PicturesSerializer, CategorySerializer, CareSerializer, \
    AdviceSerializer


########## Vues des user #########
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        password = request.data.get('password')
        hashed_password = make_password(password)
        request.data['password'] = hashed_password
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.CustomUser
        if user.is_active:
            refresh_token = response.data['refresh']
            access_token = response.data['access']
            custom_response_data = {
                'refresh_token': refresh_token,
                'access_token': access_token,
                'user_id': user.id,
                'user_name': user.fullname,
                'user_email': user.email,
            }
            return Response(custom_response_data)
        else:
            return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_info = {
                'id': user.id,
                'email': user.email,
                'name': user.fullname,
            }
            return Response({'access_token': access_token,'user':user_info}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)





########## Vues des gardes #########

class CareListAPIView(generics.ListAPIView):
    queryset = Care.objects.all()
    serializer_class = CareSerializer


class CareDetailAPIView(generics.RetrieveAPIView):
    queryset = Care.objects.all()
    serializer_class = CareSerializer


class CareCreateAPIView(generics.CreateAPIView):
    queryset = Care.objects.all()
    serializer_class = CareSerializer


class CareUpdateAPIView(generics.UpdateAPIView):
    queryset = Care.objects.all()
    serializer_class = CareSerializer


class CareDestroyAPIView(generics.DestroyAPIView):
    queryset = Care.objects.all()
    serializer_class = CareSerializer


########## Vues des category #########

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


########## Vues des pictures #########

class PicturesListAPIView(generics.ListAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesDetailAPIView(generics.RetrieveAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesCreateAPIView(generics.CreateAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesUpdateAPIView(generics.UpdateAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesDestroyAPIView(generics.DestroyAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


########## Vues des posts #########

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

