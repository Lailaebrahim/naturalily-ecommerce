document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('paymentForm');
    const submitButton = document.getElementById('checkout-button');
    const cashOnDelivery = document.getElementById('cashOnDelivery');
    const creditCard = document.getElementById('creditCard');

    function updateFormAction() {
        if (cashOnDelivery.checked) {
            form.action = cashOnDelivery.getAttribute("data-COD-url");
            submitButton.value = "Submit Order";
            submitButton.style.display = "block";

            form.onsubmit = null;
        } else if (creditCard.checked) {
            submitButton.value = "Pay Now";
            submitButton.style.display = "block";
            submitButton.type = 'button';

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const payUrl = creditCard.getAttribute("data-creditCard-url");
            const pubKey = creditCard.getAttribute("data-STRIPE-PUBLIC-KEY");
            var stripe = Stripe(pubKey);

            form.onsubmit = function (e) {
                e.preventDefault();
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                data.userID = creditCard.getAttribute("data-user-id");

                fetch(payUrl, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                    .then(response => response.json())
                    .then(session => {
                        return stripe.redirectToCheckout({ sessionId: session.id });
                    })
                    .then(result => {
                        if (result.error) {
                            alert(result.error.message);
                        }
                    })
                    .catch(error => console.error("Error:", error));
            };


            // Add event listener to the button
            submitButton.onclick = () => form.requestSubmit();

        } else {
            submitButton.style.display = "none";
            submitButton.type = 'submit';
        }
    }

    cashOnDelivery.addEventListener('change', updateFormAction);
    creditCard.addEventListener('change', updateFormAction);

    // Initial call to set the correct action
    updateFormAction();

});