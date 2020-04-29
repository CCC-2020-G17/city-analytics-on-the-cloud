from flask import Flask, request, url_for
import json
from backend import analysis_loader

app = Flask(__name__)

@app.route('/api/statistic', methods=['GET'])
def get_statistic_api():
    # Use For Debug
    def _load(city):
        data_path = "../../data/{}.json".format(city)
        with open(data_path, 'r') as f:
            data = json.load(f)
            return data
    # Current available city: "Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth(WA)"
    def _is_city_valid(city):
        valid_city = {"melbourne", "sydney", "brisbane", "adelaide", "perth"}
        return city in valid_city
    # response
    city = request.args.get('city').lower()
    res = {}
    if _is_city_valid(city):
        res = _load(city)
    return res

if __name__ == '__main__':
    # Use for debug
    # with app.test_request_context('/api/statistic?city=melbourne'):
    #     city = request.args.get('city')
        # statistic_data = analysis_loader.load_city_analysis(city)
    app.run(debug=True, port=3000, host='0.0.0.0')
