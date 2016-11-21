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
            json_auth = json.loads(r.text)['access_token']
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
        post_user_aff_url = self.api_endpoint + "/users/{0}/access_filters".format(user_id)
        r = requests.post(post_user_aff_url, headers={'Authorization': "token " + json_auth['access_token']},data=json.dumps(json_body))
        # print r.status_code

    def update_access_filter_fields(self,json_body,user_id,access_filter_id):
        update_user_url = self.api_endpoint  + "/users/{0}/access_filters/{1}".format(user_id,access_filter_id)
        r = requests.patch(update_user_url, headers={'Authorization': "token " + json_auth['access_token']},data=json.dumps({"access_filters":}))


    def get_models(self,model_name):
        models_url = 'https://learn.looker.com:19999/api/3.0/lookml_models/{0}'.format(model_name)
        all_models = session.get(models_url, headers={'Authorization': "token " + json_auth['access_token']})
        # print "status: " + str(all_models.status_code)
        # print "models: " + all_models.text

    def get_models_explores(self,model_name,explore_name):
        models_url = 'https://learn.looker.com:19999/api/3.0/lookml_models/{0}/explores/{1}'.format(model_name,explore_name)
        all_models = session.get(models_url, headers={'Authorization': "token " + json_auth['access_token']})
