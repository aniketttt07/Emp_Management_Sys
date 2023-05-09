from django.shortcuts import render, HttpResponse
from django.db import IntegrityError
from .models import Employee, Role, Department
from datetime import datetime
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html') 

def viewEmp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'viewEmp.html', context)

def addEmp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        dept_id = request.POST.get('dept')
        role_id = request.POST.get('role')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')

        try:
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Department.DoesNotExist:
            return HttpResponse('Department does not exist')
        except Role.DoesNotExist:
            return HttpResponse('Role does not exist')
        except IntegrityError:
            return HttpResponse('An Exceptional error')

        employee = Employee(first_name=first_name, last_name=last_name, salary=salary, dept=dept, role=role, bonus=bonus, phone=phone, hire_date=datetime.today())
        employee.save()
        messages.success(request, 'Your message has been sent!')
        return render(request, 'addEmp.html')
    elif request.method == 'GET':
        return render(request, 'addEmp.html')
    else:
        return HttpResponse('An Exceptional error')

def removeEmp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Remove Successfully")
        except:
            return HttpResponse('Please select valid id')
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'removeEmp.html', context)

def filterEmp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name=dept)
        if role:
            emps = emps.filter(role__name=role)

        context = {
            'emps': emps
        }
        return render(request, 'viewEmp.html', context)
    elif request.method == 'GET':
        return render(request, 'filterEmp.html')
    else:
        return render(request, 'An Exception Occurred')

