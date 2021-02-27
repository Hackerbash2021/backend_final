from django.http.response import HttpResponse, JsonResponse
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # User
    path("signInStudent/", views.signInStudent),
    path("signUpStudent/", views.signUpStudent),
    path("joinClass/", views.joinClass)
    path("fetchOrg/",view.fetchOrg),
    path("fetchExams/", views.fetchExams),
    path("registerExam/", views.registerExam),
    # path("userProfile/", views.userProfile),
    # path("changePassword/", views.changePassword),
    # path("forgotPassword/", views.forgotPassword),

    # Admin
    path("signUpInstitute/", views.signUpInstitute),
    path("signInInstitute/", views.signInInstitute),
    path("crudClass/", views.crudClass),
    # path("removeClass/", views.removeClass),
    # path("addStudent/", views.addStudent),
    path("crudStudent/", views.crudStudent),
    path("crudExam/", views.crudExam),
    # path("removeExam/", views.removeExam),

    # Common 
    path("signOut/", views.signOut),
    
  
]
