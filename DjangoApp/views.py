import random
from datetime import timezone, timedelta, datetime

from django.contrib.auth import login, authenticate 
from django.contrib.auth.hashers import make_password
import random

from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
        print(request)
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
            expiration_time = datetime.now() + timedelta(hours=1)
            refresh.set_exp(expiration_time)
            user_info = {
                'id': user.id,
                'email': user.email,
                'name': user.fullname,
                'address':user.address,
                'zip':user.zip,
                'phone':user.phone,
                'city':user.city,
                'role':user.role,
                'expiration_token':expiration_time
            }
            return Response({'access_token': access_token, 'user': user_info}, status=status.HTTP_200_OK)
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
    if request.method == 'POST':
        print("Authorization Header:", request.headers.get('Authorization'))
        id_user = request.user.id
        mutable_data = request.data.copy()
        mutable_data['id_user'] = id_user  # Ajouter l'ID de l'utilisateur aux données de la requête
        serializer = AdviceSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            advices = Advice.objects.all()
            advices_data = AdviceSerializer(advices, many=True).data
            return Response({'advices_data': advices_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UpdateAdvice(request, pk):
    if request.method=='PUT':
        try:
            prev_advice=Advice.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        id_user=request.user.id
        mutable_data=request.data.copy()
        mutable_data['id_user']=id_user
        serializer=AdviceSerializer(prev_advice,data=mutable_data)
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

##### Amelioration du selectionnement aléatoires a faire #####


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def care_create_with_assignment(request):
    if request.method == 'POST':
        print(request.data)
        serializer = CareSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            print('coucou')
            # Récupérer l'owner depuis l'utilisateur authentifié
            owner = request.user

            # Sélectionner aléatoirement un botaniste et un keeper
            botanistes = CustomUser.objects.filter(role='botanist').exclude(id=owner.id)
            keepers = CustomUser.objects.filter(role='owner').exclude(id=owner.id)
            print('on est la')
            if not botanistes.exists() or not keepers.exists():
                return Response({"error": "Pas assez d'utilisateurs pour attribuer les rôles"}, status=status.HTTP_400_BAD_REQUEST)

            botaniste = random.choice(botanistes)
            keeper = random.choice(keepers)
            print(botaniste)
            print('hello world!')

            # Créer l'objet Care avec les utilisateurs attribués
            care = Care.objects.create(
                owner=owner,
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                started_at=serializer.validated_data.get('started_at'),
                ended_at=serializer.validated_data.get('ended_at'),
                active=serializer.validated_data['active'],
                keeper=keeper,
                botaniste=botaniste
            )

            # Sérialiser l'objet créé pour la réponse
            response_serializer = CareSerializer(care)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
def CreateCommentPost(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(post=post)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

#######################
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListCareOwner(request):
    user_id=request.user.id
    try:
        cares=Care.objects.filter(owner=user_id,active=1)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        cares_data=CareSerializer(cares,many=True).data
        return Response({'cares':cares_data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListCareKeeper(request):
    user_id=request.user.id
    try:
        cares=Care.objects.filter(keeper=user_id,active=1)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        cares_data=CareSerializer(cares,many=True).data
        return Response({'cares':cares_data},status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ListCareToKeep(request):
    user_id = request.user.id
    try:
        # Utilisation de exclude pour exclure les gardes de l'utilisateur connecté
        cares = Care.objects.exclude(owner=user_id).filter(active=0)
    except Care.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cares_data = CareSerializer(cares, many=True).data
        return Response({'cares': cares_data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UpdateCare(request, pk):
    user_id = request.user.id
    try:
        care = Care.objects.get(pk=pk)
    except Care.DoesNotExist:
        return Response({'detail': 'Care not found'}, status=status.HTTP_404_NOT_FOUND)

    # Vérifie si l'utilisateur est le propriétaire de la garde
    if care.owner_id == user_id:
        return Response({'detail': 'You do not have permission to update this care'}, status=status.HTTP_403_FORBIDDEN)

    # Vérifie si la garde n'est pas déjà active
    if care.active:
        return Response({'detail': 'Care is already active'}, status=status.HTTP_400_BAD_REQUEST)

    # Sélectionne un botaniste aléatoire parmi ceux disponibles
    available_botanists = CustomUser.objects.filter(role='botanist').exclude(id=user_id)
    if not available_botanists.exists():
        return Response({'detail': 'No botanists available to assign'}, status=status.HTTP_400_BAD_REQUEST)

    random_botanist = random.choice(available_botanists)

    # Met à jour la garde
    care.active = True
    care.keeper_id = user_id
    care.botaniste_id = random_botanist.id
    care.save()

    serializer = CareSerializer(care)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_care(request):
    user = request.user

    # Vérifie si l'utilisateur est propriétaire
    if user.role != 'owner':
        return Response({'detail': 'You do not have permission to create a care'}, status=status.HTTP_403_FORBIDDEN)

    # Création de la garde
    serializer = CareSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request, care_id):
    user = request.user

    # Vérifie si l'utilisateur est le keeper de la garde
    try:
        care = Care.objects.get(id=care_id)
        if care.keeper != user:
            return Response({'detail': 'You do not have permission to create a post for this care'}, status=status.HTTP_403_FORBIDDEN)
    except Care.DoesNotExist:
        return Response({'detail': 'Care not found'}, status=status.HTTP_404_NOT_FOUND)

    # Création du post
    serializer = PostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(id_care=care)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

