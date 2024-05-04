from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, Post, Pictures, Category, Care, Advice, Comment

from .serializers import CustomUserSerializer, PostSerializer, PicturesSerializer, CategorySerializer, CareSerializer, \
    AdviceSerializer, CommentSerializer


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

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UpdateProfile(request):
    user_id=request.user.id
    try:
        user=CustomUser.objects.get(pk=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='PUT':
        serializer=CustomUserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user':request.data},status=status.HTTP_200_OK)

########## Vues des advices ########
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListAdvice(request):
    try:
        advices=Advice.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=AdviceSerializer(advices,many=True).data
        return Response({'advices':serializer},status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def CreateAdvice(request):
    if request.method=='POST':
        serializer=AdviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            advices=Advice.objects.all()
            advices_data=AdviceSerializer(advices,many=True).data
            return Response({
                'advices_data':advices_data
            }, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UpdateAdvice(request, pk):
    if request.method=='PUT':
        try:
            prev_advice=Advice.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=AdviceSerializer(prev_advice,data=request.data)
        if serializer.is_valid():
            serializer.save()
            advices=Advice.objects.all()
            advices_data=AdviceSerializer(advices,many=True).data
            return Response({
                'advices_data':advices_data
            },status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def DeleteAdvice(request, pk):
    try:
        advice=Advice.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        Advice.delete(advice)
        advices = Advice.objects.all()
        advices_data = AdviceSerializer(advices, many=True).data
        return Response({
            'advices_data': advices_data
        }, status=status.HTTP_200_OK)



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

########## Vues de l'espace des botanistes #########
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListCareBotaniste(request):
    user_id=request.user.id
    try:
        cares=Care.objects.filter(botaniste=user_id,active=1)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        cares_data=CareSerializer(cares,many=True).data
        return Response({'cares':cares_data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListPostCare(request,pk):
    try:
        posts=Post.objects.filter(id_care=pk,visibility=1)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        posts_data=PostSerializer(posts,many=True).data
        return Response({'posts':posts_data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DetailsPost(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post_data = PostSerializer(post).data
        pictures = Pictures.objects.filter(post=post)
        pictures_data = PicturesSerializer(pictures, many=True).data
        comments = Comment.objects.filter(post_id=pk)
        comments_data = CommentSerializer(comments, many=True).data
        return Response({
            'post': post_data,
            'pictures': pictures_data,
            'comments':comments_data
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def CommentsPost(request,pk):
    try:
        comments=Comment.objects.filter(post_id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        comments_data=CommentSerializer(comments,many=True).data
        return Response({'comments':comments_data},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def CreateCommentPost(request,pk):
    try:
        post=Post.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='POST':
        comment=CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save(post=post)
            return Response(status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def DeleteComment(request,pk):
    try:
        comment=Comment.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        Comment.delete(comment)
        comments=Comment.objects.all()
        comments_data=CommentSerializer(comments,many=True).data
        return Response({'comments':comments_data},status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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

