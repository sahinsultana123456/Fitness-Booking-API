````
# Fitness Studio Booking API

A simple Django REST API to view and book fitness classes (like Yoga, Zumba, and HIIT).

---

## Features

- View upcoming fitness classes  
- Book a class using name and email  
- Check all bookings by your email  
- Prevents overbooking  
- Timezone handled (IST)  

---

## Setup Instructions

### 1. Clone the repository or download the ZIP

```bash
git clone https://github.com/sahinsultana123456/Fitness-Booking-API.git
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the server

```bash
python manage.py runserver
```

---

## API Endpoints

### GET `/classes/`

Returns a list of upcoming fitness classes.

**Response example:**

```json
[
    {
        "id": 2,
        "name": "Advanced yoga training program",
        "date_time": "2025-06-11 07:00:00 IST",
        "instructor": {
            "id": 2,
            "name": "Arohi Mishra",
            "email": "arohi@email.com",
            "bio": "Professional yoga trainer",
            "profile_picture": ""
        },
        "difficulty": "Advanced",
        "total_slots": 2,
        "available_slots": 0
    },
    {
        "id": 1,
        "name": "Begginers yoga classes",
        "date_time": "2025-06-16 06:00:00 IST",
        "instructor": {
            "id": 1,
            "name": "Riya Patra",
            "email": "riya@email.com",
            "bio": "5+ years of experience in Yoga",
            "profile_picture": ""
        },
        "difficulty": "Beginner",
        "total_slots": 20,
        "available_slots": 19
    },
  
]
```

---

### POST `/book/`

Book a spot in a fitness class.

**Request body:**

```json
{
  "class_id": 3,
  "client_name": "John Doe",
  "client_email": "john@email.com"
}
```

**Response on success:**

```json
{
    "id": 6,
    "fitness_class": {
        "id": 3,
        "name": "Morning Yoga Practice",
        "date_time": "2025-06-18 08:00:00 IST",
        "instructor": {
            "id": 2,
            "name": "Arohi Mishra",
            "email": "arohi@email.com",
            "bio": "Professional yoga trainer",
            "profile_picture": ""
        },
        "difficulty": "Intermediate",
        "total_slots": 15,
        "available_slots": 13
    },
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "booked_at": "2025-06-07T00:42:47.885043+05:30"
}
```

---

### GET `/bookings/`

Get all bookings made by a specific email address.

**Request URL example:**

http://127.0.0.1:8000/api/bookings?email=john@example.com

**Response example:**

```json
[
    {
        "id": 6,
        "fitness_class": {
            "id": 3,
            "name": "Morning Yoga Practice",
            "date_time": "2025-06-18 08:00:00 IST",
            "instructor": {
                "id": 2,
                "name": "Arohi Mishra",
                "email": "arohi@email.com",
                "bio": "Professional yoga trainer",
                "profile_picture": ""
            },
            "difficulty": "Intermediate",
            "total_slots": 15,
            "available_slots": 13
        },
        "client_name": "John Doe",
        "client_email": "john@example.com",
        "booked_at": "2025-06-07T00:42:47.885043+05:30"
    }
]
```

---


## Author

Developed by \[Sahin Sultana]
For demonstration and evaluation purposes only.

---

## License

This project is open-source and free to use for educational purposes.

```

---

```
