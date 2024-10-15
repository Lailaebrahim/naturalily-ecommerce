document.addEventListener('DOMContentLoaded', function() {
    const newPrice = document.querySelector("[data-price-after-offer]");
    const oldPrice = document.querySelector("[data-price-before-offer]").getAttribute('data-price-before-offer');
    const discount = document.querySelector("[data-discount]").getAttribute('data-discount');
    const price = parseInt(oldPrice) - parseInt(oldPrice) * parseFloat(discount);
    newPrice.innerHTML = price;
});