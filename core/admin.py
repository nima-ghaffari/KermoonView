from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, TourLeaderProfile, Hotel, Tour, Reservation, Post, LeaderReview, Comment, PostComment
from django_jalali.admin.filters import JDateFieldListFilter

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 1. Admin management panel
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    list_editable = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('role', 'phone_number', 'avatar', 'national_id')}),
    )
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 2. management Profile TourLeader 
@admin.register(TourLeaderProfile)
class TourLeaderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience_years', 'is_verified', 'verification_status')
    list_filter = ('is_verified', 'specialty')
    search_fields = ('user__username', 'user__first_name')
    list_editable = ('is_verified',) 
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 'green', '✅ تایید شده')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 'orange', '⏳ در انتظار بررسی')
    verification_status.short_description = "وضعیت رنگی"

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
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'leader', 'price', 'start_date', 'status_badge', 'is_active')
    list_filter = ('is_active', 'category', ('start_date', JDateFieldListFilter))
    search_fields = ('title', 'leader__username', 'location')    
    list_editable = ('is_active',)    
    actions = ['approve_tours', 'reject_tours']

    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: {}; color: {}; padding: 3px 10px; border-radius: 10px;">{}</span>',
                '#def7ec', '#03543f', 'فعال'
            )
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; border-radius: 10px;">{}</span>',
            '#fff3cd', '#856404', ' نیاز به تایید'
        )
    status_badge.short_description = "وضعیت نمایش"

    @admin.action(description=' تایید و انتشار تورهای انتخاب شده')
    def approve_tours(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "تورهای انتخاب شده با موفقیت فعال شدند.")

    @admin.action(description=' عدم تایید (غیرفعال کردن)')
    def reject_tours(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "تورهای انتخاب شده غیرفعال شدند.")
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 5. Reservations management 
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'total_price', 'status', 'status_colored', 'created_at')
    list_filter = ('status', ('created_at', JDateFieldListFilter))
    list_editable = ('status',)

    def status_colored(self, obj):
        colors = {'pending': 'orange', 'confirmed': 'green', 'rejected': 'red'}
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "وضعیت رنگی"
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 6. Tour comment 
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', ('created_at', JDateFieldListFilter))
    list_editable = ('is_approved',)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 7. TourLeader (TL) comment
@admin.register(LeaderReview)
class LeaderReviewAdmin(admin.ModelAdmin):
    list_display = ('leader', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    list_editable = ('is_approved',)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 8. Post set in home page . 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', ('created_at', JDateFieldListFilter))
    prepopulated_fields = {'slug': ('title',)} 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 9. Post comment in home page management . 
@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=