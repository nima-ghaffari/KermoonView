document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.auth-tab');
    const forms = document.querySelectorAll('.auth-form');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            tab.classList.add('active');
            
            const targetId = tab.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });
});

document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const pass = document.getElementById('reg-pass').value;
    const confirm = document.getElementById('reg-confirm').value;
    const btn = this.querySelector('button');
    const originalText = btn.innerHTML;

    if (pass !== confirm) {
        alert('رمز عبور و تکرار آن یکسان نیستند!');
        return;
    }

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> لطفا صبر کنید...';
    btn.disabled = true;

    setTimeout(() => {
        alert('ثبت نام با موفقیت انجام شد!');
        window.location.href = 'index.html';
    }, 2000);
});

document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const btn = this.querySelector('button');
    const originalText = btn.innerHTML;

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال ورود...';
    btn.disabled = true;

    setTimeout(() => {
        alert('خوش آمدید!');
        window.location.href = 'index.html';
    }, 2000);
});