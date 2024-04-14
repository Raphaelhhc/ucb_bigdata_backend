
from data_collector.temperature_collectors import TemperatureCollector
from data_analyzer.temperature_analyzer import TemperatureAnalyzer

data = {
    "place": "Taiwan",
    "lat": 25.0478,
    "lon": 121.5319,
    "this_year": 2024,
    "past_span": 5,
    "day_span": 10
}

collector = TemperatureCollector(
    place=data.get('place'),
    lat=data.get('lat'),
    lon=data.get('lon'),
    this_year=data.get('this_year'),
    past_span=data.get('past_span')
)

print("Created temperature collector!")

collector.collect_temperatures()

print("Collected temperatures!")

analyzer = TemperatureAnalyzer(
    place=data.get('place'),
    this_year=data.get('this_year'),
    past_span=data.get('past_span'),
    day_span=data.get('day_span'),
    temperature_lists=collector.get_collect_temperatures()
)

print("Created temperature analyzer!")

analyzer.calculate_temperature_probabilities()
analyzer.calculate_temperature_scores()

print("Temperature analysis completed!")

probability = analyzer.get_temperature_probabilities()
scores = analyzer.get_temperature_scores()

print("Temperature Probabilities:")
print(probability)
print("Temperature Scores:")
print(scores)
