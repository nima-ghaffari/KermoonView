const toursDetailsData = [
    {
        id: 1,
        title: "تور ارگ تاریخی بم",
        price: 500000,
        image: "https://media.kojaro.com/2020/9/f4850785-525d-4f10-9b30-33b092a7927d.jpg",
        duration: "۱ روزه",
        location: "بم، کرمان",
        category: "تاریخی",
        desc: "سفری شگفت‌انگیز به بزرگترین بنای خشتی جهان. در این تور یک روزه، شما از ارگ قدیم بم که پس از زلزله بازسازی شده دیدن می‌کنید.",
        features: ["راهنمای تخصصی", "ناهار محلی", "ترانسفر VIP", "بیمه مسافرتی"],
        availableDates: [
            "۱۴۰۳/۱۰/۱۵ - جمعه (ظرفیت محدود)",
            "۱۴۰۳/۱۰/۲۲ - جمعه",
            "۱۴۰۳/۱۰/۲۹ - جمعه"
        ],
        reviews: [
            { user: "علی رضایی", date: "۱۴۰۳/۱۰/۰۲", rating: 5, text: "واقعاً عالی بود." },
            { user: "سارا", date: "۱۴۰۳/۰۹/۱۵", rating: 4, text: "ارگ بم خیلی باشکوهه." }
        ]
    },
    {
        id: 2,
        title: "گهر پارک سیرجان",
        price: 850000,
        image: "https://api2.kojaro.com/media/2024-1-7b801bb2-4f4a-45f2-8260-15266189e49c-67c46117c1067c5ba7689a14?w=1200&q=80",
        duration: "۲ روزه",
        location: "سیرجان",
        category: "طبیعت گردی",
        desc: "بازدید از مدرن‌ترین پارک گردشگری منطقه. شب مانی در کمپ‌های مجهز زیر آسمان پرستاره کویر.",
        features: ["اقامت در کمپ", "۳ وعده غذا", "راهنمای طبیعت", "عکاسی شبانه"],
        availableDates: [
            "۱۴۰۳/۱۰/۱۲ - چهارشنبه",
            "۱۴۰۳/۱۰/۲۶ - چهارشنبه"
        ],
        reviews: [
            { user: "نیما", date: "۱۴۰۳/۰۹/۱۰", rating: 5, text: "شب مانی توی کمپ خیلی هیجان انگیز بود." }
        ]
    },
    {
        id: 3,
        title: "باغ شاهزاده ماهان",
        price: 350000,
        image: "https://images.kojaro.com/2016/2/b9f9392e-b153-488f-9a13-43c33367d383.jpg",
        duration: "نیم روزه",
        location: "ماهان",
        category: "فرهنگی",
        desc: "نگینی سبز در دل کویر. باغ شاهزاده ماهان یکی از زیباترین باغ‌های ایرانی است که در فهرست میراث جهانی یونسکو ثبت شده است.",
        features: ["عصرانه سنتی", "ورودی باغ", "راهنمای محلی"],
        availableDates: [
            "۱۴۰۳/۱۰/۱۴ - پنجشنبه",
            "۱۴۰۳/۱۰/۱۵ - جمعه",
            "۱۴۰۳/۱۰/۲۱ - پنجشنبه"
        ],
        reviews: [
            { user: "فرزاد", date: "۱۴۰۳/۱۰/۰۵", rating: 5, text: "باغ شاهزاده تو پاییز محشره." }
        ]
    },
    {
        id: 4,
        title: "کمپ کویر لوت (کلوت‌ها)",
        price: 1200000,
        image: "https://core.orienttrips.com/storage//image/city-gallery/1-Kerman-Iran.jpg",
        duration: "۲ روز و ۱ شب",
        location: "شهداد",
        category: "ماجراجویی",
        desc: "سفر به گرم‌ترین نقطه زمین! تماشای کلوت‌های جادویی شهداد در هنگام طلوع و غروب خورشید.",
        features: ["کمپ شبانه", "سافاری 4x4", "ستاره نگری", "شام آتیشی"],
        availableDates: [
            "۱۴۰۳/۱۱/۰۱ - دوشنبه",
            "۱۴۰۳/۱۱/۰۵ - جمعه"
        ],
        reviews: [
            { user: "کامران", date: "۱۴۰۳/۰۹/۰۱", rating: 5, text: "سکوت کویر در شب رو هیچ جا نمیشه تجربه کرد." }
        ]
    },
    {
        id: 5,
        title: "روستای صخره‌ای میمند",
        price: 600000,
        image: "https://media.isna.ir/content/1444122971556_Ali+Abouali-21.jpg/2",
        duration: "۱ روزه",
        location: "شهربابک",
        category: "تاریخی",
        desc: "سفر به هزاران سال قبل. میمند روستایی دستکند در دل کوه است که مردمانش هنوز با آداب و رسوم کهن در آن زندگی می‌کنند.",
        features: ["صبحانه محلی", "بازدید از آتشکده", "خرید سوغات"],
        availableDates: [
            "۱۴۰۳/۱۰/۲۰ - پنجشنبه"
        ],
        reviews: []
    }
];

let currentTour = null;

document.addEventListener('DOMContentLoaded', () => {
    loadPageData();
});

function loadPageData() {
    const params = new URLSearchParams(window.location.search);
    const tourId = parseInt(params.get('id'));

    currentTour = toursDetailsData.find(t => t.id === tourId);

    if (!currentTour) {
        document.body.innerHTML = '<div style="text-align:center; padding:50px;"><h2>تور مورد نظر یافت نشد!</h2><a href="tours.html">بازگشت</a></div>';
        return;
    }

    document.getElementById('detail-image').src = currentTour.image;
    document.getElementById('detail-title').innerText = currentTour.title;
    document.getElementById('detail-location').innerText = currentTour.location;
    document.getElementById('detail-duration').innerText = currentTour.duration;
    document.getElementById('detail-desc').innerText = currentTour.desc;
    document.getElementById('detail-category').innerText = currentTour.category;
    document.getElementById('detail-price').innerText = currentTour.price.toLocaleString('fa-IR');

    const featuresList = document.getElementById('detail-features');
    featuresList.innerHTML = '';
    currentTour.features.forEach(f => {
        featuresList.innerHTML += `<li><i class="fas fa-check-circle"></i> ${f}</li>`;
    });

    const dateSelect = document.getElementById('book-date');
    dateSelect.innerHTML = '<option value="" disabled selected>انتخاب تاریخ حرکت...</option>'; // ریست کردن
    
    if(currentTour.availableDates && currentTour.availableDates.length > 0) {
        currentTour.availableDates.forEach(date => {
            const option = document.createElement('option');
            option.value = date;
            option.text = date;
            dateSelect.appendChild(option);
        });
    } else {
        const option = document.createElement('option');
        option.text = "فعلا تاریخی موجود نیست";
        option.disabled = true;
        dateSelect.appendChild(option);
    }

    renderReviews(currentTour.reviews);
}

function renderReviews(reviews) {
    const container = document.getElementById('reviews-list');
    const ratingAvg = document.getElementById('detail-rating-avg');
    container.innerHTML = '';

    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p style="color:#718096">هنوز نظری برای این تور ثبت نشده است.</p>';
        ratingAvg.innerText = 'جدید';
        return;
    }

    let totalRating = 0;
    
    reviews.forEach(review => {
        totalRating += review.rating;
        
        let starsHTML = '';
        for (let i = 1; i <= 5; i++) {
            starsHTML += (i <= review.rating) ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
        }

        const initial = review.user.charAt(0);

        const card = `
            <div class="review-card">
                <div class="review-header">
                    <div class="user-info">
                        <div class="user-avatar">${initial}</div>
                        <div class="user-details">
                            <h4>${review.user}</h4>
                            <span class="review-date">${review.date}</span>
                        </div>
                    </div>
                    <div class="review-rating">${starsHTML}</div>
                </div>
                <div class="review-text">${review.text}</div>
            </div>
        `;
        container.innerHTML += card;
    });

    const avg = (totalRating / reviews.length).toFixed(1);
    ratingAvg.innerText = avg + ` (${reviews.length.toLocaleString('fa-IR')} نظر)`;
}

function updateTotalPrice() {
    if (!currentTour) return;

    const count = parseInt(document.getElementById('book-count').value) || 1;
    const total = count * currentTour.price;

    const calcBox = document.getElementById('price-calc-box');
    const mathSpan = document.getElementById('calc-math');
    const totalSpan = document.getElementById('calc-total');

    if (count > 0) {
        calcBox.style.display = 'flex';
        mathSpan.innerHTML = `${currentTour.price.toLocaleString('fa-IR')} × ${count.toLocaleString('fa-IR')} نفر`;
        totalSpan.innerHTML = `${total.toLocaleString('fa-IR')} تومان`;
    }
}

function handleSidebarBooking(e) {
    e.preventDefault();

    if (typeof isUserLoggedIn === 'function' && !isUserLoggedIn()) {
        showToast('خطای دسترسی', 'برای تکمیل رزرو باید وارد حساب شوید', 'error');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    const dateSelect = document.getElementById('book-date');
    const selectedDate = dateSelect.value;
    
    if (!selectedDate) {
        showToast('تاریخ نامعتبر', 'لطفا یکی از تاریخ‌های موجود را انتخاب کنید', 'error');
        return;
    }

    const btn = e.target.querySelector('button');
    const originalText = btn.innerText;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال اتصال به درگاه...';
    btn.disabled = true;

    setTimeout(() => {
        showToast('انتقال به درگاه', 'در حال انتقال به صفحه پرداخت بانک...', 'success');
        setTimeout(() => {
             btn.innerHTML = originalText;
             btn.disabled = false;
        }, 2000);
    }, 1500);
}
function showToast(title, message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    let iconClass = 'fa-check-circle';
    if (type === 'error') iconClass = 'fa-times-circle';
    if (type === 'info') iconClass = 'fa-info-circle';

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${iconClass}"></i>
        <div class="toast-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOutToast 0.5s forwards';
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 500);
    }, 3500);
}