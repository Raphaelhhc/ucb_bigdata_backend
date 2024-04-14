# package: util
# constants.py

DAYS_OF_YEAR: int = 365

RAIN_SCENES: dict = {
    'no rain': 0.0, 
    'slight rain': 5.0, 
    'heavy rain': 15.0, 
    'very heavy rain': None
}

RAIN_SCENES_WEIGHT: dict = {
    'no rain': 1.0, 
    'slight rain': 0.7, 
    'heavy rain': 0.3, 
    'very heavy rain': 0.0
}

TEMPERATURE_SCENES: dict = {
    'very cold': 0.0, 
    'cold': 8.0, 
    'cool': 15.0, 
    'medium': 20.0, 
    'warm': 25.0, 
    'hot': 30.0, 
    'very hot': None
}

TEMPERATURE_SCENES_WEIGHT: dict = {
    'very cold': 0, 
    'cold': 0.3, 
    'cool': 0.7, 
    'medium': 1.0, 
    'warm': 0.7, 
    'hot': 0.3, 
    'very hot': 0
}