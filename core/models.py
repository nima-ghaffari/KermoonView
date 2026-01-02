from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'گردشگر'),
        ('leader', 'تور لیدر'),
        ('admin', 'ادمین'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="نقش")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="شماره تماس")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="تصویر پروفایل")
    national_id = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد ملی")

    def __str__(self):
        return self.username

class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام هتل")
    location = models.CharField(max_length=200, verbose_name="آدرس دقیق")
    capacity = models.IntegerField(verbose_name="ظرفیت کل (نفر)")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده توسط ادمین")

    def __str__(self):
        return self.name


class TourLeaderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leader_profile')
    
    specialty = models.CharField(max_length=100, default='نامشخص', verbose_name="تخصص")
    experience_years = models.IntegerField(default=0, verbose_name="سال سابقه")
    languages = models.CharField(max_length=200, default='فارسی', verbose_name="زبان‌ها")
    bio = models.TextField(default='پروفایل جدید', verbose_name="درباره من")
    
    motivation = models.TextField(verbose_name="انگیزه فعالیت", blank=True, null=True)
    documents = models.FileField(upload_to='leader_docs/', verbose_name="فایل مدارک و رزومه", blank=True, null=True)
    
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده توسط مدیریت")

    def __str__(self):
        return f"پروفایل {self.user.username}"

class Tour(models.Model):
    CATEGORY_CHOICES = (
        ('تاریخی', 'تاریخی'),
        ('طبیعت گردی', 'طبیعت گردی'),
        ('فرهنگی', 'فرهنگی'),
        ('ماجراجویی', 'ماجراجویی'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان تور")
    leader = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'leader'}, verbose_name="تورلیدر")
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="هتل")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت تور")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    duration_text = models.CharField(max_length=50, verbose_name="مدت زمان")
    location = models.CharField(max_length=100, verbose_name="مکان برگزاری")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="دسته بندی")
    description = models.TextField(verbose_name="توضیحات کامل")
    image = models.ImageField(upload_to='tours/', verbose_name="تصویر تور")
    is_active = models.BooleanField(default=False, verbose_name="تایید نهایی ادمین")

    def __str__(self):
        return self.title


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده (صدور بلیط)'),
        ('rejected', 'رد شده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="تور")
    passengers_count = models.PositiveIntegerField(default=1, verbose_name="تعداد مسافر")
    total_price = models.PositiveIntegerField(verbose_name="قیمت کل")
    # تغییر پیش‌فرض به pending و اضافه کردن choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"رزرو {self.tour.title} - {self.user.username}"
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    content = models.TextField(verbose_name="متن کامل")
    image = models.ImageField(upload_to='blog/', verbose_name="تصویر شاخص")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پست وبلاگ"
        verbose_name_plural = "پست‌های وبلاگ"

class Comment(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="تور")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="امتیاز")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class LeaderReview(models.Model):
    leader = models.ForeignKey(TourLeaderProfile, on_delete=models.CASCADE, related_name='reviews', verbose_name="تور لیدر")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر نظر دهنده")
    comment = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="امتیاز")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده توسط ادمین")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="تایید شده")

    class Meta:
        ordering = ['-created_at']