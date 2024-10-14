window.onload = function () {

    /* function to add event listner on an array of elements */
    const eventListeners = new WeakMap();
    const addEventOnElem = function (elem, type, callback) {
        const addListener = (el) => {
            el.addEventListener(type, callback);
            if (!eventListeners.has(el)) {
                eventListeners.set(el, {});
            }
            if (!eventListeners.get(el)[type]) {
                eventListeners.get(el)[type] = [];
            }
            eventListeners.get(el)[type].push(callback);
        };

        if (elem.length > 1) {
            for (let i = 0; i < elem.length; i++) {
                addListener(elem[i]);
            }
        } else {
            addListener(elem);
        }
    };

    /* function to remove event listener from a group of elements */
    const removeExistingEventListeners = function (elem, type) {
        const removeListeners = (el) => {
            if (eventListeners.has(el) && eventListeners.get(el)[type]) {
                eventListeners.get(el)[type].forEach(callback => {
                    el.removeEventListener(type, callback);
                });
                eventListeners.get(el)[type] = [];
            }
        };

        if (elem.length > 1) {
            for (let i = 0; i < elem.length; i++) {
                removeListeners(elem[i]);
            }
        } else {
            removeListeners(elem);
        }
    };

    /* function to send an ajax call to backend to get number of items in wishlist and cat to be displaued to user */
    const getCountUrl = document.querySelector("[data-get-count-url]").getAttribute("data-get-count-url");
    const getCartCount = async () => {
        try {
            const response = await fetch(getCountUrl);
            const data = await response.json();
            const dataCartBadge = document.querySelector("[data-cart-badge]");
            dataCartBadge.innerHTML = data.cart_count;
            const dataWishListBadge = document.querySelector("[data-wishlist-badge]");
            dataWishListBadge.innerHTML = data.wishlist_count;
            const cartTotal = document.querySelector("[data-cart-total]");
            cartTotal.innerHTML = data.cart_total;
        } catch (error) {
            console.error('Error getting cart count:', error);
        }
    }
    getCartCount();

    /* functions to toggle navbar on small screens  */
    const navToggler = document.querySelector("[data-nav-toggler]");
    const nav = document.querySelector("[data-navbar]");
    const navClose = document.querySelector("[data-nav-close]");
    const navOverlay = document.querySelector("[data-overlay]");
    const btnUp = document.querySelector("[data-back-top-btn]");
    const toggleNav = function () {
        nav.classList.toggle("active");
        navOverlay.classList.toggle("active");
    }
    const closeNav = function () {
        nav.classList.remove("active");
        navOverlay.classList.remove("active");
    }
    addEventOnElem(navToggler, "click", toggleNav);
    addEventOnElem(navClose, "click", closeNav);

    /* function to show the button which moves to start of page */
    const header = document.querySelector("[data-header]");
    let lastScrolledPos = 0;
    const headeractive = function () {
        if (window.scrollY > 150) {
            header.classList.add("active");
            btnUp.classList.add("active");
        } else {
            header.classList.remove("active");
            btnUp.classList.remove("active");
        }
    }
    /* function to make header sticky on scrolling */
    const headerSticky = function () {
        if (lastScrolledPos >= window.scrollY) {
            header.classList.remove(".header-hide");
        } else {
            header.classList.add(".header-hide");
        }
        lastScrolledPos = window.scrollY;
    }
    addEventOnElem(window, "scroll", headeractive);
    addEventOnElem(window, "scroll", headerSticky);


    /** Display Cart */
    const cartToggler = document.querySelector("[data-cart-toggler]");
    const cart = document.querySelector("[data-cart]");
    const cartClose = document.querySelector("[data-cart-close]");
    const cartOverlay = document.querySelector("[data-cart-overlay]");
    const addToCartUrl = cart.getAttribute("data-add-to-cart-url");
    const cartToggle = () => {
        cart.classList.toggle("active");
        cartOverlay.classList.toggle("active");
    }
    const closeCart = () => {
        cart.classList.remove("active");
        cartOverlay.classList.remove("active");
    }
    addEventOnElem(cartToggler, "click", cartToggle);
    addEventOnElem(cartClose, "click", closeCart);


    /* functions that send a request to backend to inc or dec quantity of item in cart */
    const incQuantity = async (event, incQuantityUrl) => {
        try {
            const incQ = event.target;
            const productPk = incQ.getAttribute("product-id");
            const response = await fetch(`${incQuantityUrl}?productPk=${productPk}`);
            const data = await response.json();
            if (data.status === "200") {
                const quantity = document.querySelector(`[data-quantity-id="${productPk}"]`);
                quantity.innerHTML = data.quantity;
                const cartTotal = document.querySelector("[data-cart-total]");
                cartTotal.innerHTML = data.cart_total;
            }
            else {
                alert(data.message);
            }

        } catch (error) {
            console.error('Error increasing quantity:', error);
        }
    };
    const decQuantity = async (event, decQuantityUrl) => {
        try {
            const decQ = event.target;
            const productPk = decQ.getAttribute("product-id");
            const response = await fetch(`${decQuantityUrl}?productPk=${productPk}`);
            const data = await response.json();
            if (data.status === "200") {
                const quantity = document.querySelector(`[data-quantity-id="${productPk}"]`);
                quantity.innerHTML = data.quantity;
                const cartTotal = document.querySelector("[data-cart-total]");
                cartTotal.innerHTML = data.cart_total;
            }
            else {
                alert(data.message);
            }

        } catch (error) {
            console.error('Error decreasing quantity:', error);
        }
    };

    /* function to add event listners to increase and decrease button of items in cart */
    const addEventsOnQuantityBtns = async (incQuantityUrl, decQuantityUrl) => {
        const increaseButton = document.querySelectorAll("[data-item-quantity-inc]");
        const decreaseButton = document.querySelectorAll("[data-item-quantity-dec]");

        /* remove existing event listners */
        removeExistingEventListeners(decreaseButton, 'click');
        removeExistingEventListeners(increaseButton, 'click');

        /* add the new ones */
        increaseButton.forEach(item => {
            addEventOnElem(item, 'click', (event) => incQuantity(event, incQuantityUrl));
        });

        decreaseButton.forEach(item => {
            addEventOnElem(item, 'click', (event) => decQuantity(event, decQuantityUrl));
        });

    }

    const incQuantityUrl = document.querySelector("[data-item-quantity-inc]").getAttribute("inc-check-quantity-url");
    const decQuantityUrl = document.querySelector("[data-item-quantity-dec]").getAttribute("dec-check-quantity-url");
    addEventsOnQuantityBtns(incQuantityUrl, decQuantityUrl);

    /* function to send ajax call to backend to remove item from cart */
    const removeItem = async (event, removeItemUrl) => {
        try {
            const remove = event.target;
            const productPk = remove.getAttribute("product-id");
            const response = await fetch(`${removeItemUrl}?productPk=${productPk}`);
            const data = await response.json();
            if (data.status === "200") {
                const cartTotal = document.querySelector("[data-cart-total]");
                cartTotal.innerHTML = data.cart_total;
                const item = document.querySelector(`[data-item-id="${productPk}"]`);
                item.remove();
                const dataCartBadge = document.querySelector("[data-cart-badge]");
                dataCartBadge.innerHTML = data.cart_count;
            }
            else {
                alert(data.message);
            }

        } catch (error) {
            console.error('Error removing item:', error);
        }
    };
    const removeItemUrl = document.querySelector("[data-item-remove]").getAttribute("data-item-remove-url");
    const removeItemBtn = document.querySelectorAll("[data-item-remove]");
    removeItemBtn.forEach(item => {
        addEventOnElem(item, 'click', (event) => removeItem(event, removeItemUrl));
    });

    /* function to send ajax call to backend to remove item from cart */
    const removewish = async (event, removewishUrl) => {
        try {
            const remove = event.target;
            const productPk = remove.getAttribute("product-id");
            const response = await fetch(`${removewishUrl}?productPk=${productPk}`);
            const data = await response.json();
            if (data.status === "200") {
                const cartTotal = document.querySelector("[data-cart-total]");
                cartTotal.innerHTML = data.cart_total;
                const wish = document.querySelector(`[data-wish-id="${productPk}"]`);
                wish.remove();
                const dataWishListBadge = document.querySelector("[data-wishlist-badge]");
                dataWishListBadge.innerHTML = data.wishlist_count;
            }
            else {
                alert(data.message);
            }

        } catch (error) {
            console.error('Error removing wish:', error);
        }
    };
    const removewishUrl = document.querySelector("[data-wish-remove]").getAttribute("data-wish-remove-url");
    const removewishBtn = document.querySelectorAll("[data-wish-remove]");
    removewishBtn.forEach(wish => {
        addEventOnElem(wish, 'click', (event) => removewish(event, removewishUrl));
    });


    /** Display WishList */
    const wishlistToggler = document.querySelector("[data-wishlist-toggler]");
    const wishlist = document.querySelector("[data-wishlist]");
    const wishlistClose = document.querySelector("[data-wishlist-close]");
    const wishlistOverlay = document.querySelector("[data-wishlist-overlay]");
    const addToWishListUrl = wishlist.getAttribute("data-add-to-wishlist-url");
    const wishlistToggle = () => {
        wishlist.classList.toggle("active");
        wishlistOverlay.classList.toggle("active");
    }
    const closeWishlist = () => {
        wishlist.classList.remove("active");
        wishlistOverlay.classList.remove("active");
    }
    addEventOnElem(wishlistToggler, "click", wishlistToggle);
    addEventOnElem(wishlistClose, "click", closeWishlist);


    /*  AJAX setup to send cookie with csrf token with each request */
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /** function that create html to be inserted after loading products for the requested page */
    let currentPage = 1;
    function createProductCard(product) {
        const inStock = product.quantity_in_stock != null && parseInt(product.quantity_in_stock, 10) > 0;
        return `<li class="scrollbar-item product">
            <div class="shop-card product-card">
                <div class="card-banner img-holder">
                    <img src="${product.image_url}" width="300" height="300" loading="lazy" alt="${product.name}" class="product-img">
                    ${inStock
                ? (product.offer ? `<span class="badge" aria-label="${product.offer} off">${product.offer}</span>` : '')
                : `<span class="badge out-of-stock" aria-label="Out of stock">Out of stock</span>`
            }

                    <div class="card-actions">
                    ${inStock ? `
                        <button class="action-btn" aria-label="add to cart" data-product-pk="${product.id}" data-add-to-cart>
                            <ion-icon name="bag-handle-outline" aria-hidden="true"></ion-icon>
                        </button>
                        ` : ''}
                        <button class="action-btn" aria-label="add to wishlist"  data-product-pk="${product.id}" data-add-to-wishlist>

                            <ion-icon name="star-outline" aria-hidden="true"></ion-icon>
                        </button>
                    </div>
                </div>
                <div class="card-content">
                    <div class="price">
                        ${product.offer && inStock
                ? `
                            <del class="price-old">${product.price}</del>
                            <span class="price-new">${(product.price * (1 - product.discount)).toFixed(2)}</span>
                            `
                : `<span class="price-new">${product.price}</span>`
            }
                    </div>

                    <h3>
                        <a href="${product.product_url}" class="card-title">${product.name}</a>
                    </h3>
                    <p>${product.description}</p>

                    <div class="card-rating">
                        <div class="rating-wrapper" aria-label="5 star rating">
                            ${Array(5).fill('<ion-icon name="star" aria-hidden="true"></ion-icon>').join('')}
                        </div>
                        <p class="rating-text">
                            ${product.reviews} reviews
                        </p>
                    </div>
                </div>
            </div>
        </li>`;
    }

    /* function that send ajax call to backend to get the current page products */
    async function loadProducts(page, url) {
        try {
            const response = await fetch(`${url}?page=${page}`);
            const data = await response.json();

            const productContainer = document.querySelector("[products-list]");
            const nextButton = document.querySelector("[products-next]");
            const prevButton = document.querySelector("[products-prev]");

            // clear existing products if going to a new page
            productContainer.innerHTML = '';

            // add new products
            data.products.forEach(product => {
                productContainer.insertAdjacentHTML('beforeend', createProductCard(product));
            });

            // update button visibility
            nextButton.style.display = data.has_next ? 'block' : 'none';
            prevButton.style.display = page > 1 ? 'block' : 'none';

            currentPage = data.current_page;

        } catch (error) {
            console.error('Error loading products:', error);
        }
    }

    /* function that send ajax call to backend to add product to cart */
    const addToCart = (event, addToCartUrl) => {
        const addtocart = event.target;
        const productPk = addtocart.getAttribute("data-product-pk");
        $.ajax({
            url: addToCartUrl,
            data: {
                'productPk': productPk,
            },
            dataType: 'json',
            success: function (data) {
                if (data.status == 201) {
                    /* edit cart total */
                    const cartTotal = document.querySelector("[data-cart-total]");
                    cartTotal.innerHTML = data.cart_total;
                    console.log("add to cart");
                    location.reload();
                }
                else {
                    alert(data.message);
                }
            }
        });
    };

    /* function that send ajax call to backend to add product to wishlist */
    const addToWishList = (event, addToWishListUrl) => {
        const addtowishlist = event.target;
        const productPk = addtowishlist.getAttribute("data-product-pk");
        $.ajax({
            url: addToWishListUrl,
            data: {
                'productPk': productPk,
            },
            dataType: 'json',
            success: function (data) {
                if (data.status == 201) {
                    location.reload();
                }
                else {
                    alert(data.message);
                }
            }
        });
    }

    /* adding events to add to cart and to add to wish list buttons */
    const addEventsOnWishlistCartBtns = async (addToCartUrl, addToWishListUrl) => {
        const addtocart = document.querySelectorAll("[data-add-to-cart]");
        const addtowishlist = document.querySelectorAll("[data-add-to-wishlist]");

        /* remove existing event listners */
        removeExistingEventListeners(addtocart, 'click');
        removeExistingEventListeners(addtowishlist, 'click');

        /* add the new ones */
        addtocart.forEach(item => {
            addEventOnElem(item, 'click', (event) => addToCart(event, addToCartUrl));
        });

        addtowishlist.forEach(item => {
            addEventOnElem(item, 'click', (event) => addToWishList(event, addToWishListUrl));
        });
    }

    const addAfterLoad = async (addToCartUrl, addToWishListUrl) => {
        try {
            const nextButton = document.querySelector("[products-next]");
            const prevButton = document.querySelector("[products-prev]");
            const urlElement = document.querySelector("[our-products]");
            const url = urlElement ? urlElement.getAttribute('url') : '';

            await loadProducts(currentPage, url);
            await addEventsOnWishlistCartBtns(addToCartUrl, addToWishListUrl);

            nextButton.addEventListener('click', async function () {
                await loadProducts(currentPage + 1, url);
                await addEventsOnWishlistCartBtns(addToCartUrl, addToWishListUrl);
            });

            prevButton.addEventListener('click', async function () {
                if (currentPage > 1) {
                    await loadProducts(currentPage - 1, url);
                    await addEventsOnWishlistCartBtns(addToCartUrl, addToWishListUrl);
                }
            });

        } catch (err) {
            console.error('Error loading products:', err);
            try {
                await addEventsOnWishlistCartBtns(addToCartUrl, addToWishListUrl);
            }
            catch (err) {
                console.error('Error adding to cart or cart:', err);
            }
        }
    }

    addAfterLoad(addToCartUrl, addToWishListUrl);

}
