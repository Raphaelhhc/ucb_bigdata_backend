
from data_collector.rainvolume_collectors import RainVolumeCollector
from data_analyzer.rainvolume_analyzer import RainVolumeAnalyzer

data = {
	"place":"Taiwan",
	"lat":25.0478,
	"lon":121.5319,
	"this_year":2024,
	"past_span":5,
	"day_span":10
}

collector = RainVolumeCollector(
            place=data.get('place'),
            lat=data.get('lat'),
            lon=data.get('lon'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span')
        )

print("create collector!")

collector.collect_rain_volumes()

print("collected rain volumes!")

analyzer = RainVolumeAnalyzer(
            place=data.get('place'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span'),
            day_span=data.get('day_span'),
            rain_volume_lists=collector.get_collect_rain_volumes()
        )

print("create analyzer!")

analyzer.calculate_rain_volume_probabilities()
analyzer.calculate_rain_volume_scores()

print("analyzed!")

probability = analyzer.get_rain_volume_probabilities()
scores = analyzer.get_rain_volume_scores()

print(probability)
print(scores)