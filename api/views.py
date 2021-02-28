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
    OrgAdmin,
    UserClass,
)
import string
import random

# Create your views here.


@api_view()
def whoAmI(request):
    try:
        user = Student.objects.get(email=request.user.email)
        user = 'student'
    except:
        user = 'orgadmin'
    print(user)
    return Response(status=status.HTTP_200_OK, data={'userType': user})

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
def _login(request):
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# for student to join a class using code ,and thereby subscribe to exams


@api_view(['POST'])
def joinOrgClass(request):
    code = request.data.get('code')
    email = request.data.get('email')
    try:
        org_class = OrgClass.objects.get(class_code=code)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    org = org_class.organization
    student = Student.objects.get(email=email)
    data = {
        user: student,
        org_class: org_class,
        organization: org,
    }
    serializer = UserClassSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for student to register to an exam : public
@api_view(['POST'])
def registerExam(request):
    email = request.data.get('email')
    org_id = request.data.get('org_id')
    class_id = request.data.get('class_id')
    try:
        student = Student.objects.get(email=email)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {
        user: student.id,
        org_class: class_id,
        organization: org_id,
    }
    serializer = UserClassSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def fetchExams(request):
    class_id = request.data.get("class_id")
    try:
        exams = Exam.objects.filter(org_class_id=class_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if exams.count() != 0:
        serializer = ExamSerializer(data=exams)
        data = serializer.data
        return Response(status=status.HTTP_200_OK, data=data)
    else:
        return Response(
            data="No exams yet", status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def getMyClasses(request):
    user_id = request.data.get('user_id')

    try:
        user_classes = UserClass.objects.filter(user=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    class_ids = []
    for u_class in user_classes:
        class_ids.append(u_class.id)

    classes_data = []
    for id in class_ids:
        c = OrgClass.objects.get(id=id)
        _temp = {
            class_id: id,
            name: c.name,
            description: c.description,
        }
        classes_data.append(_temp)

    response = {
        classes: classes_data
    }
    return Response(data=response)


# SEARCHBAR

@api_view(['GET'])
def getPublic(request):
    search_term = request.data.get('search')

    try:
        orgs = Organization.objects.filter(
            org_name=search_term, accessibility=False)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    org_ids = []
    for org in orgs:
        org_ids.append(org.id)

    org_data = []
    for id in org_ids:
        c = Organization.objects.get(id=id)
        _temp = {
            org_id: id,
            name: c.name,
        }
        org_data.append(_temp)

    response = {
        org: org_data,
    }
    return Response(data=response)

# FROM THE POV OF ADMIN/INSTITUTE


@api_view(['GET'])
def getOrgClasses(request):
    org_id = request.data.get('org_id')

    try:
        user_classes = UserClass.objects.filter(organization=org_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    class_ids = []
    for u_class in user_classes:
        class_ids.append(u_class.id)

    classes_data = []
    for id in class_ids:
        c = OrgClass.objects.get(id=id)
        _temp = {
            class_id: id,
            name: c.name,
            description: c.description,
        }
        classes_data.append(_temp)

    response = {
        classes: classes_data
    }
    return Response(data=response)


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

    admin_name = request.data.get("name")
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


@api_view(["POST"])
def signInInstitute(request):
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        admin = authenticate(request, email=email, password=password)
        if admin is not None:
            login(request, admin)
            return HttpResponse()
        elif OrgAdmin.objects.filter(email=email).count():
            inst = OrgAdmin.objects.get(email=email)
            if OrgAdmin.check_password(inst, password):
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def crudClass(request):
    if request.method == "GET":
        class_id = request.data.get('class_id')
        try:
            classObj = OrgClass.objects.get(id=class_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        org = classObj.organization
        org_name = Organization.objects.get(id=org).org_name
        data = {
            class_code: classObj.class_code,
            name: classObj.name,
            description: classObj.description,
            organizaton: org_name
        }
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        class_id = request.data.get('class_id')
        try:
            classObj = OrgClass.objects.get(id=class_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if(request.data.get('name') not in ["", None]):
            name = request.data.get('name')
        if(request.data.get('description') not in ["", None]):
            description = request.data.get('description')

            classObj.save()
        data = {
            class_code: classObj.class_code,
            Organization: classObj.organization,
            name: name,
            description: description
        }
        serializer = OrgClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description')
        org_id = request.data.get('org_id')
        org = Organization.objects.get(id=org_id)
        class_code = None
        if org.accessibility == True:  # which means org private
            while True:
                class_code = ''.join(random.choices(string.ascii_uppercase +
                                                    string.digits, k=9))
                org_class = OrgClass.objects.get(class_code=class_code)
                if org_class is not None:
                    continue
                else:
                    break

        data = {
            class_code: class_code,
            name: name,
            description: description,
            organization: org,
        }
        serializer = OrgClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pass
    elif request.method == 'DELETE':
        class_id = request.data.get('class_id')
        try:
            classObj = OrgClass.objects.get(id=class_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        classObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def crudStudent(request):
    if request.method == "GET":
        # get students based on class id
        class_id = request.data.get('class_id')
        classes = UserClass.objects.filter(org_class_id=class_id)
        students = []
        for c in classes:
            students.append(c.user)

        student_data = []
        for student in students:
            student_data.append(Student.objects.get(id=student))

        if student_data.count() != 0:
            response = {}
            response.setdefault('students', student_data)
            return Response(status=status.HTTP_200_OK, data=response)
        else:
            return Response(
                data="No students in the class yet", status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'PUT':
        user_id = request.data.get('user_id')
        user = Student.objects.get(id=user_id)
        if(request.data.get('name') not in ["", None]):
            user.name = request.data.get('name')
        if(request.data.get('email') not in ["", None]):
            user.email = request.data.get('email')
        if(request.data.get('phone') not in ["", None]):
            user.phone = request.data.get("phone")
        if(request.data.get('password') not in ["", None]):
            user.phone = request.data.get("password")

        user.save()
        return Response()

    elif request.method == 'DELETE':
        user_id = request.data.get('user_id')
        user = Student.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        pass


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def crudExam(request):
    if request.method == "GET":
        class_id = request.data.get('class_id')
        exams = Exam.objects.filter(org_class_id=class_id)
        # ser exams => data
        if exams.count() != 0:
            serializer = ExamSerializer(data=exams)
            data = serializer.data
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(
                data="No exams yet", status=status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'PUT':
        exam_id = request.data.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        if(request.data.get('name') not in ["", None]):
            exam.name = request.data.get('name')
        if(request.data.get('description') not in ["", None]):
            exam.description = request.data.get('description')
        if(request.data.get('date') not in ["", None]):
            exam.date = timezone.datetime.fromtimestamp(
                int(request.data.get("date")))

        exam.save()
        return Response()

    elif request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description')
        date = timezone.datetime.fromtimestamp(int(request.data.get("date")))
        class_id = request.data.get('class_id')
        org_class = OrgClass.objects.get(id=class_id)
        data = {
            exam_name: name,
            description: description,
            date: date,
            organization: org_class.organization,
            org_class: class_id
        }
        serializer = ExamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exam_id = request.data.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def signOut(request):
    print('logged out')
    logout(request)
    return Response(status=status.HTTP_200_OK)
