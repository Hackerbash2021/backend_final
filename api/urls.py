from django.http.response import HttpResponse, JsonResponse
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # User
    path("login/", views._login),
    # path("signInStudent/", views.signInStudent),
    path("signUpStudent/", views.signUpStudent),
    path("joinOrgClass/", views.joinOrgClass),
    # path("fetchOrg/",view.fetchOrg),
    path("fetchExams/", views.fetchExams),
    path("registerExam/", views.registerExam),
    # path("userProfile/", views.userProfile),
    # path("changePassword/", views.changePassword),
    # path("forgotPassword/", views.forgotPassword),
    path('getMyClasses/', views.getMyClasses),
    path('getPublic/', views.getMyClasses),
    path('whoAmI/', views.whoAmI),


    # Admin
    path('getOrgClasses/', views.getOrgClasses),
    path("signUpInstitute/", views.signUpInstitute),
    # path("signInInstitute/", views.signInInstitute),
    path("crudClass/", views.crudClass),
    path("crudStudent/", views.crudStudent),
    path("crudExam/", views.crudExam),


    # Common
    path("signOut/", views.signOut),


]
