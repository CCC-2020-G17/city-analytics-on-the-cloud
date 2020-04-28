import os
import json
from configparser import ConfigParser


class staticAnalysisGenerator():

    def __init__(self, city=None):
        self.city = city
        self.config = ConfigParser()
        self.load_city_structure()
        self.load_suburbs_structure()

    def load_city_structure(self):
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config.read(self.structure_file)
        self.analysis_result = json.loads(self.config.get('FIRST-LAYER', 'CITY'))
        self.analysis_result['city_name'] = self.city
        # self.analysis_result['covid-19'] = json.loads(self.config.get('SECOND-LAYER', 'COVID-19'))
        # self.analysis_result['crime'] = json.loads(self.config.get('SECOND-LAYER', 'CRIME'))
        self.analysis_result['econ'] = json.loads(self.config.get('SECOND-LAYER', 'ECON'))
        self.analysis_result['offence'] = json.loads(self.config.get('SECOND-LAYER', 'OFFENCE'))
        self.polygon_dict = None

    def load_suburbs_structure(self):
        suburb_json_file = '{}/suburbs/{}_suburbs.json'.format(os.path.pardir, self.city)
        with open(suburb_json_file) as f:
            suburb_info_json = json.load(f)
        for feature in suburb_info_json['features']:
            suburb = feature['properties']['name']
            self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
            self.analysis_result['suburbs'][suburb]['econ'] = json.loads(self.config.get('THIRD-LAYER', 'ECON'))
            self.analysis_result['suburbs'][suburb]['offence'] = json.loads(self.config.get('THIRD-LAYER', 'OFFENCE'))


if __name__ == '__main__':
    city = 'melbourne'
    generator = staticAnalysisGenerator(city)
    print(generator.analysis_result)
    with open('{}_static_result.json'.format(city), 'w') as f:
        json.dump(generator.analysis_result, f, indent=3)


