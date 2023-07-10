# Product Manager

Product Manager is a Django-based web application that provides functionalities for managing products. It allows users to authenticate, view and search products, sort search results, select products, and maintain user sessions. This README provides an overview of the project structure, key features, and instructions for running the application.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up the Product Manager application, follow these steps:

1. Clone the repository:

   ```shell
   git clone /home/software/PycharmProjects/product_manager
   ```

2. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

To run the Product Manager application, use the following command:

```shell
python manage.py runserver
```

The application will start on `http://localhost:8000`.

## Features

Product Manager offers the following features:

1. **Authentication**: The application provides an authentication screen where users can enter their credentials. The backend verifies the credentials and grants access upon successful authentication. The logged-in user's email is displayed in the top right corner.

2. **Product Listing**: After logging in, users can view an empty table of products along with a search field. The table contains columns such as ID, name, description, price, and stock.

3. **Search**: Users can enter a search string, and the application sends an API request to the backend. As the user types, the search results are displayed dynamically.

4. **Sorting**: Users can sort the search results by any of the available fields. The application sends the appropriate API request to the backend, which returns sorted search results.

5. **Product Selection**: Users have the ability to "select" any product, triggering a request to the backend. The backend marks the selected product as chosen.

6. **User Session Persistence**: User sessions are saved, allowing users to reopen the browser tab and have their search results, selections, and authentication session automatically restored.

7. **Logout**: A logout button is available to users. Clicking the logout button clears the session and logs the user out of the application.

## API Endpoints

The following are the main API endpoints used in the Product Manager application:

- `/api/signup/` (POST): User signup endpoint to create a new account.
- `/api/product/create/` (POST): Endpoint for creating a new product.
- `/api/product/search/` (GET): Endpoint for searching and sorting products.

**Proper API are mentioned in postman collection**


Refer to the API documentation or code implementation for detailed request/response information.

## Docker

You can also run the Product Manager application using Docker. The Dockerfile provided with the project allows you to containerize the application with ease. Here's how to use Docker:

1. Build the Docker image:

   ```shell
   docker build -t product-manager .
   ```

2. Run a Docker container based on the image:

   ```shell
   docker run -p 8010:8010 product-manager
   ```

The application will be accessible at `http://localhost:8010` inside the Docker container and on your local machine.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).