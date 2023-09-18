from django.http import HttpResponse
from .models import Sensor, Werte
from .forms.TempsFilterForm import TempsFilterForm
from .forms.SensorForm import SensorForm
from django.db.models import Max, Min
from datetime import timedelta

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/web')
    else:
        form = UserCreationForm()
    return render(request, 'web/auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'web/auth/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    users = User.objects.all
    return render(request, 'web/index.html', {'users': users})


def display_sensors(request):
    queryset = Sensor.objects.all()
    return render(request, "web/sensors/index.html", {
        "sensorlist": list(queryset)
    })


def edit_sensor(request, sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)

    if request.method == "POST":
        print("GET")
        form = SensorForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
            return redirect("/web/sensors/")
    else:
        form = SensorForm(instance=sensor)
        return render(request, "web/sensors/edit.html", {"form": form})


def new_sensor(request):
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/web/sensors')
    else:
        form = SensorForm()
    return render(request, 'web/sensors/new.html', {'form': form})


def temp_details(request, temp_id):
    print(temp_id + "tempdetails")
    queryset = Sensor.objects.get(pk=temp_id)
    return HttpResponse(f"""Tempdetails for Sensor-ID {temp_id}:
                         {queryset.sen_raum}, 
                         {queryset.sen_ip},
                         {queryset.sen_code}""")


def display_temps(request):
    if request.method == "POST":
        form = TempsFilterForm(request.POST)

        if form.is_valid():
            lower_val = form.cleaned_data["lowerVal"]
            if lower_val is None:
                lower_val = Werte.objects.aggregate(Min('temperatur'))["temperatur__min"]

            upper_val = form.cleaned_data["upperVal"]
            if upper_val is None:
                upper_val = Werte.objects.aggregate(Max('temperatur'))["temperatur__max"]

            date_from = form.cleaned_data["vonDate"]
            date_until = form.cleaned_data["bisDate"]

            queryset = Werte.objects.filter(
                datum__gte=date_from,
                datum__lte=(date_until + timedelta(days=1)),
                temperatur__lte=upper_val,
                temperatur__gte=lower_val,
            )

            return render(request, "web/sensors/temps.html", {"name": "Berg", "temp_list": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        form = TempsFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        temp_list = list(queryset)
        return render(request, "web/sensors/temps.html", {"form": form, "temp_list": temp_list})


def display_humid(request):
    if request.method == "POST":
        form = TempsFilterForm(request.POST)

        if form.is_valid():
            lower_val = form.cleaned_data["lowerVal"]
            if lower_val is None:
                lower_val = Werte.objects.aggregate(Min('temperatur'))["temperatur__min"]

            upper_val = form.cleaned_data["upperVal"]
            if upper_val is None:
                upper_val = Werte.objects.aggregate(Max('temperatur'))["temperatur__max"]

            date_from = form.cleaned_data["vonDate"]
            date_until = form.cleaned_data["bisDate"]

            queryset = Werte.objects.filter(
                datum__gte=date_from,
                datum__lte=(date_until + timedelta(days=1)),
                temperatur__lte=upper_val,
                temperatur__gte=lower_val,
            )

            return render(request, "web/sensors/humid.html", {"name": "Berg", "temp_list": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        form = TempsFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        temp_list = list(queryset)
        return render(request, "web/sensors/humid.html", {"form": form, "temp_list": temp_list})

def display_air_press(request):
    if request.method == "POST":
        form = TempsFilterForm(request.POST)

        if form.is_valid():
            lower_val = form.cleaned_data["lowerVal"]
            if lower_val is None:
                lower_val = Werte.objects.aggregate(Min('temperatur'))["temperatur__min"]

            upper_val = form.cleaned_data["upperVal"]
            if upper_val is None:
                upper_val = Werte.objects.aggregate(Max('temperatur'))["temperatur__max"]

            date_from = form.cleaned_data["vonDate"]
            date_until = form.cleaned_data["bisDate"]

            queryset = Werte.objects.filter(
                datum__gte=date_from,
                datum__lte=(date_until + timedelta(days=1)),
                temperatur__lte=upper_val,
                temperatur__gte=lower_val,
            )

            return render(request, "web/sensors/air-press.html", {"name": "Berg", "temp_list": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        form = TempsFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        temp_list = list(queryset)
        return render(request, "web/sensors/air-press.html", {"form": form, "temp_list": temp_list})
