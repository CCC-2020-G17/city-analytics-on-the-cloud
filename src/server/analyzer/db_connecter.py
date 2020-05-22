import os
import numbers
from couchDB import db_util
from configparser import ConfigParser


tweet_db = "tweets_mixed"
analysis_result_db = "analysis_results"


def _couchdb_get_url(section='DEFAULT', verbose=False):
    global config
    config = ConfigParser()
    url_file = '{}/config/server.url.cfg'.format(os.path.pardir)
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


class dataLoader():

    def __init__(self, city=None):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def load_tweet_data(self):
        """
        Load all data from given city
        :return:
        """
        db = db_util.cdb(self.serverURL, tweet_db)
        city_key = self.city
        return  db.getByCity(city_key)

    def load_period_tweet_data(self, start_ts, end_ts):
        db = db_util.cdb(self.serverURL, tweet_db)
        cityData = db.getByBlock(start_ts=start_ts, end_ts=end_ts, cityname=self.city)
        return cityData

    def load_city_suburb_coordinates(self):
        if self.city:
            city_key = "{}_suburbs".format(self.city.lower())
            db = db_util.cdb(self.serverURL, "aurin")
            return db.getByKey(city_key)
        else:
            return None

    def load_aus_demographics(self):
        key = "australia_demographics"
        db = db_util.cdb(self.serverURL, "aurin")
        return db.getByKey(key)


    def load_aus_language(self):
        key = "australia_languages"
        db = db_util.cdb(self.serverURL, "aurin")
        return db.getByKey(key)

    def load_city_income(self):
        if self.city:
            city_key = "{}_income".format(self.city.lower())
            db = db_util.cdb(self.serverURL, "aurin")
            return db.getByKey(city_key)
        else:
            return None

    def load_city_migration(self):
        if self.city:
            city_key = "{}_migration".format(self.city.lower())
            db = db_util.cdb(self.serverURL, "aurin")
            return db.getByKey(city_key)
        else:
            return None

    def load_city_education(self):
        if self.city:
            city_key = "{}_education".format(self.city.lower())
            db = db_util.cdb(self.serverURL, "aurin")
            return db.getByKey(city_key)
        else:
            return None

    def load_analysis(self):
        if self.city:
            db = db_util.cdb(self.serverURL, analysis_result_db)
            city_key = "{}_analysis_result".format(self.city.lower())
            return db.getByKey(city_key)
        else:
            return None


class analysisResultSaver():

    def __init__(self, city=None):
        self.serverURL = _couchdb_get_url()
        self.city = city
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

    def save_analysis(self, analysis_result):
        """
        Save analysis result to database. This will replace the document with the same id.
        """
        db = db_util.cdb(self.serverURL, analysis_result_db)
        analysis_city_id = "{}_analysis_result".format(self.city.lower())
        db.put(analysis_result, analysis_city_id)

    def update_helper(self, renewal, existing,  type):
        # TODO: Add special pattern for updating night tweet proportion and tweet frequency
        if not isinstance(renewal, dict) or not isinstance(existing, dict):
            if isinstance(renewal, str) and isinstance(existing, str):
                return existing
            elif isinstance(renewal, numbers.Number) and isinstance(existing, numbers.Number):
                if type == 'add':
                    return sum([renewal, existing])
                elif type == 'replace':
                    return renewal
            elif renewal is None or existing is None:
                return existing
        for key in existing:
            if key in renewal:
                renewal[key] = self.update_helper(renewal[key], existing[key], type)
            else:
                renewal[key] = existing[key]
        return renewal

    def update_analysis(self, renewal, type='add'):
        """
        Update the analysis result. Can be add to or replace the values of certain keys.
        """
        existing = dataLoader(self.city).load_analysis()
        new_result = self.update_helper(renewal, existing, type)
        self.save_analysis(new_result)

    def reset_static_result(self):
        """
        Reset static result in result database. In case static modules are loaded for multiple times.
        """
        existing = dataLoader(self.city).load_analysis()
        new_result = existing
        for tuple in self.young_twitter_key_tuples:
            new_result['young_twitter_preference'][tuple[0]] = 0
        for tuple in self.tweet_density_key_tuples:
            new_result['tweet_density'][tuple[0]] = 0
        for suburb in new_result['suburbs'].keys():
            for tuple in self.income_key_tuples:
                new_result['suburbs'][suburb]['income'][tuple[0]] = 0
            for tuple in self.education_key_pairs:
                new_result['suburbs'][suburb]['education'][tuple[0]] = 0
            for tuple in self.migration_key_pairs:
                new_result['suburbs'][suburb]['migration'][tuple[0]] = 0
        self.save_analysis(new_result)

if __name__ == '__main__':
    city = 'melbourne'
    start_ts = '1588256300'
    end_ts = '1588256400'
    print(dataLoader(city).load_period_tweet_data(start_ts, end_ts))



