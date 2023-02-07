from django.shortcuts import render
from django.template import loader
from myapp.form import EmpForm, StudentForm, EmployeeForm
from myapp.functions.functions import handle_uploaded_file
from myapp.models import Employee

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
import datetime
import csv
from reportlab.pdfgen import canvas
@require_http_methods(["GET"])

def getpdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename="file.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Times-Roman",55)
    p.drawString(100,700,"Halo Dodol")
    p.showPage()
    p.save()
    return response

def getcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    employees = Employee.objects.all()
    writer = csv.writer(response)
    for employee in employees:
        writer.writerow([employee.eid,employee.ename,employee.econtact])
    return response

def getfile(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment;filename="file.csv"'
    writer = csv.writer(response)
    writer.writerow(['101','Semangka','Padalarang','Bandung'])
    writer.writerow(['102','Juliet','Ciclilin','Bandung'])
    writer.writerow(['103','Dodol Garut','Cikalong','Bandung'])
    return response



def setsession(request):
    request.session['sname'] = 'irfan'
    request.session['semail'] = 'irfan.sssit@gmail.com'
    return HttpResponse("session is set")

def getsession(request):
    studentname = request.session['sname']
    studentemail = request.session['semail']
    return HttpResponse(studentname+" "+studentemail);

def setcookie(request):
    response = HttpResponse("Cookie set")
    response.set_cookie('alamat','Padalarang')
    return response

def getcookie(request):
    alamat = request.COOKIES['alamat']
    return HttpResponse("Alamatnya ada di ? "+ alamat)

def show(request):
    return HttpResponse('<h1> Ini Http GET Method</h1>')

def hello(request):
    return HttpResponse("<h2> Dodol siah</h2>")

def index(request):
    now = datetime.datetime.now()
    #html = "<html><body><h3>Now time is %s.</h3></body></html>" % now

    #template = loader.get_template('index.html')
    #nama = {
    #    "student":"Dedi Triyanto"
    #}
    stu = EmpForm()
    return render(request,"index.html",{'form':stu})
    #return (HttpResponse(template.render(nama)))

def formstudent(request):
    student = StudentForm()
    return render(request,"index.html",{'form':student})

def emp(request):
    if request.method =='POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                return redirect('/')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request,'index.html',{'form':form})

def uploadfile(request):
    if request.method=='POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File Uploaded succcess")
    else:
        student = StudentForm()
        return render(request,"index.html",{'form':student})

def login(request):
    return render(request,"login.html")
