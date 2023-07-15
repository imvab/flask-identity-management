# User Identity Management API

This repository contains an API for managing user identities, built using Flask framework. It provides various endpoints to handle user-related operations such as user creation, retrieval, updating, and deletion.

## Installation

To use this API, you need to have Python and Flask installed on your system.

1. Clone this repository to your local machine:

```bash
git clone https://github.com/imvab/flask-identity-management.git
```

2. Navigate to the project directory:

```bash
cd flask-identity-manager
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To start the API, run the following command in your terminal:

```bash
flask run
```

By default, the API will be accessible at `http://localhost:5000`.

## Endpoints

The API exposes the following endpoints:

### Identity Creation

- **Endpoint**: `/identity`
- **Method**: `POST`
- **Parameters**:
  - `email` (string?): The email of the identity to create.
  - `phoneNumber` (string?): The phone number of the identity.
- **Example**:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "john.doe@example.com",
  "phoneNumber": "12345678"
}' http://localhost:5000/identity
```
- **Sample Response**

```
{
    "contact": {
        "emails": [
            "test-test@gmail.com",
            "test@gmail.com"
        ],
        "phoneNumbers": [
            "8777123456",
            "877712345"
        ],
        "primaryContatctId": 27,
        "secondaryContactIds": [
            28,
            29,
            30,
            31,
            32
        ]
    }
}
```