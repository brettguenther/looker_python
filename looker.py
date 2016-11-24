class LookerAPI(object):
    """Class to contain methods and variables related to looker API authentication and Requests
    """
    def __init__(self, api_info):
        """api_info is a dictionary that contains information related to the specific looker instance"""
        self.api_endpoint = api_info['api_endpoint']
        self.client_secret = api_info['client_secret']
        self.client_id = api_info['client_id']
        self.login_endpoint = api_info['login_url']

    def login(self):
        """login to looker API"""
        try:
            auth_data = {'client_id':self.client_id, 'client_secret':self.client_secret}
            r = requests.post( self.login_endpoint,data=auth_data) # error handle here
            json_auth = r.json()['access_token']
            return json_auth
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def run_look(self, look_id, json_auth,return_format='csv'):
        """run look and return as csv, need to add more formats here"""
        try:
            look_run_url = self.api_endpoint + '/looks/{0}/run/{1}'.format(look_id,return_format)
            r = requests.get(look_run_url, headers={'Authorization': "token " + json_auth})
            return r.text
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def run_query(self, query_id, json_auth,return_format='csv'):
        """run query and return as csv, need to add more formats here"""
        try:
            query_run_url = self.api_endpoint + '/queries/{0}/run/{1}'.format(query_id,return_format)
            r = requests.get(look_run_url, headers={'Authorization': "token " + json_auth})
            return r.text
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def sql_query(self, sql_query_slug, json_auth, return_format='csv'):
        """Run arbitrary query based on model and return results"""
        try:
            query_run_url = self.api_endpoint + '/sql_queries/{0}'.format(sql_query_slug)
            r = requests.get(query_run_url, headers={'Authorization': "token " + json_auth})
            return r
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def sql_query_post(self, sql_query_body, json_auth):
        """Run arbitrary query based on model and return results"""
        try:
            query_run_url = self.api_endpoint + '/sql_queries'
            r = requests.post(query_run_url, headers={'Authorization': "token " + json_auth}, data=sql_query_body)
            return r
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def post_prefetch(self, dashboard_id, body, json_auth):
        """Run arbitrary query based on model and return results"""
        try:
            dashboard_url = self.api_endpoint + "/dashboards/{0}".format(dashboard_id)
            prefetch_dash_url = self.api_endpoint + "/dashboards/{0}/prefetch".format(dashboard_id)
            dashboard_patch = requests.patch(dashboard_url, headers={'Authorization': "token " + json_auth},data=json.dumps({"load_configuration":"prefetch_cache_run"}))
            prefetch_req = requests.post(prefetch_dash_url, headers={'Authorization': "token " + json_auth}, data=json.dumps(body))
            return dashboard_patch.text, prefetch_req.text
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def create_access_filter_fields(self,json_body,user_id):
        """
           create access filter fields for a user
            example body: {"field": "blank.test3","value": "1","model": "brettg_testing"}
        """
        try:
            post_user_aff_url = self.api_endpoint + "/users/{0}/access_filters".format(user_id)
            r = requests.post(post_user_aff_url, headers={'Authorization': "token " + json_auth['access_token']},data=json.dumps(json_body))
        except requests.exceptions.RequestException as e:
            logger.error(e)
    def update_access_filter_fields(self,json_body,user_id,access_filter_id):
        try:
            update_user_url = self.api_endpoint  + "/users/{0}/access_filters/{1}".format(user_id,access_filter_id)
            r = requests.patch(update_user_url, headers={'Authorization': "token " + json_auth['access_token']},data=json.dumps({"access_filters":json_body}))
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def get_models(self,model_name):
        try:
            models_url = self.api_endpoint + "/lookml_models/{0}".format(model_name)
            all_models = requests.get(models_url, headers={'Authorization': "token " + json_auth['access_token']})
            return all_models
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def get_models_explores(self,model_name,explore_name):
        try:
            explore_url = self.api_endpoint + "/lookml_models/{0}/explores/{1}".format(model_name,explore_name)
            explore_info = requests.get(models_url, headers={'Authorization': "token " + json_auth['access_token']})
            return explore_info
        except requests.exceptions.RequestException as e:
            logger.error(e)

def ConfigSectionMap(section):
    import ConfigParser
    Config = ConfigParser.ConfigParser()
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                logger.debug("skip: %s" % option)
        except:
            logger.warn("exception on %s!" % option)
            dict1[option] = None
    return dict1

def logger_initialize(log_suffix):
    """
    include a suffix to append to log names
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(str(time.strftime("%d_%m_%Y")) + log_suffix + ".log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def test(config_section_name,look_id):
    logger_initialize("looker_api")
    looker_api = LookerAPI(ConfigSectionMap(config_section_name))
    json_auth = looker_api.login()
    look_response = looker_api.run_look(look_id,json_auth)
