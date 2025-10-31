from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import Car, Case, Series, CollectorProfile
from .forms import CarForm, LoginForm, CaseForm, SeriesForm

def home(request):
    """Dynamic homepage showing collection"""
    cases = Case.objects.annotate(car_count=Count('cars')).order_by('name')
    series = Series.objects.filter(is_active=True).annotate(car_count=Count('cars')).order_by('name')
    
    # Get treasure hunts
    treasure_hunts = Car.objects.filter(
        Q(treasure_hunt='TH') | Q(treasure_hunt='STH') | Q(treasure_hunt='CHASE')
    ).order_by('-created_at')[:12]
    
    # Get all cars for complete gallery
    recent_cars = Car.objects.all().order_by('-created_at')
    
    # Get collector profile
    collector = CollectorProfile.objects.first()
    
    # Statistics
    total_cars = Car.objects.count()
    total_cases = cases.count()
    total_series = series.count()
    total_sth = Car.objects.filter(treasure_hunt='STH').count()
    total_th = Car.objects.filter(treasure_hunt='TH').count()
    total_chase = Car.objects.filter(treasure_hunt='CHASE').count()
    
    context = {
        'cases': cases,
        'series': series,
        'treasure_hunts': treasure_hunts,
        'recent_cars': recent_cars,
        'collector': collector,
        'total_cars': total_cars,
        'total_cases': total_cases,
        'total_series': total_series,
        'total_sth': total_sth,
        'total_th': total_th,
        'total_chase': total_chase,
    }
    
    return render(request, 'collection/home.html', context)


def user_login(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'collection/login.html', {'form': form})

def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    """Custom collector dashboard"""
    collector = CollectorProfile.objects.first()
    
    # Get all data
    cases = Case.objects.annotate(car_count=Count('cars')).order_by('name')
    series = Series.objects.annotate(car_count=Count('cars')).order_by('name')
    cars = Car.objects.all().order_by('-created_at')
    
    # Filters
    case_filter = request.GET.get('case')
    series_filter = request.GET.get('series')
    th_filter = request.GET.get('th')
    
    if case_filter:
        cars = cars.filter(case__name=case_filter)
    if series_filter:
        cars = cars.filter(series__slug=series_filter)
    if th_filter:
        cars = cars.filter(treasure_hunt=th_filter)
    
    context = {
        'collector': collector,
        'cases': cases,
        'series': series,
        'cars': cars,
        'case_filter': case_filter,
        'series_filter': series_filter,
        'th_filter': th_filter,
    }
    
    return render(request, 'collection/dashboard.html', context)

class CarDetailView(DetailView):
    model = Car
    template_name = 'collection/car_detail.html'
    context_object_name = 'car'
    slug_field = 'slug'

@login_required(login_url='login')
def car_create(request):
    """Create new car"""
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, f'Successfully added {car.casting_name}!')
            return redirect('dashboard')
    else:
        form = CarForm()
    
    return render(request, 'collection/car_form.html', {'form': form, 'title': 'Add New Car'})

@login_required(login_url='login')
def car_update(request, slug):
    """Update existing car"""
    car = get_object_or_404(Car, slug=slug)
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            messages.success(request, f'Successfully updated {car.casting_name}!')
            return redirect('car_detail', slug=car.slug)
    else:
        form = CarForm(instance=car)
    
    return render(request, 'collection/car_form.html', {'form': form, 'title': 'Edit Car', 'car': car})

@login_required(login_url='login')
def car_delete(request, slug):
    """Delete car"""
    car = get_object_or_404(Car, slug=slug)
    
    if request.method == 'POST':
        car_name = car.casting_name
        car.delete()
        messages.success(request, f'Successfully deleted {car_name}!')
        return redirect('dashboard')
    
    return render(request, 'collection/car_confirm_delete.html', {'car': car})

def case_detail(request, case_name):
    """Show all cars in a specific case"""
    case = get_object_or_404(Case, name=case_name)
    cars = Car.objects.filter(case=case).order_by('number', 'casting_name')
    
    context = {
        'case': case,
        'cars': cars,
    }
    
    return render(request, 'collection/case_detail.html', context)

def series_detail(request, slug):
    """Show all cars in a specific series"""
    series = get_object_or_404(Series, slug=slug)
    cars = Car.objects.filter(series=series).order_by('number', 'casting_name')
    
    context = {
        'series': series,
        'cars': cars,
    }
    
    return render(request, 'collection/series_detail.html', context)

@login_required(login_url='login')
def case_create(request):
    """Create new case"""
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            messages.success(request, f'Successfully created Case {case.name}!')
            return redirect('dashboard')
    else:
        form = CaseForm()
    
    return render(request, 'collection/case_form.html', {'form': form, 'title': 'Add New Case'})

@login_required(login_url='login')
def case_update(request, case_name):
    """Update existing case"""
    case = get_object_or_404(Case, name=case_name)
    
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save()
            messages.success(request, f'Successfully updated Case {case.name}!')
            return redirect('dashboard')
    else:
        form = CaseForm(instance=case)
    
    return render(request, 'collection/case_form.html', {'form': form, 'title': 'Edit Case', 'case': case})

@login_required(login_url='login')
def case_delete(request, case_name):
    """Delete case"""
    case = get_object_or_404(Case, name=case_name)
    
    if request.method == 'POST':
        case_name_display = f"Case {case.name}"
        case.delete()
        messages.success(request, f'Successfully deleted {case_name_display}!')
        return redirect('dashboard')
    
    return render(request, 'collection/case_confirm_delete.html', {'case': case})

@login_required(login_url='login')
def series_create(request):
    """Create new series"""
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save()
            messages.success(request, f'Successfully created {series.name}!')
            return redirect('dashboard')
    else:
        form = SeriesForm()
    
    return render(request, 'collection/series_form.html', {'form': form, 'title': 'Add New Series'})

@login_required(login_url='login')
def series_update(request, slug):
    """Update existing series"""
    series = get_object_or_404(Series, slug=slug)
    
    if request.method == 'POST':
        form = SeriesForm(request.POST, instance=series)
        if form.is_valid():
            series = form.save()
            messages.success(request, f'Successfully updated {series.name}!')
            return redirect('dashboard')
    else:
        form = SeriesForm(instance=series)
    
    return render(request, 'collection/series_form.html', {'form': form, 'title': 'Edit Series', 'series': series})

@login_required(login_url='login')
def series_delete(request, slug):
    """Delete series"""
    series = get_object_or_404(Series, slug=slug)
    
    if request.method == 'POST':
        series_name = series.name
        series.delete()
        messages.success(request, f'Successfully deleted {series_name}!')
        return redirect('dashboard')
    
    return render(request, 'collection/series_confirm_delete.html', {'series': series})

@login_required(login_url='login')
def manage_collection(request):
    """Manage cases and series"""
    cases = Case.objects.annotate(car_count=Count('cars')).order_by('year', 'name')
    series = Series.objects.annotate(car_count=Count('cars')).order_by('name')
    
    context = {
        'cases': cases,
        'series': series,
    }
    
    return render(request, 'collection/manage_collection.html', context)

