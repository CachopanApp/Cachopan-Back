# Cachopan-Back

## Overview

This project is a RESTful API built with Flask, providing endpoints for managing users and clients. The API supports operations such as creating, updating, deleting, and retrieving users and clients. It also includes JWT-based authentication for secure access.

## Project Structure

```
.
├── app
│   ├── config.py
│   ├── extensions.py
│   ├── __init__.py
│   ├── migrations
│   ├── models
│   │   ├── client.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── user.cpython-312.pyc
│   │   └── user.py
│   ├── __pycache__
│   │   ├── config.cpython-312.pyc
│   │   ├── extensions.cpython-312.pyc
│   │   └── __init__.cpython-312.pyc
│   ├── routes
│   │   ├── client.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── user.cpython-312.pyc
│   │   └── user.py
│   ├── schemas
│   │   ├── client.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── user.cpython-312.pyc
│   │   └── user.py
│   └── services
│       ├── client.py
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── client.cpython-312.pyc
│       │   ├── __init__.cpython-312.pyc
│       │   └── user.cpython-312.pyc
│       └── user.py
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Endpoints

### User Endpoints

- **Create User**
    - **URL:** `/user/create`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
            "name": "string",
            "email": "string",
            "password": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "name": "string",
            "email": "string"
        }
        ```

- **Authenticate User**
    - **URL:** `/user/login`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
            "name": "string",
            "password": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "access_token": "string"
        }
        ```

### Client Endpoints

- **Get All Clients**
    - **URL:** `/client/getAll/<int:user_id>`
    - **Method:** `GET`
    - **Response:**
        ```json
        [
            {
                "name": "string",
                "email": "string",
                "number": "string",
                "user_id": "integer"
            }
        ]
        ```

- **Create Client**
    - **URL:** `/client/create`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
            "name": "string",
            "email": "string",
            "number": "string",
            "user_id": "integer"
        }
        ```
    - **Response:**
        ```json
        {
            "name": "string",
            "email": "string",
            "number": "string",
            "user_id": "integer"
        }
        ```

- **Get Client by ID**
    - **URL:** `/client/get/<int:client_id>`
    - **Method:** `GET`
    - **Response:**
        ```json
        {
            "name": "string",
            "email": "string",
            "number": "string",
            "user_id": "integer"
        }
        ```

- **Update Client**
    - **URL:** `/client/update/<int:client_id>`
    - **Method:** `PUT`
    - **Request Body:**
        ```json
        {
            "name": "string",
            "email": "string",
            "number": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "name": "string",
            "email": "string",
            "number": "string",
            "user_id": "integer"
        }
        ```

- **Delete Client**
    - **URL:** `/client/delete/<int:client_id>`
    - **Method:** `DELETE`
    - **Response:** `204 No Content`

## Configuration

Configuration settings are managed in the 

config.py

 file. Ensure to update the database URI and other settings as per your environment.

## License

This project is licensed under the MIT License. See the 

LICENSE

 file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any inquiries or support, please contact [your-email@example.com](mailto:your-email@example.com).

---

Enjoy using the API! 🚀