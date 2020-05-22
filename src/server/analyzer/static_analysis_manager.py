import os
import json
from configparser import ConfigParser
from analyzer import db_connecter


class staticAnalysisGenerator():

    def __init__(self, city=None):
        self.city = city
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config = ConfigParser()
        self.data_loader = db_connecter.dataLoader(self.city)
        self.suburb_info_json = self.data_loader.load_city_suburb_coordinates()
        self.city_scenarios = ['covid-19','young_twitter_preference', 'tweet_density']
        self.suburb_scenarios = ['income', 'education', 'migration']
        self.scenario_file_young = self.data_loader.load_aus_demographics()
        self.scenario_file_english = self.data_loader.load_aus_language()
        self.scenario_file_income = self.data_loader.load_city_income()
        self.scenario_file_migration = self.data_loader.load_city_migration()
        self.scenario_file_education = self.data_loader.load_city_education()
        self.young_twitter_key_tuples = [('young_people_proportion', 'p_15_24_yrs_pc', 'p_25_34_yrs_pc')]
        self.tweet_density_key_tuples = [('english_mother_tongue_proportion', 'person_tot_spks_eng_only', 'person_tot_tot')]
        self.income_key_tuples = [('low_income_proportion', 'tot_p_inc_wk_p_ov_15_yrs_p_earn_nil_inc_pr100',
                                   'tot_p_inc_wk_p_ov_15_yrs_p_earn_aud1_aud499wk_pr100'),
                                  ('high_income_proportion', 'tot_p_inc_wk_p_ov_15_yrs_p_earn_aud2000_aud2999wk_pr100',
                                   'tot_p_inc_wk_p_ov_15_yrs_p_earn_aud3000_plswk_pr100')]
        self.education_key_pairs = [('complete_yr_12_proportion', 'hi_yr_scl_completed_p15_yrs_ov_completed_yr_12_equivalent_pr100'),
                                    ('post_school_proportion', 'p_post_scl_qualf_p_post_scl_qualification_pr100'),
                                    ('youth_in_study_or_work_proportion', 'yth_engagement_wrk_study_engaged_pr100')]
        self.migration_key_pairs = [('not_english_at_home', 'spks_lang_oth_eng_home_prop_tot_pop_net_mig_pr100'),
                                    ('born_overseas_proportion', 'ovs_brn_pop_prop_tot_pop_tot_brn_ovs_net_mig_pr100'),
                                    ('population_density', 'pop_density_pop_density_p_p_km2')]

        self.load_city_structure()
        self.load_suburbs_structure()

    def load_city_structure(self):
        """
        Load result structure for city level analysis
        """
        self.config.read(self.structure_file)
        self.analysis_result = json.loads(self.config.get('FIRST-LAYER', 'CITY'))
        self.analysis_result['city_name'] = self.city.capitalize()
        for scenario in self.city_scenarios:
            self.analysis_result[scenario] = json.loads(self.config.get('SECOND-LAYER', scenario.upper()))
        self.polygon_dict = None
        self.add_young_people_proportion()
        self.add_english_speaker_proportion()
        # self.add_crime_index()


    def load_suburbs_structure(self):
        """
        Load result structure for suburb level analysis
        """
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
            for scenario in self.suburb_scenarios:
                self.analysis_result['suburbs'][suburb][scenario] = json.loads(self.config.get('THIRD-LAYER', scenario.upper()))
            self.add_income(suburb)
            self.add_migration(suburb)
            self.add_education(suburb)

    def add_young_people_proportion(self):
        try:
            city_dict = self.scenario_file_young['features']['Greater {}'.format(self.city.capitalize())]
            for tuple in self.young_twitter_key_tuples:
                self.analysis_result['young_twitter_preference'][tuple[0]] \
                    = city_dict[tuple[1]] + city_dict[tuple[2]]
        except Exception as e:
            print(e)

    def add_english_speaker_proportion(self):
        try:
            city_dict = self.scenario_file_english['features']['Greater {}'.format(self.city.capitalize())]
            for tuple in self.tweet_density_key_tuples:
                self.analysis_result['tweet_density'][tuple[0]] \
                    = round((city_dict[tuple[1]] / city_dict[tuple[2]])*100, 1)
        except Exception as e:
            print(e)

    def add_crime_index(self):
        with open('{}/analyzer/static_result.json'.format(os.path.pardir)) as f:
            city_crime_index = json.load(f)
        self.analysis_result['crime']['crime_index'] = city_crime_index[self.city]['crime_index']

    def reset_crime_index(self):
        self.analysis_result['crime']['crime_index'] = 0

    def add_income(self, suburb):
        try:
            suburb_dict = self.scenario_file_income['suburbs'][suburb]
            for tuple in self.income_key_tuples:
                self.analysis_result['suburbs'][suburb]['income'][tuple[0]] = suburb_dict[tuple[1]] + suburb_dict[tuple[2]]
        except:
            # print('Exception: add_income', suburb)
            pass

    def reset_income(self):
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            for tuple in self.income_key_tuples:
                self.analysis_result['suburbs'][suburb]['income'][tuple[0]] = 0

    def add_education(self, suburb):
        try:
            suburb_dict = self.scenario_file_education['suburbs'][suburb]
            for pair in self.education_key_pairs:
                self.analysis_result['suburbs'][suburb]['education'][pair[0]] = suburb_dict[pair[1]]
        except:
            # print('Exception: add_education', suburb)
            pass

    def reset_education(self):
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            for pair in self.education_key_pairs:
                self.analysis_result['suburbs'][suburb]['education'][pair[0]] = 0

    def add_migration(self, suburb):
        try:
            suburb_dict = self.scenario_file_migration['suburbs'][suburb]
            for pair in self.migration_key_pairs:
                self.analysis_result['suburbs'][suburb]['migration'][pair[0]] = suburb_dict[pair[1]]
        except:
            # print('Exception: add_migration', suburb)
            pass

    def reset_migration(self):
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            for pair in self.migration_key_pairs:
                self.analysis_result['suburbs'][suburb]['migration'][pair[0]] = 0

    def add_static_data_to_db(self):
        db_connecter.analysisResultSaver(self.city).update_analysis(self.analysis_result, type='add')


if __name__ == '__main__':
    cities = [ "Brisbane"]
    for city in cities:
        city = city.split(" ")[0].lower()
        generator = staticAnalysisGenerator(city)
        # generator.add_static_data_to_db()
        # db_connecter.analysisResultSaver(city).reset_static_result()


