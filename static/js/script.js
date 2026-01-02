
const toursData = [
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
        availableDates: ["۱۴۰۳/۱۰/۱۵ - جمعه", "۱۴۰۳/۱۰/۲۲ - جمعه"],
        reviews: [{ user: "علی", date: "۱۴۰۳/۱۰/۰۲", rating: 5, text: "عالی بود." }]
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
        availableDates: ["۱۴۰۳/۱۰/۱۲ - چهارشنبه"],
        reviews: [{ user: "نیما", date: "۱۴۰۳/۰۹/۱۰", rating: 5, text: "خیلی هیجان انگیز بود." }]
    },
    { 
        id: 3, 
        title: "باغ شاهزاده ماهان", 
        price: 350000, 
        image: "https://images.kojaro.com/2016/2/b9f9392e-b153-488f-9a13-43c33367d383.jpg", 
        duration: "نیم روزه", 
        location: "ماهان", 
        category: "فرهنگی",
        desc: "نگینی سبز در دل کویر. باغ شاهزاده ماهان یکی از زیباترین باغ‌های ایرانی است.",
        features: ["عصرانه سنتی", "ورودی باغ", "راهنمای محلی"],
        availableDates: ["۱۴۰۳/۱۰/۱۴ - پنجشنبه"],
        reviews: [{ user: "فرزاد", date: "۱۴۰۳/۱۰/۰۵", rating: 5, text: "بسیار زیبا." }]
    },
    { 
        id: 4, 
        title: "کمپ کویر لوت", 
        price: 1200000, 
        image: "https://core.orienttrips.com/storage//image/city-gallery/1-Kerman-Iran.jpg", 
        duration: "۲ روز و ۱ شب", 
        location: "شهداد", 
        category: "ماجراجویی",
        desc: "سفر به گرم‌ترین نقطه زمین! تماشای کلوت‌های جادویی شهداد در هنگام طلوع و غروب خورشید.",
        features: ["کمپ شبانه", "سافاری 4x4", "ستاره نگری", "شام آتیشی"],
        availableDates: ["۱۴۰۳/۱۱/۰۱ - دوشنبه"],
        reviews: [{ user: "کامران", date: "۱۴۰۳/۰۹/۰۱", rating: 5, text: "سکوت کویر عالی بود." }]
    }
];

const guidesData = [
    { 
        id: 101, 
        name: "محمد کریمی", 
        image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?fit=crop&w=600&h=400", 
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?fit=crop&w=200&h=200", 
        specialty: "طبیعت‌گردی", 
        rating: 4.9, 
        experience: 8, 
        toursCount: 145, 
        location: "کرمان، شهداد", 
        languages: "فارسی، انگلیسی", 
        bio: "عاشق کویر و ستاره‌شناسی هستم. ۸ سال است که به صورت تخصصی در منطقه کلوت‌های شهداد فعالیت می‌کنم.",
        upcomingTours: [
            { id: 4, title: "کمپ کویر لوت", date: "۱۴۰۳/۱۱/۰۱", image: "https://core.orienttrips.com/storage//image/city-gallery/1-Kerman-Iran.jpg" }
        ],
        pastTours: [
            { title: "سافاری شهداد", date: "پاییز ۱۴۰۳", location: "شهداد" }
        ],
        reviews: [{ user: "کامران", rating: 5, text: "کاربلد و حرفه‌ای." }]
    },
    { 
        id: 102, 
        name: "سارا احمدی", 
        image: "https://images.unsplash.com/photo-1494790108755-2616b612b5bc?fit=crop&w=600&h=400", 
        avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b5bc?fit=crop&w=200&h=200", 
        specialty: "تاریخی", 
        rating: 4.8, 
        experience: 5, 
        toursCount: 89, 
        location: "بم، ماهان", 
        languages: "فارسی، فرانسه", 
        bio: "کارشناس ارشد باستان‌شناسی. علاقه من به تاریخ کرمان باعث شد وارد حرفه تورلیدری شوم.",
        upcomingTours: [
            { id: 1, title: "تور ارگ تاریخی بم", date: "۱۴۰۳/۱۰/۲۲", image: "https://media.kojaro.com/2020/9/f4850785-525d-4f10-9b30-33b092a7927d.jpg" }
        ],
        pastTours: [{ title: "بازدید بازار کرمان", date: "آذر ۱۴۰۳", location: "کرمان" }],
        reviews: [{ user: "زهرا", rating: 4, text: "خیلی خوش برخورد." }]
    }
];




document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    updateAuthButton();

    initScrollAnimations();

    if (path.includes('login.html')) {
        setupLoginTabs();
        const loginForm = document.getElementById('login-form');
        if(loginForm) loginForm.onsubmit = handleLogin;
        const regForm = document.getElementById('register-form');
        if(regForm) regForm.onsubmit = handleRegister;
    }

    if (path.includes('dashboard.html')) {
        setupDashboard();
    }

    if (path.includes('tours.html')) {
        renderTours(toursData);
    }
    
    if (path.includes('guides.html')) {
        renderGuidesList(guidesData);
    }

    if (path.includes('guide-details.html')) {
        loadGuideProfile();
    }

    if (path.includes('tour-details.html')) {
        loadTourDetailsPage();
    }
});



const mobileMenuBtn = document.querySelector('.mobile-menu');
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function() {
        const mobileNav = document.querySelector('.nav-mobile');
        mobileNav.classList.toggle('active');
        
        const icon = this.querySelector('i');
        if(icon) {
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        }
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if(href === '#' || href.length < 2) return; 
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Close mobile menu if open
            const mobileNav = document.querySelector('.nav-mobile');
            if (mobileNav && mobileNav.classList.contains('active')) {
                mobileNav.classList.remove('active');
                const icon = document.querySelector('.mobile-menu i');
                if(icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        }
    });
});

window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (header) {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
            header.style.backdropFilter = 'blur(10px)';
        }
    }
});

const statsSection = document.querySelector('.stats');
if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    });
    observer.observe(statsSection);
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-item h3');
    counters.forEach(counter => {
        const rawText = counter.textContent;
        const target = parseInt(rawText.replace(/\D/g, '')); 
        const suffix = rawText.replace(/[0-9]/g, '');
        
        if(isNaN(target)) return;

        let current = 0;
        const increment = target / 50; 
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target + suffix; 
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current) + suffix;
            }
        }, 30);
    });
}

function initScrollAnimations() {
    if(!document.getElementById('anim-style')) {
        const style = document.createElement('style');
        style.id = 'anim-style';
        style.innerHTML = `@keyframes fadeInUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }`;
        document.head.appendChild(style);
    }

    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                cardObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const cards = document.querySelectorAll('.feature-card, .package-card, .testimonial-card, .blog-card, .soft-card, .guide-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s cubic-bezier(0.5, 0, 0, 1) ${index % 3 * 0.1}s`;
        cardObserver.observe(card);
    });
}



function isUserLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

function updateAuthButton() {
    if (isUserLoggedIn()) {
        const authBtns = document.querySelectorAll('.auth-buttons .cta-button, .nav-mobile a[href="login.html"]');
        const role = localStorage.getItem('userRole');
        const name = localStorage.getItem('userName');
        const displayName = name ? name.split(' ')[0] : 'کاربر';
        
        authBtns.forEach(btn => {
            btn.innerHTML = `<i class="fas fa-user-circle"></i> ${displayName}`; 
            btn.href = 'dashboard.html';
            
            if(btn.classList.contains('cta-button')) {
                btn.style.background = role === 'leader' ? '#2d3748' : '#48bb78';
            } else {
                btn.style.color = '#48bb78';
            }
        });
    }
}

function selectRole(role) {
    const btns = document.querySelectorAll('.role-btn');
    const roleInput = document.getElementById('reg-role');
    const leaderFields = document.getElementById('leader-code-group');

    btns.forEach(btn => btn.classList.remove('active'));
    if(event && event.currentTarget) event.currentTarget.classList.add('active');

    if(roleInput) roleInput.value = role;

    if (role === 'leader') {
        if(leaderFields) leaderFields.style.display = 'block';
    } else {
        if(leaderFields) leaderFields.style.display = 'none';
    }
}

function handleRegister(event) {
    event.preventDefault();
    const btn = event.target.querySelector('.submit-btn');
    const name = document.getElementById('reg-name').value;
    const role = document.getElementById('reg-role').value;
    
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال ثبت نام...';
    btn.disabled = true;

    setTimeout(() => {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userRole', role);
        localStorage.setItem('userName', name);

        showToast('ثبت نام موفق', `خوش آمدید ${name}!`, 'success');
        setTimeout(() => window.location.href = 'dashboard.html', 1500);
    }, 1500);
}

function handleLogin(event) {
    event.preventDefault();
    const btn = event.target.querySelector('.submit-btn');
    const originalText = btn.innerText;
    const email = document.getElementById('login-email').value.trim();
    const pass = document.getElementById('login-password').value;

    btn.innerHTML = '...';
    btn.disabled = true;

    setTimeout(() => {
        let role = '', name = '';
        if (email === 'leader@test.com' && pass === '1234') {
            role = 'leader'; name = 'محمد کریمی';
        } else if (email === 'user@test.com' && pass === '1234') {
            role = 'user'; name = 'نیما غفاری';
        } else {
            showToast('خطا', 'اطلاعات اشتباه است', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }

        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userRole', role);
        localStorage.setItem('userName', name);
        window.location.href = 'dashboard.html';
    }, 1000);
}

function logout() {
    if(confirm("خروج از حساب؟")) {
        localStorage.clear();
        window.location.href = 'index.html';
    }
}

function setupLoginTabs() {
    const tabs = document.querySelectorAll('.auth-tab');
    const sections = document.querySelectorAll('.auth-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            tab.classList.add('active');
            const targetId = tab.dataset.target;
            if(document.getElementById(targetId)) {
                document.getElementById(targetId).classList.add('active');
            }
        });
    });
}



function renderTours(tours) {
    const container = document.getElementById('tours-container');
    if (!container) return;
    container.innerHTML = '';
    
    if(!tours || tours.length === 0) {
        const noRes = document.getElementById('no-results');
        if(noRes) noRes.style.display = 'block';
        return;
    } else {
        const noRes = document.getElementById('no-results');
        if(noRes) noRes.style.display = 'none';
    }

    tours.forEach((tour, index) => {
        container.innerHTML += `
            <div class="soft-card" style="animation: fadeInUp 0.5s ease forwards ${index * 0.1}s">
                <div class="soft-card-image"><img src="${tour.image}"><span class="soft-category">${tour.category}</span></div>
                <div class="soft-card-content">
                    <div class="soft-card-header"><h3 class="soft-title">${tour.title}</h3><span class="soft-tag-blue">${(tour.price/1000).toLocaleString()} ت</span></div>
                    <ul class="soft-info-list"><li><i class="fas fa-map-marker-alt"></i> ${tour.location}</li></ul>
                    <div class="soft-actions">
                        <a href="tour-details.html?id=${tour.id}" class="btn-outline-soft">جزئیات</a>
                        <a href="tour-details.html?id=${tour.id}" class="btn-fill-soft">رزرو</a>
                    </div>
                </div>
            </div>`;
    });
}

function filterTours() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = toursData.filter(t => t.title.includes(query) || t.location.includes(query));
    renderTours(filtered);
}

function renderGuidesList(guides) {
    const container = document.getElementById('guides-container');
    if (!container) return;
    container.innerHTML = '';
    
    if(!guides || guides.length === 0) {
        const noRes = document.getElementById('no-results');
        if(noRes) noRes.style.display = 'block';
        return;
    } else {
        const noRes = document.getElementById('no-results');
        if(noRes) noRes.style.display = 'none';
    }

    guides.forEach((guide, index) => {
        container.innerHTML += `
            <div class="soft-card" style="animation: fadeInUp 0.5s ease forwards ${index * 0.1}s">
                <div class="soft-card-image"><img src="${guide.image}"><span class="soft-category">${guide.specialty}</span></div>
                <div class="soft-card-content">
                    <div class="soft-card-header"><h3 class="soft-title">${guide.name}</h3><span class="soft-tag-blue">${guide.experience} سال</span></div>
                    <ul class="soft-info-list"><li><i class="fas fa-map-marker-alt"></i> ${guide.location}</li></ul>
                    <div class="soft-actions">
                        <a href="guide-details.html?id=${guide.id}" class="btn-outline-soft">بیوگرافی</a>
                        <a href="guide-details.html?id=${guide.id}" class="btn-fill-soft">مشاهده</a>
                    </div>
                </div>
            </div>`;
    });
}

function filterGuides() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = guidesData.filter(g => g.name.includes(query) || g.location.includes(query));
    renderGuidesList(filtered);
}

function loadGuideProfile() {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get('id'));
    const guide = guidesData.find(g => g.id === id);
    if (!guide) return;

    const ids = { 'g-name': guide.name, 'g-specialty': guide.specialty, 'g-rating': guide.rating, 'g-exp': guide.experience, 'g-tours-count': guide.toursCount, 'g-lang': guide.languages, 'g-area': guide.location, 'g-bio': guide.bio };
    for (const [key, val] of Object.entries(ids)) { if(document.getElementById(key)) document.getElementById(key).innerText = val; }
    if(document.getElementById('g-avatar')) document.getElementById('g-avatar').src = guide.avatar;
    
    const upcomingContainer = document.getElementById('upcoming-tours-list');
    if(upcomingContainer) {
        upcomingContainer.innerHTML = '';
        if(guide.upcomingTours.length > 0) {
            guide.upcomingTours.forEach(t => {
                upcomingContainer.innerHTML += `<div class="mini-tour-item"><img src="${t.image}" class="mini-tour-img"><div class="mini-tour-body"><span class="mini-tour-title">${t.title}</span><a href="tour-details.html?id=${t.id}" class="btn-mini-action">رزرو</a></div></div>`;
            });
        } else {
            upcomingContainer.innerHTML = '<p style="color:#718096">توری موجود نیست.</p>';
        }
    }
    const reviewsContainer = document.getElementById('guide-reviews');
    if(reviewsContainer && guide.reviews) {
        reviewsContainer.innerHTML = '';
        guide.reviews.forEach(r => {
            reviewsContainer.innerHTML += `<div class="guide-review-item" style="background:#f9fafb; padding:15px; border-radius:10px; margin-bottom:10px;"><strong>${r.user}</strong> <span style="color:#f6ad55">★ ${r.rating}</span><p>${r.text}</p></div>`;
        });
    }
}

let currentTourPage = null;
function loadTourDetailsPage() {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get('id'));
    const tour = toursData.find(t => t.id === id);
    currentTourPage = tour;
    if(!tour) return;

    if(document.getElementById('detail-image')) document.getElementById('detail-image').src = tour.image;
    const ids = { 'detail-title': tour.title, 'detail-location': tour.location, 'detail-duration': tour.duration, 'detail-desc': tour.desc, 'detail-category': tour.category, 'detail-price': tour.price.toLocaleString() };
    for (const [key, val] of Object.entries(ids)) { if(document.getElementById(key)) document.getElementById(key).innerText = val; }

    const featuresList = document.getElementById('detail-features');
    if(featuresList) {
        featuresList.innerHTML = '';
        tour.features.forEach(f => featuresList.innerHTML += `<li><i class="fas fa-check-circle"></i> ${f}</li>`);
    }

    const dateSelect = document.getElementById('book-date');
    if(dateSelect && tour.availableDates) {
        dateSelect.innerHTML = '<option value="" disabled selected>انتخاب تاریخ...</option>';
        tour.availableDates.forEach(d => {
            const opt = document.createElement('option'); opt.value = d; opt.text = d; dateSelect.appendChild(opt);
        });
    }
    
    const reviewsContainer = document.getElementById('reviews-list');
    if(reviewsContainer && tour.reviews) {
        reviewsContainer.innerHTML = '';
        tour.reviews.forEach(r => {
            reviewsContainer.innerHTML += `<div class="review-card" style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;"><strong>${r.user}</strong> <span style="color:#f6ad55">★ ${r.rating}</span><p>${r.text}</p></div>`;
        });
    }
}



function setupDashboard() {
    if (!isUserLoggedIn()) { window.location.href = 'login.html'; return; }
    const role = localStorage.getItem('userRole');
    const name = localStorage.getItem('userName');
    
    if(document.getElementById('dash-name')) document.getElementById('dash-name').innerText = name;
    
    if (role === 'leader') {
        if(document.getElementById('dash-role')) {
            document.getElementById('dash-role').innerText = 'تورلیدر تایید شده';
            document.getElementById('dash-role').style.background = '#ebf8ff';
            document.getElementById('dash-role').style.color = '#2b6cb0';
        }
    } else {
        if(document.getElementById('dash-role')) {
            document.getElementById('dash-role').innerText = 'گردشگر عادی';
            document.getElementById('dash-role').style.background = '#f0fff4';
            document.getElementById('dash-role').style.color = '#2f855a';
        }
        document.querySelectorAll('.leader-only').forEach(el => el.style.display = 'none');
        if(document.getElementById('create-tour')) document.getElementById('create-tour').remove();
        if(document.getElementById('manage-users')) document.getElementById('manage-users').remove();
    }
}

function switchTab(id) {
    document.querySelectorAll('.dash-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.dash-menu li').forEach(el => el.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    if(event) event.currentTarget.classList.add('active');
}

function updateTotalPrice() {
    if (!currentTourPage) return;
    const count = parseInt(document.getElementById('book-count').value) || 1;
    const total = count * currentTourPage.price;
    const calcBox = document.getElementById('price-calc-box');
    if(calcBox && count > 0) {
        calcBox.style.display = 'flex';
        if(document.getElementById('calc-math')) document.getElementById('calc-math').innerText = `${currentTourPage.price.toLocaleString()} × ${count}`;
        if(document.getElementById('calc-total')) document.getElementById('calc-total').innerText = `${total.toLocaleString()} تومان`;
    }
}

function handleSidebarBooking(e) {
    e.preventDefault();
    if (!isUserLoggedIn()) {
        showToast('خطا', 'ابتدا وارد شوید', 'error');
        setTimeout(() => window.location.href = 'login.html', 1500);
        return;
    }
    const btn = e.target.querySelector('button');
    btn.innerHTML = 'در حال پردازش...';
    btn.disabled = true;
    setTimeout(() => {
        showToast('موفق', 'انتقال به درگاه...', 'success');
        setTimeout(() => { btn.innerHTML = 'رزرو آنلاین'; btn.disabled = false; }, 2000);
    }, 1500);
}

function openBookingPopup(packageName = '') {
    const overlay = document.getElementById('bookingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
        const input = document.getElementById('package');
        if(input) input.value = packageName;
    }
}

function closeBookingPopup() {
    const overlay = document.getElementById('bookingOverlay');
    if (overlay) overlay.style.display = 'none';
}

function checkLoginAndBook(packageName) {
    if (isUserLoggedIn()) {
        if (!window.location.pathname.includes('tour-details.html')) {
            openBookingPopup(packageName);
        }
    } else {
        showToast('خطا', 'ابتدا وارد شوید', 'error');
        setTimeout(() => window.location.href = 'login.html', 1500);
    }
}

function handleBookingSubmit(event) {
    event.preventDefault();
    const btn = event.target.querySelector('.submit-btn');
    btn.innerHTML = '...';
    setTimeout(() => {
        showToast('موفق', 'رزرو ثبت شد', 'success');
        closeBookingPopup();
        btn.innerHTML = 'تایید';
    }, 2000);
}

const bookingOverlay = document.getElementById('bookingOverlay');
if(bookingOverlay) {
    bookingOverlay.addEventListener('click', (e) => {
        if(e.target === bookingOverlay) closeBookingPopup();
    });
}



function showToast(title, msg, type) {
    const box = document.createElement('div');
    box.className = `toast ${type}`;
    box.style.cssText = `position:fixed; top:20px; right:20px; background:#fff; padding:15px; border-radius:10px; box-shadow:0 5px 20px rgba(0,0,0,0.2); border-right:5px solid ${type==='success'?'#48bb78':'#f56565'}; z-index:99999; min-width:300px; display:flex; flex-direction:column; gap:5px; animation: slideIn 0.3s forwards;`;
    
    box.innerHTML = `<strong style="font-size:1rem; color:#333;">${title}</strong><p style="margin:0; font-size:0.9rem; color:#666;">${msg}</p>`;
    
    document.body.appendChild(box);
    
    const style = document.createElement('style');
    style.innerHTML = `@keyframes slideIn { from { transform: translateX(100%); opacity:0; } to { transform: translateX(0); opacity:1; } }`;
    document.head.appendChild(style);

    setTimeout(() => {
        box.style.opacity = '0';
        box.style.transform = 'translateX(100%)';
        box.style.transition = 'all 0.5s';
        setTimeout(() => box.remove(), 500);
    }, 3000);
}