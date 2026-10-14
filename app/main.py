from fastapi import FastAPI, HTTPException

#import CarInput using from .models
from .models import CarInput

app = FastAPI(title="Car Catalogue Api")

CARS = [
    {
        "id": 1,
        "name": "Toyota Corolla",
        "category": "Hatchback",
        "manufacturer": "Toyota",
        "variant": "1.8 Hybrid Design",
        "description": (
            "A compact hybrid hatchback with supportive seats, "
            "easy controls, and a quiet cabin for everyday driving."
        ),
        "tip": "Try the hybrid system in slow traffic during a test drive.",
    },
    {
        "id": 2,
        "name": "Volvo XC60",
        "category": "SUV",
        "manufacturer": "Volvo",
        "variant": "B5 Plus AWD",
        "description": (
            "A comfortable SUV with a spacious cabin. Take a drive "
            "to explore the visibility and relaxed driving position."
        ),
        "tip": "Check the rear seats and boot space before a test drive.",
    },
    {
        "id": 3,
        "name": "Toyota GR86",
        "category": "Coupe",
        "manufacturer": "Toyota",
        "variant": "2.4 Boxer Manual",
        "description": (
            "A compact sports coupe with responsive steering and a set "
            "of simple controls designed around the driver."
        ),
        "tip": "Try the manual gearbox on a varied test-drive route.",
    },
]

# API -> the communication interface between clients and servers
# endpoint -> a specific request / response that a client-server may do

# Health API endpoint
@app.get("/api/health")
def health():
    """Confirm that the application can respond to a 
    request"""
    return {"status":"ok"}


# An endpoint that returns ALL the CARS
@app.get("/api/cars")
def list_cars():
    """Return every car in the catalogue"""
    return CARS

# An API endpoint that will return cars matching the supplied search text and category

@app.get("/api/filter_cars")
def filter_cars(q: str = "", category: str | None = None):
    """Return cars matching the supplied search text and category."""

    # Sanitize user's input 
    # 1 .strip -> remove leading and trailing whitespaces
    # .casefold -> all lowercases

    search_text = q.strip().casefold()
    matching_cars = []

    for car in CARS:
        if category is not None and car["category"] != category:
            continue

        searchable_text = " ".join(
            [
                car["name"],
                car["manufacturer"],
                car["description"]
            ]
        ).casefold()

        if search_text and search_text not in searchable_text:
            continue

        matching_cars.append(car)


    return matching_cars



# An API endpoint that returns Cars based on name

@app.get("/api/car_by_name")
def car_by_name(car_name: str = ""):
    matching_cars = []

    for car in CARS:
        if  car_name == "" or car["name"] == car_name:
            matching_cars.append(car)

    return matching_cars

@app.get("/api/cars/{car_id}")
def get_car(car_id: int):
    """Return one car, or respond with 404 if its ID does not exist."""
    # The value from the URL arrives here as an integer.
    for car in CARS:
        if car["id"] == car_id:             
            return car

    # Reaching this line means we checked every car without finding a match.
    # Raise an HTTP error instead of returning a successful response with no data.
    raise HTTPException(
        status_code=404,
        detail="This car does not exist.",
    )


#POST ENDPOINT - CREATE A CAR
@app.post("/api/cars", status_code=201)
def create_car(car: CarInput):

    next_id = max(
        (car["id"] for car in CARS),
        default=0,
    ) +1

    # Convert the validated Pydantic object into an ordinary python dictionary
    new_car = car.model_dump()

    new_car["id"] = next_id

    CARS.append(new_car)

    return new_car

# PUT method - update a car
@app.put("/api/cars/{car_id}")
def update_car(car_id: int, data: CarInput):
    """Replace a cars content while preserving it's ID"""
    # enumerate() gives us both the list position (index) and the car at that position
    for index, car in enumerate(CARS): 
        if car["id"] == car_id:
            #reuse the same validation rules as the create endpoint.
            updated_car = data.model_dump()

            #Editing the car doesnt/shouldnt change its id
            updated_car["id"] = car_id

            # Replace the existing dictionoary rather than appending one
            CARS[index] = updated_car

            return updated_car

    # Updating a missing car does not create one
    raise HTTPException(
        status_code=404,
        detail="This car doesnt exist."
    )


