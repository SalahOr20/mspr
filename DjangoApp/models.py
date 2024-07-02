from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est requis')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=45)
    email = models.CharField(max_length=80, unique=True)
    address = models.CharField(max_length=60)
    zip = models.IntegerField()
    city = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    role = models.CharField(max_length=10, choices=[
        ('owner', 'botanist'),
    ], default='owner')
    last_connexion = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname','role']

    objects = CustomUserManager()

    def __str__(self):
        return self.fullname


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'



class Advice(models.Model):
    id_advice = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    like = models.IntegerField(null=True)
    picture=models.ImageField(upload_to='uploads/', null=True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'advice'


class Care(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_cares')
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=100)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()
    keeper = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='kept_cares')
    botaniste = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='botaniste',null=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'care'





class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=100)
    visibility = models.BooleanField()
    id_care = models.ForeignKey(Care, on_delete=models.CASCADE)
    read = models.BooleanField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'post'
class Pictures(models.Model):
    id_pictures = models.AutoField(primary_key=True)
    picture = models.ImageField(upload_to='uploads/', null=True,default='none')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'pictures'
class Comment(models.Model):
    id_comment= models.AutoField(primary_key=True)
    comments=models.CharField(max_length=50)
    createdAt=models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment

