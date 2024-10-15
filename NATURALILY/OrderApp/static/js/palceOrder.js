document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('paymentForm');
    const submitButton = document.getElementById('submitButton');
    const cashOnDelivery = document.getElementById('cashOnDelivery');
    const creditCard = document.getElementById('creditCard');

    function updateFormAction() {
        if (cashOnDelivery.checked) {
            form.action = cashOnDelivery.getAttribute("data-COD-url");
            submitButton.value = "Submit Order";
            submitButton.style.display = "block";
        } else if (creditCard.checked) {
            form.action = "{% url 'process_payment' %}";
            submitButton.value = "Pay Now";
            submitButton.style.display = "block";
        } else {
            submitButton.style.display = "none";
        }
    }


    cashOnDelivery.addEventListener('change', updateFormAction);
    creditCard.addEventListener('change', updateFormAction);

    // Initial call to set the correct action
    updateFormAction();

});