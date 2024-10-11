window.onload = function() {
    const addEventOnElem = function (elem, type, callback) {
        if (elem.length > 1) {
            for (let i = 0; i < elem.length; i++) {
                elem[i].addEventListener(type, callback);
            }
        } else {
            elem.addEventListener(type, callback);
        }
    };

    const navToggler = document.querySelector("[data-nav-toggler]");
    const nav = document.querySelector("[data-navbar]");
    const navLinks = document.querySelectorAll("[data-nav-link]");
    const navClose = document.querySelector("[data-nav-close]");
    const navOverlay = document.querySelector("[data-overlay]");
    const btnUp = document.querySelector("[data-back-top-btn]");

    const toggleNav = function () { 
        nav.classList.toggle("active");
        navOverlay.classList.toggle("active");
    }

    addEventOnElem(navToggler, "click", toggleNav);

    const closeNav = function () {
        nav.classList.remove("active");
        navOverlay.classList.remove("active");
    }

    addEventOnElem(navClose, "click", closeNav);

    const header = document.querySelector("[data-header]");

    const headeractive = function () {
        if (window.scrollY > 150) {
            header.classList.add("active");
            btnUp.classList.add("active");
        } else {
            header.classList.remove("active");
            btnUp.classList.remove("active");
        }
    }

    addEventOnElem(window, "scroll", headeractive);

    let lastScrolledPos = 0;
    const headerSticky = function () {
        if (lastScrolledPos >= window.scrollY) {
            header.classList.remove(".header-hide");
        } else {
            header.classList.add(".header-hide");
        }
        lastScrolledPos = window.scrollY;
    }

    addEventOnElem(window, "scroll", headerSticky);

    
    /** reveal content on scrolling 
     * 
     * 
     * const sections = document.querySelectorAll("[data-section]");
    const revealSection = function () {
        sections.forEach(section => {
            if (window.scrollY + window.innerHeight > section.offsetTop) {
                section.classList.add("active");
            }
        });
    }
    addEventOnElem(window, "scroll", revealSection);
    */
    

}
