from flask import Flask, request, url_for
import json
from flask_cors import CORS
from utils import city_info_loader

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/api/statistic', methods=['GET'])
def get_statistic_api():
    # test: http://0.0.0.0:3000/api/statistic?city=melbourne
    city = request.args.get('city').lower()
    return city_info_loader.load_city_info(city)

if __name__ == '__main__':
    # Use for debug
    # with app.test_request_context('/api/statistic?city=melbourne'):
    #     city = request.args.get('city')
        # statistic_data = analysis_loader.load_city_analysis(city)
    app.run(debug=False, port=3000, host='0.0.0.0')
