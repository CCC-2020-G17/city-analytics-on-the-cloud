from flask import Flask, request, url_for
import json
from back_end import analysis_loader

app = Flask(__name__)

@app.route('/api/statistic', methods=['GET'])
def get_statistic_api():
    # Current available city: "Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth(WA)"
    city = request.args.get('city')
    statistic_data = analysis_loader.load_city_analysis(city)
    return statistic_data

if __name__ == '__main__':
    # Use for debug
    # with app.test_request_context('/api/statistic?city=melbourne'):
    #     print(request.args.get('city'))
    app.run(debug=True, port=3000, host='0.0.0.0')
