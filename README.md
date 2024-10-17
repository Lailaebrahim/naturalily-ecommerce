# ALX Backend Specialization Portfolio Project

# Naturalily E-commerce Web Application

Welcome to the ALX Backend Specialization Portfolio Project!

## Overview

Naturalily is an e-commerce web application designed to provide a seamless shopping experience for users looking to purchase natural and organic products. The application features a user-friendly interface, secure payment processing, and efficient order management.

## Features

- **User Authentication**: Secure login and registration system.
- **Product Catalog**: Browse and products with detailed descriptions and images.
- **Shopping Cart**: Add, remove, and update items in the cart.
- **Wishlist**: Save products to your wishlist for future purchase.
- **Product Reviewing**: Leave reviews and ratings for products.
- **Checkout Process**: Secure payment gateway integration.
- **Order Management**: Track order status and history.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django
- **Database**: PostgreSQL
- **Payment Gateway**: Stripe

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Lailaebrahim/ALX-Backend-Specialization-Portfoilo-Project.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Install PostgreSQL:
    ```bash
    sudo apt-get install postgresql postgresql-contrib
    ```
    or on Windows, download and install PostgreSQL from [the official website](https://www.postgresql.org/download/).

5. Initialize the database using `db_init.sql`:
    ```bash
    sudo -u postgres psql -f path/to/db_init.sql
    ```
    **Note**: Make sure to edit the `db_init.sql` file to include your own database name, user, and password.

6. Edit the `settings.py` file to include your database configuration:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    5. Initialize the database using `db_init.sql`:

        On Linux:
        ```bash
        sudo -u postgres psql -f path/to/db_init.sql
        ```

        On Windows:
        ```bash
        psql -U postgres -f path\to\db_init.sql
        ```

        **Note**: Make sure to edit the `db_init.sql` file to include your own database name, user, and password.

6. Edit the `settings.py` file to include your database configuration:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

7. Apply database migrations:
    ```bash
    python manage.py migrate
    ```
8. Start the development server:
    ```bash
    python manage.py runserver
    ```
9. For using Stripe API in development mode, you need to create a Stripe developer account. You can sign up at [Stripe](https://stripe.com).

10. Install Stripe cli:

    ```bash
    curl -s https://cli-assets.heroku.com/install.sh | sh
    ```

    or on Windows, download and install the Stripe CLI from [the official website](https://stripe.com/docs/stripe-cli#install).

11. Log in to the Stripe CLI:
    ```bash
    stripe login
    ```

12. Start the Stripe webhook forwarding:
    ```bash
    stripe listen --forward-to http://127.0.0.1:8000/orders/webhooks/stripe/
    ```

    > **Note**: starting the Stripe webhook forwarding is essential for receiving real-time notifications about events related to your Stripe account, such as successful payments, refunds, and disputes. This allows your application to respond to these events promptly and update the order status accordingly.

13. Modify the Stripe public key, secret key, and webhook key in `settings.py`:
    ```python
    STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
    STRIPE_SECRET_KEY = 'your_stripe_secret_key'
    STRIPE_WEBHOOK_SECRET = 'your_stripe_webhook_secret_key'
    ```

    > **Note**: The Stripe public key and secret key are used to authenticate your application with the Stripe API. The webhook secret key is used to verify the authenticity of the events received from Stripe, ensuring that they are not tampered with.

14. Start the development server:
        ```bash

        cd NATURALILY
        python manage.py runserver
        ```
    ```

## Usage

1. Register or log in to your account.
2. Browse the product catalog and add items to your cart.
3. Proceed to checkout and complete the payment process.
4. Track your order status from your account dashboard.

![Usage GIF](NATURALILY.gif)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact:

- **Laila Ebrahim**
- **Email**: lailaebraheim108@gmail.com
- **GitHub**: [Lailaebrahim](https://github.com/Lailaebrahim)
