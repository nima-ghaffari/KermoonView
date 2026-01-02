// --- Mock Database: Tour Guides ---
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
        upcomingTours: [],
        pastTours: [],
        reviews: []
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
        upcomingTours: [],
        pastTours: [],
        reviews: []
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('guides-container');
    if (container) {
        renderGuidesList(guidesData);
    }
});

function renderGuidesList(guides) {
    const container = document.getElementById('guides-container');
    container.innerHTML = '';

    if (guides.length === 0) {
        document.getElementById('no-results').style.display = 'block';
        return;
    } else {
        document.getElementById('no-results').style.display = 'none';
    }

    guides.forEach((guide, index) => {
        const cardHTML = `
            <div class="soft-card" style="opacity:0; animation: fadeInUp 0.5s ease forwards ${index * 0.1}s">
                <div class="soft-card-image">
                    <img src="${guide.image}" alt="${guide.name}">
                    <span class="soft-category">${guide.specialty}</span>
                </div>
                
                <div class="soft-card-content">
                    <div class="soft-card-header">
                        <h3 class="soft-title">${guide.name}</h3>
                        <span class="soft-tag-blue">${guide.experience} سال سابقه</span>
                    </div>
                    
                    <ul class="soft-info-list">
                        <li><i class="fas fa-map-marker-alt"></i> ${guide.location}</li>
                        <li><i class="fas fa-language"></i> ${guide.languages}</li>
                        <li><i class="fas fa-star" style="color:#f6ad55"></i> ${guide.rating} (رضایت بالا)</li>
                    </ul>
                    
                    <div class="soft-actions">
                        <a href="guide-details.html?id=${guide.id}" class="btn-outline-soft">بیوگرافی</a>
                        <a href="guide-details.html?id=${guide.id}" class="btn-fill-soft">مشاهده پروفایل</a>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += cardHTML;
    });
}

function filterGuides() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    
    const filtered = guidesData.filter(guide => {
        return guide.name.toLowerCase().includes(query) || 
               guide.specialty.toLowerCase().includes(query) ||
               guide.location.toLowerCase().includes(query);
    });
    
    renderGuidesList(filtered);
}

const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path.includes('guides.html')) renderGuidesList(guidesData);
    if (path.includes('guide-details.html')) loadGuideProfile();
});

function loadGuideProfile() {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get('id'));
    const guide = guidesData.find(g => g.id === id);

    if (!guide) {
        document.querySelector('.guide-profile-layout').innerHTML = '<div style="text-align:center; padding:50px;"><h2>لیدر یافت نشد</h2><a href="guides.html">بازگشت</a></div>';
        return;
    }

    document.getElementById('g-avatar').src = guide.avatar;
    document.getElementById('g-name').innerText = guide.name;
    document.getElementById('g-specialty').innerText = guide.specialty;
    document.getElementById('g-rating').innerText = guide.rating;
    document.getElementById('g-exp').innerText = guide.experience;
    document.getElementById('g-tours-count').innerText = guide.toursCount;
    document.getElementById('g-lang').innerText = guide.languages;
    document.getElementById('g-area').innerText = guide.location; 
    document.getElementById('g-bio').innerText = guide.bio;

    const upcomingContainer = document.getElementById('upcoming-tours-list');
    upcomingContainer.innerHTML = '';
    
    if (guide.upcomingTours && guide.upcomingTours.length > 0) {
        guide.upcomingTours.forEach(tour => {
            upcomingContainer.innerHTML += `
                <div class="mini-tour-item">
                    <img src="${tour.image}" class="mini-tour-img">
                    <div class="mini-tour-body">
                        <span class="mini-tour-title">${tour.title}</span>
                        <span class="mini-tour-date"><i class="far fa-calendar"></i> ${tour.date}</span>
                        <!-- لینک مستقیم به صفحه رزرو تور -->
                        <a href="tour-details.html?id=${tour.id}" class="btn-mini-action">مشاهده و رزرو</a>
                    </div>
                </div>
            `;
        });
    } else {
        upcomingContainer.innerHTML = '<p style="color:#a0aec0; text-align:center; grid-column:1/-1;">در حال حاضر توری تعریف نشده است.</p>';
    }

    const pastContainer = document.getElementById('past-tours-list');
    pastContainer.innerHTML = '';
    
    if (guide.pastTours && guide.pastTours.length > 0) {
        guide.pastTours.forEach(tour => {
            pastContainer.innerHTML += `
                <div class="timeline-row">
                    <span class="tl-date">${tour.date}</span>
                    <span class="tl-title">${tour.title}</span>
                    <span class="tl-loc"><i class="fas fa-map-marker-alt"></i> ${tour.location}</span>
                </div>
            `;
        });
    } else {
        pastContainer.innerHTML = '<p>اطلاعاتی ثبت نشده است.</p>';
    }

    const reviewsContainer = document.getElementById('guide-reviews');
    reviewsContainer.innerHTML = '';
    
    if (guide.reviews && guide.reviews.length > 0) {
        guide.reviews.forEach(review => {
            let stars = '';
            for(let i=1; i<=5; i++) stars += (i<=review.rating) ? '<i class="fas fa-star" style="color:#f6ad55"></i>' : '<i class="far fa-star" style="color:#ddd"></i>';
            
            reviewsContainer.innerHTML += `
                <div class="guide-review-item">
                    <div class="g-review-header">
                        <span class="g-reviewer-name">${review.user}</span>
                        <div>${stars}</div>
                    </div>
                    <p class="g-review-text">${review.text}</p>
                </div>
            `;
        });
    } else {
        reviewsContainer.innerHTML = '<p style="color:#a0aec0">هنوز نظری ثبت نشده است.</p>';
    }
}
