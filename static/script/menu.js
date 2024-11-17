document.addEventListener('DOMContentLoaded', function () {
    
    const menuBtn = document.getElementById('menuSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    document.body.appendChild(overlay);

    const menuItems = document.querySelectorAll('.menu-items li a');
    const submenuSo = document.getElementById('submenu-so');

    menuItems.forEach((menuItem) => {
        menuItem.addEventListener('click', function (e) {
            e.preventDefault(); 
            handleMenuClick(menuItem.textContent.trim()); 
        });
    });

    function handleMenuClick(menuText) {
        // Toggle submenu visibility when clicking "Chuyển đổi số"
        if (menuText === 'Chuyển đổi số') {
            submenuSo.style.display = submenuSo.style.display === 'none' ? 'block' : 'none';
        } else {
            submenuSo.style.display = 'none'; 
        }
    }

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
