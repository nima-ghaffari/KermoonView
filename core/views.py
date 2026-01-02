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
#