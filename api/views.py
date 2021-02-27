from api.serializers import StudentSerializer
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import (
    Organization,
    OrgClass,
    Exam,
    Student,
    Admin,
)

# Create your views here.


# FROM THE POV OF STUDENT

@api_view(["POST"])
def signUpStudent(request):
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
    
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def signInStudent(request):
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse()
        elif Student.objects.filter(email=email).count():
            inst = Student.objects.get(email=email)
            if Student.check_password(inst, password):
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def joinOrgClass(request):
    code = request.data.get('code')
    email = request.data.get('email')
    org_class=OrgClass.objects.get(class_code = code)
    org = org_class.organization
    student = Student.objects.get(email = email)
    data = {
        user:student,
        org_class:org_class,
        organization: org,
    }
    serializer = UserClassSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def registerExam(request):
    email = request.data.get('email')
    org_id = request.data.get('org_id')
    student = Student.objects.get(email = email)
    data = {
        user:student,
        org_class:None,
        organization: org_id,
    }
    serializer = UserClassSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def fetchExams(request):
    # studentId = request.data.get("studentId")
    # organizationId = request.data.get("organizationId")
    class_id = request.data.get("class_id")
    org_class = OrgClass.objects.get(id = class_id)

    # student = Student.objects.get(id=studentId)

    exams = Exam.filter(org_class_id=organizationClassId)
    # ser exams => data
    serialzer = ExamSerializer(data=exams)
    data = serialzer.data

    return Response(status=status.HTTP_200_OK, data=data)


# FROM THE POV OF ADMIN/INSTITUTE

@api_view()
def signUpInstitute(request):
    org_name = request.data.get("org_name")
    accessibility = request.data.get("accessibility")
    org_type = request.data.get("org_type")

    org_data = {
        "org_name": org_name,
        "accessibility": accessibility,
        "org_type": org_type,
    }

    admin_name = request.data.get("admin_name")
    email = request.data.get("email")
    password = request.data.get("password")
    phone = request.data.get("phone")

    admin_data = {
        "admin_name": admin_name,
        "phone": phone,
        "email": email,
        "password": password,
        "is_staff": False,
    }

    serializer1 = OrganizationSerializer(data=org_data)
    if serializer1.is_valid():
        serializer1.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer2 = AdminSerializer(data=admin_data)
    if serializer2.is_valid():
        serializer2.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def signInInstitute(request):
    return Response(status=status.HTTP_200_OK, data={"message": "Heyy!"})

@api_view(['GET','PUT','POST','DELETE'])
def crudClass(request): 
    if request.method == "GET":
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method =='DELETE':
        pass


@api_view(['GET','PUT','POST','DELETE'])
def crudStudent(request):
    email = request.data.get('email')
    if request.method == "GET":
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method =='DELETE':
        pass

@api_view(['GET','PUT','POST','DELETE'])
def crudExam(request):
    email = request.data.get('email')
    if request.method == "GET":
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method =='DELETE':
        pass

# @api_view(['DELETE'])
# def removeExam(request):
#     pass