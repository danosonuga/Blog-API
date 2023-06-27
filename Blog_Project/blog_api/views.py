from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog_api.serializers import PostSerializer, CategorySerializer, CommentSerializer, UserSerializer, LikeSerializer, SubCommentSerializer, UserProfileSerializer
from blog_api.models import Post, Comment, Category, Like, SubComment, UserProfile
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from blog_api.permissions import IsAuthorOrReadOnly

from django.core.mail import send_mail

#LoginJWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


#Create your views here.
@api_view(['GET'])
def api_overview(request, format=None):
    return Response({
        'signup': reverse('create-user', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'details': reverse('post-detail', args=[1], request=request, format=format),
        'comment': reverse('comment-post', args=[1], request=request, format=format),
    })

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist with this email'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_password_url = request.build_absolute_uri('change/{}/{}/'.format(uidb64, token))

        send_mail(
                'Password reset request',
                f'Hi {user.first_name} {user.last_name}\n\n We received a request to reset your password.\n\n Please click the following link to reset your password: \n\n{reset_password_url}',
                'daab53622981da',
                [email],
                fail_silently=False,
            )

        return Response("Successful! A mail has been sent to you", status=status.HTTP_200_OK)
        
class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if not new_password or not confirm_password:
                return Response("The fields must not be empty", status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response("The passwords do not match", status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response("Your password has been updated successfully", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        return response

class CreateUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')

            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            user_profile = UserProfile.objects.create(user=user)
            serializer = UserProfileSerializer(user_profile)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


# @api_view(['POST'])
# def commentToPost(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(post=post, author=request.user)
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)

class CommentsComment(generics.ListCreateAPIView):
    queryset = SubComment.objects.all()
    serializer_class = SubCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, comment=comment)

class LikePostView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]