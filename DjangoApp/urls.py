"""
URL configuration for merchex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from .views import register, login_view, CareListAPIView, \
    CareDetailAPIView, CareCreateAPIView, CareUpdateAPIView, CareDestroyAPIView, CategoryListAPIView, \
    CategoryDetailAPIView, CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDestroyAPIView, PicturesListAPIView, \
    PicturesDetailAPIView, PicturesCreateAPIView, PicturesUpdateAPIView, PicturesDestroyAPIView, PostListAPIView,  \
    PostDetailAPIView, PostCreateAPIView, PostUpdateAPIView, PostDestroyAPIView, CreateAdvice, UpdateAdvice, \
    DeleteAdvice, ListAdvice, ListCareBotaniste, ListPostCare, CreateCommentPost, CommentsPost, DeleteComment, \
    DetailsPost, UpdateProfile, ListCareOwner, ListCareKeeper, ListCareToKeep, UpdateCare

urlpatterns = [
    ########## URLs des users #########
    path('user/signup', register, name='register'),
    path('user/update', UpdateProfile, name='UpdateProfile'),
    path('user/signin', login_view, name='login'),
    path('token/', token_obtain_pair, name='token_obtain_pair'),
    ########## URLs des advices #########
    path('advice', ListAdvice, name='ListAdvice'),
    path('advice/create', CreateAdvice, name='CreateAdvice'),
    path('advice/<int:pk>/update', UpdateAdvice, name='UpdateAdvice'),
    path('advice/<int:pk>/delete', DeleteAdvice, name='DeleteAdvice'),
    ########## URLs des catégories #########
    path('category', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('category/create', CategoryCreateAPIView.as_view(), name='category-create'),
    path('category/<int:pk>/update', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', CategoryDestroyAPIView.as_view(), name='category-delete'),
    ########## URLs des gardes #########
    path('care', CareListAPIView.as_view(), name='care-list'),
    #path('care/<int:pk>', CareDetailAPIView.as_view(), name='care-detail'),
    path('care/create', CareCreateAPIView.as_view(), name='care-create'),
    path('care/<int:pk>/update', CareUpdateAPIView.as_view(), name='care-update'),
    path('care/<int:pk>/delete', CareDestroyAPIView.as_view(), name='care-delete'),

    ########## URLs de l'espace botaniste ########
    path('attribution', ListCareBotaniste, name='ListCareBotaniste'),
    path('attribution/care/<int:pk>/posts', ListPostCare, name='ListPostCare'),
    path('attribution/care/<int:pk>/post', DetailsPost, name='DetailsPost'),
    path('attribution/create/care/<int:pk>/post/comment', CreateCommentPost, name='CreateCommentPost'),
    path('attribution/care/post/<int:pk>/comment', CommentsPost, name='CommentsPost'),
    path('attribution/delete/care/post/<int:pk>/comment',DeleteComment,name='DeleteComment'),


    
    ########## URLs des pictures #########
    path('picture/', PicturesListAPIView.as_view(), name='picture-list'),
    path('picture<int:pk>', PicturesDetailAPIView.as_view(), name='picture-detail'),
    path('picture/create', PicturesCreateAPIView.as_view(), name='picture-create'),
    path('picture/<int:pk>/update', PicturesUpdateAPIView.as_view(), name='picture-update'),
    path('picture/<int:pk>/delete', PicturesDestroyAPIView.as_view(), name='picture-delete'),


    ########## URLs des posts #########
    path('post/', PostListAPIView.as_view(), name='picture-list'),
    path('post/<int:pk>', PostDetailAPIView.as_view(), name='post-detail'),
    path('post/create', PostCreateAPIView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateAPIView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDestroyAPIView.as_view(), name='post-delete'),
    ######### URLS espace propriaitaire####
    path('owned-cares/', ListCareOwner, name='ListCareOwner'),
    path('kept-cares/', ListCareKeeper, name='ListCareOwner'),
    path('cares-to-keep/', ListCareToKeep, name='ListCareToKeep'),
    path('keep/', UpdateCare, name='UpdateCare'),



]

