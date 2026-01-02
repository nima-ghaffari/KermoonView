const toursData = [
    {
        id: 1,
        title: "تور ارگ تاریخی بم",
        price: 500000,
        image: "https://media.kojaro.com/2020/9/f4850785-525d-4f10-9b30-33b092a7927d.jpg",
        duration: "۱ روزه",
        location: "بم، کرمان",
        category: "تاریخی"
    },
    {
        id: 2,
        title: "گهر پارک سیرجان",
        price: 850000,
        image: "https://api2.kojaro.com/media/2024-1-7b801bb2-4f4a-45f2-8260-15266189e49c-67c46117c1067c5ba7689a14?w=1200&q=80",
        duration: "۲ روزه",
        location: "سیرجان",
        category: "طبیعت گردی"
    },
    {
        id: 3,
        title: "باغ شاهزاده ماهان",
        price: 350000,
        image: "https://images.kojaro.com/2016/2/b9f9392e-b153-488f-9a13-43c33367d383.jpg",
        duration: "نیم روزه",
        location: "ماهان",
        category: "فرهنگی"
    },
    {
        id: 4,
        title: "کمپ کویر لوت (کلوت‌ها)",
        price: 1200000,
        image: "https://core.orienttrips.com/storage//image/city-gallery/1-Kerman-Iran.jpg",
        duration: "۲ روز و ۱ شب",
        location: "شهداد",
        category: "ماجراجویی"
    },
    {
        id: 5,
        title: "روستای صخره‌ای میمند",
        price: 600000,
        image: "https://media.isna.ir/content/1444122971556_Ali+Abouali-21.jpg/2",
        duration: "۱ روزه",
        location: "شهربابک",
        category: "تاریخی"
    }
];

document.addEventListener('DOMContentLoaded', () => {
    renderTours(toursData);
});

function renderTours(tours) {
    const container = document.getElementById('tours-container');
    if (!container) return;

    container.innerHTML = '';

    if (tours.length === 0) {
        document.getElementById('no-results').style.display = 'block';
        return;
    } else {
        document.getElementById('no-results').style.display = 'none';
    }

    tours.forEach((tour, index) => {
        const cardHTML = `
            <div class="soft-card" style="animation: fadeInUp 0.5s ease forwards ${index * 0.1}s; opacity: 0; transform: translateY(20px);">
                <div class="soft-card-image">
                    <img src="${tour.image}" alt="${tour.title}">
                    <span class="soft-category">${tour.category}</span>
                </div>
                
                <div class="soft-card-content">
                    <div class="soft-card-header">
                        <h3 class="soft-title">${tour.title}</h3>
                        <span class="soft-price">${(tour.price / 1000).toLocaleString('fa-IR')} هزارتومان</span>
                    </div>
                    
                    <ul class="soft-features">
                        <li><i class="fas fa-map-marker-alt"></i> ${tour.location}</li>
                        <li><i class="fas fa-clock"></i> ${tour.duration}</li>
                        <li><i class="fas fa-star"></i> ۴.۸ (رضایت بالا)</li>
                    </ul>
                    
                    <div class="soft-actions">
                        <a href="tour-details.html?id=${tour.id}" class="btn-outline-soft">جزئیات</a>
                        <!-- تابع checkLoginAndBook از فایل script.js اصلی خوانده میشود -->
                        <button class="btn-fill-soft" onclick="checkLoginAndBook('${tour.title}')">رزرو</button>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += cardHTML;
    });
}

function filterTours() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    
    const filtered = toursData.filter(tour => {
        return tour.title.toLowerCase().includes(query) || 
               tour.location.toLowerCase().includes(query) ||
               tour.category.toLowerCase().includes(query);
    });
    
    renderTours(filtered);
}

const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);