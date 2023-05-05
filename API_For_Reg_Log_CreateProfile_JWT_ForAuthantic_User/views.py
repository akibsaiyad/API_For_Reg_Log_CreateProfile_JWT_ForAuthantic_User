from django.shortcuts import render,redirect
from .models import *
from .serializers import *
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework_simplejwt import authentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly,IsAuthenticated
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, GenericAPIView, CreateAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
# from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny,BasePermission,SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import permission_classes
# Create your views here.
from django.shortcuts import get_object_or_404


@api_view()
@permission_classes([IsAuthenticated])
def profile_list(request):

    print(request.user.id)
    user = Profile.objects.all()
    serializer = ProfileSerializer(user,many=True)
    return Response(serializer.data)



class IsLoggedInUserOrReadOnly(BasePermission):
    
    def has_object_permission(self, request,obj):
        
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT':
            return request.user.is_authenticated
        print('akib')
        return True

class GetallBlog(ListCreateAPIView):
    queryset = Blog.objects.all().filter(is_verified=True)
    serializer_class = BlogSerializer
    permission_classes = [IsLoggedInUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogSerializer
        elif self.request.user.is_authenticated:
            return BlogSerializer
        else:
            return BlogSummarySerializer
        
      


@api_view()
@permission_classes([IsAuthenticated])
def profile_retrive(request,pk):

    user = Profile.objects.get(pk=pk)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)



class RegisterApi(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })



class EditProfile(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().user.id:
            print('akib')
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"msg":"un auth"}, status=status.HTTP_401_UNAUTHORIZED)
    
class CreateBlog(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = User.objects.get(id=self.request.user.id)
        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EditBlog(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    def patch(self, request, *args, **kwargs):
        if request.user.id == self.get_object().user.id:
            # if request.user.is_staf:
                # return True
            return self.partial_update(request, *args, **kwargs)
                 
        else:
            return Response({"msg":"un auth"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])    
def VerifieBlog(request, pk):
    print(request.user)
    if request.user.is_anonymous:
        return Response({'msg':"Unauth"})
    
    print(request.user)
    userprofile = Profile.objects.get(user=request.user.id)
    if userprofile.role == 'admin':
        blogtoverify = get_object_or_404(Blog, pk=pk) 
        blogtoverify.is_verified = True
        blogtoverify.save()
        return Response({"msg":"blog verifyed"})
    return Response({'test':'TEST'})

