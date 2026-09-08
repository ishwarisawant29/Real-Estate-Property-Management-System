from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from .forms import InquiryForm, PropertyForm, PropertyImageForm, RegisterForm, ReviewForm, VisitForm
from .models import Category, City, Favorite, Inquiry, Notification, Profile, Property, Review, Visit


def home(request):
    properties = Property.objects.filter(status='Available').order_by('-created_at')[:6]
    return render(request, 'home.html', {'properties': properties})


def property_list(request):
    properties = Property.objects.filter(status='Available')
    search = request.GET.get('search')
    city = request.GET.get('city')
    category = request.GET.get('category')

    if search:
        properties = properties.filter(title__icontains=search)
    if city:
        properties = properties.filter(city_id=city)
    if category:
        properties = properties.filter(category_id=category)

    return render(request, 'properties.html', {
        'properties': properties,
        'cities': City.objects.all(),
        'categories': Category.objects.all(),
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    reviews = Review.objects.filter(property=property_obj).order_by('-created_at')
    return render(request, 'property_detail.html', {'property': property_obj, 'reviews': reviews})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, role='Customer')
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            if hasattr(user, 'profile') and user.profile.role == 'Agent':
                return redirect('agent_dashboard')
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def add_favorite(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    Favorite.objects.get_or_create(user=request.user, property=property_obj)
    return redirect('property_detail', pk=pk)


@login_required
def remove_favorite(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    Favorite.objects.filter(user=request.user, property=property_obj).delete()
    return redirect('favorites')


@login_required
def favorites(request):
    properties = Property.objects.filter(favorites__user=request.user)
    return render(request, 'favorites.html', {'properties': properties})


@login_required
def inquiry(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    form = InquiryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user, obj.property = request.user, property_obj
        obj.save()
        Notification.objects.create(
            user=property_obj.agent,
            message=f'New inquiry for {property_obj.title}'
        )
        return redirect('property_detail', pk=pk)
    return render(request, 'inquiry.html', {'form': form, 'property': property_obj})


@login_required
def visit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    form = VisitForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user, obj.property = request.user, property_obj
        obj.save()
        Notification.objects.create(
            user=property_obj.agent,
            message=f'New visit request for {property_obj.title}'
        )
        return redirect('property_detail', pk=pk)
    return render(request, 'visit.html', {'form': form, 'property': property_obj})


@login_required
def review(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user, obj.property = request.user, property_obj
        obj.save()
        return redirect('property_detail', pk=pk)
    return render(request, 'review.html', {'form': form, 'property': property_obj})


@login_required
def dashboard(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'Agent':
        return redirect('agent_dashboard')

    context = {
        'favorites_count': Favorite.objects.filter(user=request.user).count(),
        'inquiries': Inquiry.objects.filter(user=request.user).select_related('property', 'property__agent').order_by('-created_at'),
        'visits': Visit.objects.filter(user=request.user).select_related('property').order_by('-visit_date'),
        'notifications': Notification.objects.filter(user=request.user).order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)


@login_required
def agent_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Agent':
        return redirect('dashboard')
    context = {
        'my_properties': Property.objects.filter(agent=request.user),
        'my_inquiries': Inquiry.objects.filter(property__agent=request.user).order_by('-created_at'),
        'my_visits': Visit.objects.filter(property__agent=request.user).order_by('-visit_date'),
    }
    return render(request, 'agent_dashboard.html', context)


@login_required
def reply_inquiry(request, pk):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Agent':
        return redirect('dashboard')

    inquiry_obj = get_object_or_404(Inquiry, pk=pk, property__agent=request.user)
    if request.method == 'POST':
        reply = request.POST.get('reply', '').strip()
        if reply:
            inquiry_obj.reply = reply
            inquiry_obj.status = 'Replied'
            inquiry_obj.replied_at = timezone.now()
            inquiry_obj.save()
            Notification.objects.create(
                user=inquiry_obj.user,
                message=f'Agent replied to your inquiry about {inquiry_obj.property.title}.'
            )
            messages.success(request, 'Reply sent to the customer.')
    return redirect('agent_dashboard')


@login_required
def update_visit_status(request, pk, status):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Agent':
        return redirect('dashboard')
    visit_obj = get_object_or_404(Visit, pk=pk, property__agent=request.user)
    if status in ('approved', 'rejected'):
        visit_obj.status = status.title()
        visit_obj.save()
        Notification.objects.create(
            user=visit_obj.user,
            message=f'Your visit request for {visit_obj.property.title} has been {visit_obj.status.lower()}.'
        )
    return redirect('agent_dashboard')


@login_required
def notifications(request):
    items = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': items})


@login_required
def add_property(request):
    form = PropertyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.agent = request.user
        obj.save()
        return redirect('agent_dashboard')
    return render(request, 'add_property.html', {'form': form})


@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, agent=request.user)
    form = PropertyForm(request.POST or None, instance=property_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agent_dashboard')
    return render(request, 'edit_property.html', {'form': form, 'property': property_obj})


@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, agent=request.user)
    if request.method == 'POST':
        property_obj.delete()
        return redirect('agent_dashboard')
    return render(request, 'delete_property.html', {'property': property_obj})


@login_required
def add_property_image(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, agent=request.user)
    form = PropertyImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.property = property_obj
        obj.save()
        return redirect('property_detail', pk=pk)
    return render(request, 'add_property_image.html', {'form': form, 'property': property_obj})
