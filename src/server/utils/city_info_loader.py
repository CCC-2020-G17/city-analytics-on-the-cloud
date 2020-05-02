import json
from backend import analysis_loader

def _load_geo(city):
    data_path = "suburbs/{}_suburbs.json".format(city)
    with open(data_path, 'r') as f:
        data = json.load(f)
        return data

def _load_analysis(city):
    data = analysis_loader.load_city_analysis(city)
    return data

def _is_city_valid(city):
    # Current available city: "Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth(WA)"
    valid_city = {"melbourne", "sydney", "brisbane", "adelaide", "perth"}
    return city in valid_city

def _get_merge_data(city):
    geo_data = _load_geo(city)
    analysis_data = _load_analysis(city)
    for suburb in geo_data['features']:
        try:
            suburb_name = suburb['properties']['name']
            suburb_analysis = analysis_data['suburbs'][suburb_name]
            suburb['properties']['analysis_result'] = suburb_analysis
        except Exception as e:
            # Ignore but print the error
            print('Error from utils/city_info_loader.py: ',e)
    return geo_data
            

def load_city_info(city):
    """
    Load city information with both geographic information and analysis
    :param string City name (Melbourne, Sydney, Brisbane, Adelaide, Perth)
    :return dict City information
    """
    res = {}
    if _is_city_valid(city):
        res = _get_merge_data(city)
    return res

