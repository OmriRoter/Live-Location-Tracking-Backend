# Live Location Tracking API

A lightweight, real-time location tracking API built with FastAPI and MongoDB. This API provides essential endpoints for building real-time location sharing applications.

## Features

- User creation and management
- User verification (login)
- Real-time location updates
- Location retrieval for specific users
- Active status management
- Built with FastAPI for high performance
- MongoDB for reliable data storage
- Deployed on Vercel for serverless execution

## Base URL

```
https://live-location-tracking-backend.vercel.app
```

## API Documentation

### 1. Create New User

Creates a new user in the system.

**Endpoint:** `POST /api/users/create`

**Request Body:**

```json
{
  "username": "string"
}
```

**Response:** `201 Created`

```json
{
  "id": "string",
  "username": "string",
  "created_at": "datetime",
  "is_active": true
}
```

**Possible Errors:**

- `400 Bad Request` - Username already exists
- `500 Internal Server Error` - Server error

### 2. Verify User (Login)

Verifies if a user exists in the system.

**Endpoint:** `POST /api/users/verify`

**Request Body:**

```json
{
  "user_id": "string"
}
```

**Response:** `200 OK`

```json
{
  "id": "string",
  "username": "string",
  "created_at": "datetime",
  "is_active": true
}
```

**Possible Errors:**

- `400 Bad Request` - Invalid ID format
- `404 Not Found` - User not found
- `500 Internal Server Error` - Server error

### 3. Update User Status

Updates user's active status.

**Endpoint:** `PATCH /api/users/{user_id}/status`

**Request Body:**

```json
{
  "is_active": boolean
}
```

**Response:** `200 OK`

```json
{
  "id": "string",
  "username": "string",
  "created_at": "datetime",
  "is_active": boolean
}
```

**Possible Errors:**

- `400 Bad Request` - Invalid ID format
- `404 Not Found` - User not found
- `500 Internal Server Error` - Server error

### 4. Update User Location

Updates the current location of a user.

**Endpoint:** `POST /api/locations/update`

**Request Body:**

```json
{
    "user_id": "string",
    "latitude": number,
    "longitude": number
}
```

**Response:** `200 OK`

```json
{
    "user_id": "string",
    "latitude": number,
    "longitude": number,
    "last_updated": "datetime"
}
```

**Possible Errors:**

- `400 Bad Request` - Invalid ID format
- `404 Not Found` - User not found
- `500 Internal Server Error` - Server error

### 5. Get User Location

Returns the latest location of a specific user. User must be active.

**Endpoint:** `GET /api/locations/user/{user_id}`

**Response:** `200 OK`

```json
{
    "user_id": "string",
    "latitude": number,
    "longitude": number,
    "last_updated": "datetime"
}
```

**Possible Errors:**

- `400 Bad Request` - Invalid ID format or user not active
- `404 Not Found` - User or location not found
- `500 Internal Server Error` - Server error

## Usage Examples

### Creating a New User

```javascript
const response = await fetch(
  "https://live-location-tracking-backend.vercel.app/api/users/create",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: "john_doe",
    }),
  }
);

const user = await response.json();
// Store user.id for future use
```

### Verifying User (Login)

```javascript
const response = await fetch(
  "https://live-location-tracking-backend.vercel.app/api/users/verify",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "USER_ID_HERE",
    }),
  }
);

const user = await response.json();
```

### Updating User Status

```javascript
const response = await fetch(
  "https://live-location-tracking-backend.vercel.app/api/users/USER_ID_HERE/status",
  {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      is_active: true,
    }),
  }
);

const user = await response.json();
```

### Updating User Location

```javascript
const response = await fetch(
  "https://live-location-tracking-backend.vercel.app/api/locations/update",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "USER_ID_HERE",
      latitude: 32.109333,
      longitude: 34.855499,
    }),
  }
);

const location = await response.json();
```

### Getting User Location

```javascript
const response = await fetch(
  `https://live-location-tracking-backend.vercel.app/api/locations/user/USER_ID_HERE`,
  {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }
);

const location = await response.json();
```

## Implementation Guidelines

### Best Practices

1. **User ID Management:**

   - Securely store the user ID received from user creation
   - Don't expose user IDs in the UI

2. **Location Updates:**

   - Recommended update frequency: every 5-10 seconds during active tracking
   - Validate location data before sending

3. **Error Handling:**

   - Always implement proper error handling on the client side
   - Display user-friendly error messages

4. **Security:**
   - Don't store sensitive information on the client
   - Always use HTTPS
   - Implement appropriate authentication in production

### CORS

The API supports CORS and allows access from all domains (\*). For production use, consider restricting this to specific domains.

## Technical Details

### Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [MongoDB](https://www.mongodb.com/) - NoSQL database
- [Vercel](https://vercel.com/) - Serverless deployment platform
- [Motor](https://motor.readthedocs.io/) - Async MongoDB driver

### Project Structure

```
root_dir/
  ├── main.py           # FastAPI application
  ├── requirements.txt  # Python dependencies
  ├── vercel.json      # Vercel configuration
  ├── routes/
  │   ├── users.py     # User-related endpoints
  │   └── locations.py # Location-related endpoints
  └── .env             # Environment variables
```

## Setup for Development

1. Clone the repository

```bash
git clone [repository-url]
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up environment variables
   Create a `.env` file with:

```env
MONGODB_URL=your_mongodb_url
DB_NAME=your_database_name
```

4. Run the development server

```bash
uvicorn main:app --reload
```

## License

[MIT License](LICENSE)

## Contact

For support or inquiries, please open an issue in the GitHub repository.
