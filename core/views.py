from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from django.contrib import messages

from .models import (
    Tour, Reservation, TourLeaderProfile, 
    Post, PostComment, Comment, LeaderReview, User)

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
#