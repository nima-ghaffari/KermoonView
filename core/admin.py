from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TourLeaderProfile, Hotel, Tour, Reservation, Post, LeaderReview, Comment, PostComment


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 1. Admin management panel
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('role', 'phone_number', 'avatar', 'national_id')}),
    )
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 2. management Profile TourLeader 
@admin.register(TourLeaderProfile)
class TourLeaderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience_years', 'is_verified')
    list_filter = ('is_verified', 'specialty')
    search_fields = ('user__username', 'user__first_name')
    list_editable = ('is_verified',) # امکان تایید سریع در لیست با یک تیک
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'is_verified')
        }),
        ('اطلاعات حرفه‌ای', {
            'fields': ('specialty', 'experience_years', 'languages')
        }),
        ('اطلاعات ثبت نامی (بررسی شود)', {
            'fields': ('motivation', 'documents', 'bio')
        }),
    )
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 3. Hotel sets 
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'is_approved')
    list_filter = ('is_approved',)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 4. Tour management 

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
