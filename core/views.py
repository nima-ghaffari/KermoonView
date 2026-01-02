from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from django.contrib import messages

from .models import (
    Tour, Reservation, TourLeaderProfile, 
    Post, PostComment, Comment, LeaderReview, User
)
from .forms import TourForm, ProfileUpdateForm

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Public sectors --> home tour weblog
def index(request):
    latest_tours = Tour.objects.filter(is_active=True).order_by('-id')[:3]
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    tour_comments = Comment.objects.filter(is_approved=True).select_related('tour', 'user')
    leader_reviews = LeaderReview.objects.filter(is_approved=True).select_related('leader', 'user')
    latest_reviews = sorted(chain(tour_comments, leader_reviews), key=attrgetter('created_at'), reverse=True)[:4]
    return render(request, 'index.html', {'tours': latest_tours, 'posts': latest_posts, 'reviews': latest_reviews})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Get and show Tour list 
def tour_list(request):
    tours = Tour.objects.filter(is_active=True)
    search_query = request.GET.get('q')
    if search_query:
        tours = tours.filter(Q(title__icontains=search_query) | Q(location__icontains=search_query))
    return render(request, 'tours.html', {'tours': tours})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Show tour details for user and all .
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    reviews = tour.reviews.filter(is_approved=True)
    can_review = False
    
    if request.user.is_authenticated:
        can_review = Reservation.objects.filter(user=request.user, tour=tour, status='confirmed').exists() or \
                     Reservation.objects.filter(user=request.user, tour=tour, status='paid').exists()
    
    if request.method == 'POST' and request.user.is_authenticated and can_review:
        text = request.POST.get('comment_text')
        rating = request.POST.get('rating', 5)
        if text:
            Comment.objects.create(user=request.user, tour=tour, text=text, rating=int(rating), is_approved=False)
            messages.info(request, "نظر شما ثبت شد و پس از تایید نمایش داده می‌شود.")
            return redirect('tour_detail', tour_id=tour.id)
            
    return render(request, 'tour-details.html', {'tour': tour, 'reviews': reviews, 'can_review': can_review})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Guide list for Tour and Tourleader
def guide_list(request):
    guides = TourLeaderProfile.objects.filter(is_verified=True)
    return render(request, 'guides.html', {'guides': guides})

def guide_detail(request, guide_id):
    guide = get_object_or_404(TourLeaderProfile, pk=guide_id)
    tours = Tour.objects.filter(leader=guide.user, is_active=True)
    reviews = guide.reviews.filter(is_approved=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        rating_val = request.POST.get('rating')
        if comment_text and rating_val:
            LeaderReview.objects.create(leader=guide, user=request.user, comment=comment_text, rating=int(rating_val), is_approved=False)
            messages.info(request, "نظر شما ثبت شد.")
            return redirect('guide_detail', guide_id=guide_id)
            
    return render(request, 'guide-details.html', {'guide': guide, 'tours': tours, 'reviews': reviews})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Post details 
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(is_approved=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('comment_text')
        if text: 
            PostComment.objects.create(post=post, user=request.user, text=text, is_approved=True)
            return redirect('post_detail', post_id=post.id)
            
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# State of Reservations and Ticket management . 

@login_required(login_url='/login/')
def book_tour(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=tour_id)
        count = int(request.POST.get('passengers', 1))
        
        if tour.capacity < count:
            messages.error(request, "متاسفانه ظرفیت تور تکمیل شده است.")
            return redirect('tour_detail', tour_id=tour.id)
            
        if tour.hotel and tour.hotel.capacity < count:
            messages.error(request, "ظرفیت هتل برای این تعداد تکمیل شده است.")
            return redirect('tour_detail', tour_id=tour.id)

        Reservation.objects.create(
            user=request.user, 
            tour=tour, 
            passengers_count=count, 
            total_price=tour.price * count,
            status='pending'
        )
        
        tour.capacity -= count
        tour.save()
        
        if tour.hotel:
            tour.hotel.capacity -= count
            tour.hotel.save()

        messages.success(request, "رزرو انجام شد و در انتظار تایید مدیریت است.")
        return redirect('dashboard')
        
    return redirect('tour_detail', tour_id=tour_id)

@login_required(login_url='/login/')
def view_ticket(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user, status='confirmed')
    return render(request, 'ticket.html', {'reservation': reservation})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Statment Tourleader
@login_required(login_url='/login/')
def create_tour(request):
    if request.user.role != 'leader': 
        return redirect('index')
        
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.leader = request.user
            # مهم: تور غیرفعال ساخته می‌شود تا ادمین تایید کند
            tour.is_active = False 
            tour.save()
            messages.success(request, "تور ثبت شد و پس از تایید مدیریت نمایش داده می‌شود.")
            return redirect('dashboard')
    else: 
        form = TourForm()
    return render(request, 'create_tour.html', {'form': form})
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Statement of login page
@login_required(login_url='/login/')
def upgrade_to_leader(request):
    if request.user.role == 'leader':
        return redirect('dashboard')

    try:
        if hasattr(request.user, 'leader_profile'):
            profile = request.user.leader_profile
            if not profile.is_verified:
                messages.info(request, "درخواست شما قبلا ثبت شده و در انتظار تایید است.")
                return redirect('dashboard')
    except TourLeaderProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        specialty = request.POST.get('specialty')
        experience = request.POST.get('experience')
        motivation = request.POST.get('motivation')
        documents = request.FILES.get('documents')

        request.user.national_id = national_id
        request.user.save()

        TourLeaderProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'is_verified': False,
                'specialty': specialty,
                'experience_years': experience,
                'motivation': motivation,
                'documents': documents,
                'bio': motivation
            }
        )
        messages.success(request, "درخواست شما ثبت شد. پس از بررسی مدارک در پنل ادمین، حساب شما ارتقا می‌یابد.")
        return redirect('dashboard')

    return render(request, 'upgrade_to_leader.html')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Dashboard and sign in page 
@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    is_pending_leader = False
    
    if user.role == 'user':
        try:
            if hasattr(user, 'leader_profile') and not user.leader_profile.is_verified:
                is_pending_leader = True
        except TourLeaderProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid(): 
            form.save()
            messages.success(request, "پروفایل بروزرسانی شد.")
            return redirect('dashboard')
    else: 
        form = ProfileUpdateForm(instance=user)
    
    context = {
        'profile_form': form, 
        'reservations': Reservation.objects.filter(user=user).order_by('-created_at'),
        'is_pending_leader': is_pending_leader
    }
    
    if user.role == 'leader': 
        context['leader_tours'] = Tour.objects.filter(leader=user)
        
    return render(request, 'dashboard.html', context)

def login_view(request):
    active_tab = 'login'
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            active_tab = 'login'
            u = request.POST.get('username')
            p = request.POST.get('password')
            user = authenticate(request, username=u, password=p)
            
            if user:
                if user.role == 'leader':
                    try:
                        if hasattr(user, 'leader_profile') and not user.leader_profile.is_verified:
                            return render(request, 'login.html', {
                                'error_login': 'حساب لیدر شما هنوز تایید نشده است.',
                                'active_tab': 'login'
                            })
                    except TourLeaderProfile.DoesNotExist:
                        pass
                
                login(request, user)
                messages.success(request, f"خوش آمدید {user.first_name}")
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {
                    'error_login': 'نام کاربری یا رمز عبور اشتباه است', 
                    'active_tab': 'login'
                })

        elif action == 'register':
            active_tab = 'register'
            u = request.POST.get('username')
            p = request.POST.get('password')
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            
            if User.objects.filter(username=u).exists():
                return render(request, 'login.html', {
                    'error_reg': 'این نام کاربری قبلاً انتخاب شده است.', 
                    'active_tab': 'register'
                })

            try:
                new_user = User.objects.create_user(
                    username=u, 
                    password=p, 
                    first_name=first_name, 
                    phone_number=phone, 
                    role='user'
                )
                
                login(request, new_user)
                messages.success(request, "ثبت نام موفقیت‌آمیز بود.")
                return redirect('dashboard')
                
            except Exception as e:
                return render(request, 'login.html', {
                    'error_reg': f'خطا: {str(e)}', 
                    'active_tab': 'register'
                })

    return render(request, 'login.html', {'active_tab': active_tab})

def logout_view(request):
    logout(request)
    return redirect('index')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=