from api.serializers import UserSerializer
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import (
    Organization,
    OrgClass,
    Exam,
    User,
    Admin,
)

# Create your views here.


# FROM THE POV OF STUDENT

@api_view(["POST"])
def signUpUser(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    phone = request.data.get("phone")

    data = {
        "name": name,
        "email": email,
        "password": password,
        "phone": phone,
        "is_staff": False,
    }
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def signInUser(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.filter(email = email)
    # if user.password == password:
    #     return 
        
    # if user is not None:
    #         login(request, user)
    #         return HttpResponse()
    #     elif User.objects.filter(email=email).count():
    #         inst = User.objects.get(email=email)
    #         if Student.check_password(inst, password):
    #             return Response(status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     else:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    # else:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def joinOrgClass(request):
    pass

@api_view()
def registerExam(request):
    pass



@api_view()
def fetchExams(request):
    # studentId = request.data.get("studentId")
    # organizationId = request.data.get("organizationId")
    organizationClassId = request.data.get("organizationClassId")
    # student = User.objects.get(id=studentId)
    # organization = Organization.objects.get(id=organizationId)

    exams = Exam.filter(org_class_id=organizationClassId)
    # ser exams => data
    serialzer = ExamSerializer(data=exams)
    data = serialzer.data

    return Response(status=status.HTTP_200_OK, data=data)


@api_view()



# FROM THE POV OF ADMIN/INSTITUTE

@api_view()
def signUpInstitute(request):
    name = request.data.get("name")
    phone = request.data.get("phone")

    # accessibility

@api_view()
def signInInstitute(request):
    return Response(status=status.HTTP_200_OK, data={"message": "Heyy!"})

@api_view()
def addClass(request): 
    pass

@api_view()
def addExam(request):
    pass

