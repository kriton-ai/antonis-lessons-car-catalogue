from fastapi import FastAPI

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