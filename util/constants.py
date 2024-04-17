# util/constants.py

DAYS_OF_YEAR: int = 365

RAIN_SCENES: dict = {
    'no rain (0mm)': 0.0, 
    'slight rain (0mm ~ 5mm)': 5.0, 
    'heavy rain (5mm ~ 15mm)': 15.0, 
    'very heavy rain (> 15mm)': None
}

RAIN_SCENES_WEIGHT: dict = {
    'no rain (0mm)': 1.0, 
    'slight rain (0mm ~ 5mm)': 0.7, 
    'heavy rain (5mm ~ 15mm)': 0.3, 
    'very heavy rain (> 15mm)': 0.0
}

TEMPERATURE_SCENES: dict = {
    'very cold (< 0°)': 0.0, 
    'cold (0° ~ 8°)': 8.0, 
    'cool (8° ~ 15°)': 15.0, 
    'medium (15° ~ 20°)': 20.0, 
    'warm (20° ~ 25°)': 25.0, 
    'hot (25° ~ 30°)': 30.0, 
    'very hot (> 30°)': None
}

TEMPERATURE_SCENES_WEIGHT: dict = {
    'very cold (< 0°)': 0, 
    'cold (0° ~ 8°)': 0.3, 
    'cool (8° ~ 15°)': 0.7, 
    'medium (15° ~ 20°)': 1.0, 
    'warm (20° ~ 25°)': 0.7, 
    'hot (25° ~ 30°)': 0.3, 
    'very hot (> 30°)': 0
}