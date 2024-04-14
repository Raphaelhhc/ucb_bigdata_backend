
from data_collector.rainvolume_collectors import RainVolumeCollector
from data_analyzer.rainvolume_analyzer import RainVolumeAnalyzer
from data_collector.temperature_collectors import TemperatureCollector
from data_analyzer.temperature_analyzer import TemperatureAnalyzer
from data_analyzer.recommend_analyzer import RecommendAnalyzer

data = {
    "place": "Taiwan",
    "lat": 25.0478,
    "lon": 121.5319,
    "this_year": 2024,
    "past_span": 5,
    "day_span": 10
}

rain_collector = RainVolumeCollector(
            place=data.get('place'),
            lat=data.get('lat'),
            lon=data.get('lon'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span')
        )

print("create rain collector!")

rain_collector.collect_rain_volumes()

print("collected rain volumes!")

rain_analyzer = RainVolumeAnalyzer(
            place=data.get('place'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span'),
            day_span=data.get('day_span'),
            rain_volume_lists=rain_collector.get_collect_rain_volumes()
        )

print("create rain analyzer!")

rain_analyzer.calculate_rain_volume_probabilities()
rain_analyzer.calculate_rain_volume_scores()

print("rain data analyzed!")

rain_probabilities = rain_analyzer.get_rain_volume_probabilities()
rain_scores = rain_analyzer.get_rain_volume_scores()

print("rain probabilities and scores generated!")

temp_collector = TemperatureCollector(
    place=data.get('place'),
    lat=data.get('lat'),
    lon=data.get('lon'),
    this_year=data.get('this_year'),
    past_span=data.get('past_span')
)

print("Created temperature collector!")

temp_collector.collect_temperatures()

print("Collected temperatures!")

temp_analyzer = TemperatureAnalyzer(
    place=data.get('place'),
    this_year=data.get('this_year'),
    past_span=data.get('past_span'),
    day_span=data.get('day_span'),
    temperature_lists=temp_collector.get_collect_temperatures()
)

print("Created temperature analyzer!")

temp_analyzer.calculate_temperature_probabilities()
temp_analyzer.calculate_temperature_scores()

print("Temperature analysis completed!")

temp_probabilities = temp_analyzer.get_temperature_probabilities()
temp_scores = temp_analyzer.get_temperature_scores()

print("temperature probabilities and scores generated!")

recommend_analyzer = RecommendAnalyzer(
    place=data.get('place'),
    this_year=data.get('this_year'),
    past_span=data.get('past_span'),
    day_span=data.get('day_span'),
    rain_volume_probabilities=rain_probabilities,
    temperature_probabilities=temp_probabilities,
    rain_volume_scores=rain_scores,
    temperature_scores=temp_scores
)

print("Created recommend analyzer!")

recommend_analyzer.calculate_recommend_date()

print("Recommend scores generated!")

recommend_date = recommend_analyzer.get_recommend_date()
recommend_date_probability = recommend_analyzer.get_recommend_date_probability()

print("Recommend date generated!")
print(recommend_date)
print(recommend_date_probability)