from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Api.views import *
from Api import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


router = DefaultRouter()

# router.register(r'login', LoginUser, basename='login')
# router.register(r'blog', Blogviewset, basename='blog')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.profile_list),
    path('user/<int:pk>/', views.profile_retrive),
    path('registration/', RegisterApi.as_view(), name='registration'),
    path('login/', TokenObtainPairView.as_view(), name='gettoken'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='verify'),
    path('createblog/', CreateBlog.as_view(), name='create'),
    path('editblog/<int:pk>', EditBlog.as_view(), name='editblog'),
    path('editprofile/<int:pk>', views.EditProfile.as_view(), name='edit'),
    path('editprofile/', views.EditProfile.as_view()),
    # path('', include(router.urls)),
    path('getall-blog',GetallBlog.as_view(),name='getblog'),
    path('verifybog/<int:pk>', views.VerifieBlog),
    path('', include('rest_framework.urls')),
]
