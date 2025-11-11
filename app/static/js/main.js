/* ==============================
   main.js — основной JS-файл сайта
   ============================== */

// --- Переключение версии для слабовидящих ---
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('toggle-accessibility');
    const accessibleLink = document.querySelector('link[title="accessible"]');

    if (!btn || !accessibleLink) return;

    // Устанавливаем сохранённое состояние
    const saved = localStorage.getItem('accessible');
    if (saved === 'on') {
        accessibleLink.disabled = false;
    } else {
        accessibleLink.disabled = true;
    }

    // При нажатии — переключаем стили
    btn.addEventListener('click', () => {
        if (accessibleLink.disabled) {
            accessibleLink.disabled = false;
            localStorage.setItem('accessible', 'on');
        } else {
            accessibleLink.disabled = true;
            localStorage.setItem('accessible', 'off');
        }
    });
});

// --- Поиск по странице ---
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const articles = document.querySelectorAll('.news-item, .vacancy-card');

    if (!searchInput || !articles.length) return;

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        articles.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
        });
    });
});

// --- Кнопка "Наверх" ---
document.addEventListener('DOMContentLoaded', () => {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerText = '▲';
    scrollBtn.id = 'scrollTopBtn';
    scrollBtn.title = 'Наверх';
    document.body.appendChild(scrollBtn);

    scrollBtn.style.position = 'fixed';
    scrollBtn.style.bottom = '30px';
    scrollBtn.style.right = '30px';
    scrollBtn.style.backgroundColor = '#2563eb';
    scrollBtn.style.color = '#fff';
    scrollBtn.style.border = 'none';
    scrollBtn.style.padding = '10px 14px';
    scrollBtn.style.borderRadius = '6px';
    scrollBtn.style.cursor = 'pointer';
    scrollBtn.style.display = 'none';
    scrollBtn.style.fontSize = '20px';
    scrollBtn.style.zIndex = '1000';
    scrollBtn.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';

    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
