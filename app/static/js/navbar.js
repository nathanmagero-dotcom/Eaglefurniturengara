/*==================================================
    Eagle Furniture V3
    navbar.js
==================================================*/

document.addEventListener("DOMContentLoaded", function () {

    const navbar = document.querySelector(".navbar");

    /*==============================
        SHADOW ON SCROLL
    ==============================*/

    window.addEventListener("scroll", function () {

        if (window.scrollY > 20) {

            navbar.classList.add("scrolled");

        } else {

            navbar.classList.remove("scrolled");

        }

    });

    /*==============================
        ACTIVE LINK
    ==============================*/

    const currentPath = window.location.pathname;

    document.querySelectorAll(".nav-link").forEach(link => {

        const href = link.getAttribute("href");

        if (href === currentPath) {

            document.querySelectorAll(".nav-link").forEach(item => {

                item.classList.remove("active");

            });

            link.classList.add("active");

        }

    });

    /*==============================
        CLOSE MOBILE MENU
    ==============================*/

    const navLinks = document.querySelectorAll(".nav-link");

    const navbarCollapse = document.getElementById("mainNavbar");

    navLinks.forEach(link => {

        link.addEventListener("click", () => {

            if (window.innerWidth < 992 && navbarCollapse.classList.contains("show")) {

                const collapse = bootstrap.Collapse.getInstance(navbarCollapse);

                if (collapse) {

                    collapse.hide();

                }

            }

        });

    });

});