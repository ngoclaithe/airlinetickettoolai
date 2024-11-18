document.addEventListener('DOMContentLoaded', function () {
    
    const menuBtn = document.getElementById('menuSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    document.body.appendChild(overlay);

    menuBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        toggleSidebar();
    });

    overlay.addEventListener('click', function () {
        closeSidebar();
    });

    sidebar.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    document.addEventListener('click', function (e) {
        if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
            closeSidebar();
        }
    });

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        menuBtn.classList.toggle('active');
    }

    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        menuBtn.classList.remove('active');
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const accountIcon = document.getElementById('accountIcon');
    const detailAccount = document.getElementById('detail-account');

    console.log(user_id);

    accountIcon.addEventListener('click', function (e) {
        e.preventDefault();
        if (user_id == "None") {
            window.location.href = loginUrl;
        } else {
            detailAccount.style.display = detailAccount.style.display === 'none' ? 'block' : 'none';
        }
    });

    document.addEventListener('click', function (e) {
        if (!detailAccount.contains(e.target) && !accountIcon.contains(e.target)) {
            detailAccount.style.display = 'none';
        }
    });
});
