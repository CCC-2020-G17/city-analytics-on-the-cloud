import os
import json
from configparser import ConfigParser
from analyzer import db_connecter


class staticAnalysisGenerator():

    def __init__(self, city=None):
        self.city = city
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config = ConfigParser()
        self.suburb_info_json = db_connecter.dataLoader(self.city).load_city_suburb_coordinates()
        self.scenarios = ['covid-19', 'crime', 'econ', 'offence']
        self.load_city_structure()
        self.load_suburbs_structure()

    def load_city_structure(self):
        """
        Load result structure for city level analysis
        """
        self.config.read(self.structure_file)
        self.analysis_result = json.loads(self.config.get('FIRST-LAYER', 'CITY'))
        self.analysis_result['city_name'] = self.city
        for scenario in self.scenarios:
            self.analysis_result[scenario] = json.loads(self.config.get('SECOND-LAYER', scenario.upper()))
        self.polygon_dict = None


    def load_suburbs_structure(self):
        """
        Load result structure for suburb level analysis
        :return:
        """
        # suburb_json_file = '{}/suburbs/{}_suburbs.json'.format(os.path.pardir, self.city)
        # with open(suburb_json_file) as f:
        #     suburb_info_json = json.load(f)
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
            for scenario in self.scenarios:
                self.analysis_result['suburbs'][suburb][scenario] = json.loads(self.config.get('THIRD-LAYER', scenario.upper()))

    def add_crime_index(self):
        with open('{}/analyzer/static_result.json'.format(os.path.pardir)) as f:
            city_crime_index = json.load(f)
        self.analysis_result['crime']['crime_index'] = city_crime_index[self.city]['crime_index']

    def reset_crime_index(self):
        self.analysis_result['crime']['crime_index'] = 0

    def add_income(self):
        pass

    def add_migrationn(self):
        pass

    def add_mental_health(self):
        pass


if __name__ == '__main__':
    city = 'melbourne'
    generator = staticAnalysisGenerator(city)
    # TODO: Only load once. Or check duplication.
    generator.add_crime_index()
    generator.reset_crime_index()
    db_connecter.analysisResultSaver(city).update_analysis(generator.analysis_result)
    db_connecter.analysisResultSaver(city).reset_static_result()


