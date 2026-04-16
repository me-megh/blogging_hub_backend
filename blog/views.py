from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from django.contrib.auth.models import User
from .forms import BlogPostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_protect 
from .serializers import UserSerializer 
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
import logging
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from rest_framework.decorators import api_view


def Blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'posts': posts})

class BlogPostList(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this

    def get(self, request, format=None):
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

def csrf_token_view(request):
    csrf_token = get_token(request)
    response = JsonResponse({'csrf_token': csrf_token})
    response.set_cookie(
    'csrftoken', csrf_token,          # Set the CSRF token value
    samesite='None',                  # Ensure this is a string, NOT a tuple
    secure=True )                      # If using HTTPS, set this to True

    return response
def view_blog(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'view_blog.html', {'post': blog_post})

@login_required
def profile(request):
    user_posts = BlogPost.objects.filter(author=request.user).exclude(pk__isnull=True)
    return render(request, 'profile.html', {'user_posts': user_posts})

# def logout_view(request):
#     logout(request)
#     return JsonResponse({"message": "Successfully logged out"})

def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'home.html', {'posts': posts})

class CreateBlogView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the 'author' name from the request
        author_name = request.data.get('author', None)
        
        if author_name:
            try:
                # Look up the user by their name
                author = User.objects.get(username=author_name)
            except User.DoesNotExist:
                return Response({"error": "User with this name does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Author name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add author to the request data
        data = request.data.copy()
        data['author'] = author.id  # You still need the user ID to associate with ForeignKey
        
        # Serialize and save the blog post
        serializer = BlogPostSerializer(data=data)
        if serializer.is_valid():
            blog_post = serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def test_delete_blog(request, pk):
    return Response({"message": f"Successfully matched delete request for post {pk}"}, status=200)

@api_view(['DELETE'])
@csrf_protect
def delete_blog(request, pk):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    blog_post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if the user is the author of the post
    if blog_post.author != request.user:
        return Response({"error": "You can only delete your own posts."}, status=status.HTTP_403_FORBIDDEN)
    
    blog_post.delete()
    return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@csrf_protect
def register(request):
    if request.method == 'POST':
        try:
            # Try to parse the request body as JSON
            data = json.loads(request.body)
            print("Received data:", data)  # Log the parsed data

            # Manually create a form using the received data
            form = UserCreationForm(data)

            # Check if the form is valid
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'User registered successfully'}, status=201)
            else:
                return JsonResponse({'error': form.errors}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred', 'message': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Use POST method to register'}, status=405)

@csrf_protect  # Optionally use this if you want to allow non-logged-in users to make requests without CSRF validation.
def login_view(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Successful login: Log the user in and return success message
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                # Authentication failed: Invalid credentials
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_protect  # Protect the login view with CSRF protection
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                csrf_token = get_token(request)  # Get CSRF token
                response = JsonResponse({'message': 'Login successful'})
                response.set_cookie(
                'csrftoken', csrf_token,          # Set the CSRF token value
                samesite='None',                  # Ensure this is a string, NOT a tuple
                secure=True                       # If using HTTPS, set this to True
            ) 
                 # Set the CSRF token in the cookie
                print(f"Set CSRF token in cookie: {csrf_token}")
                return response
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
            

        
# @login_required
# def edit_blog(request, pk):
#     blog_post = get_object_or_404(BlogPost, pk=pk, author=request.user)
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = BlogPostForm(instance=blog_post)
#     return render(request, 'edit_blog.html', {'form': form})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost
from .serializers import BlogPostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

@api_view(['PATCH'])
def edit_blog(request, pk):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the blog post by primary key
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # Ensure the authenticated user is the author of the blog post
    if blog_post.author != request.user:
        return Response({"error": "You can only edit your own posts."}, status=status.HTTP_403_FORBIDDEN)

    # Pass the 'request' context when initializing the serializer
    serializer = BlogPostSerializer(blog_post, data=request.data, partial=True, context={'request': request})

    if serializer.is_valid():
        serializer.save()  # Save the updated blog post
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_blog(request, pk):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the blog post by primary key
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # Ensure the authenticated user is the author of the blog post
    if blog_post.author != request.user:
        return Response({"error": "You can only update your own posts."}, status=status.HTTP_403_FORBIDDEN)

    # Update the blog post with the full data provided
    serializer = BlogPostSerializer(blog_post, data=request.data)

    if serializer.is_valid():
        serializer.save()  # Save the updated blog post
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def update_blog(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('Blog_list')
    else:
        form = BlogPostForm(instance=blog_post)
    
    return render(request, 'edit_blog.html', {'form': form})

# View to list all blog posts
class BlogPostList(APIView):
    def get(self, request, format=None):
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

# View to get a single blog post by ID
class BlogPostDetail(APIView):
    def get(self, request, pk, format=None):
        post = BlogPost.objects.get(pk=pk)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)

# API View for user registration
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # Allow public access to registration API

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def post(self, request, format=None):
        try:
            # Debugging: Print the CSRF token sent in the headers
            csrf_token_received = request.META.get('HTTP_X_CSRFTOKEN')
            print(f"CSRF Token Received: {csrf_token_received}")  # Debugging

            # Parse the incoming JSON data
            data = json.loads(request.body)
            username_or_email = data.get('username')  # Accept username or email
            password = data.get('password')

            if not username_or_email or not password:
                return Response({'error': 'Username or email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Try to get the user by username or email
            user = None
            if '@' in username_or_email:
                # If it's an email, find the user by email
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Otherwise, treat it as a username and authenticate
                user = authenticate(request, username=username_or_email, password=password)

            # If user is found and authenticated
            if user is not None:
                login(request, user)  # Log the user in
                csrf_token = get_token(request)  # Get the CSRF token for the session
                response = JsonResponse({'message': 'Login successful'})
                response.set_cookie(
                    'csrftoken', csrf_token,  # Set the CSRF token value in the cookie
                    samesite='None',          # Ensure it's a string, not a tuple
                    secure=True               # Set to True if using HTTPS
                )
                return response
            else:
                # Authentication failed: Invalid credentials
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': 'Invalid request', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def get(self, request):
        user = request.user  # The authenticated user
        # Fetch the user's blog posts
        user_posts = BlogPost.objects.filter(author=user)
        
        # Serialize the posts
        posts_data = BlogPostSerializer(user_posts, many=True).data

        # Log the authenticated user and their posts count for debugging
        print(f"User {user.username} is authenticated and has {len(posts_data)} posts.")

        # Return profile data (username and serialized posts)
        return Response({
            "username": user.username,
            "email": user.email,
            "user_posts": posts_data
        })
    
class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)