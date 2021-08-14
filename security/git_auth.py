from config import config_instance


class GithubAuthDefaults:
    ***REMOVED***

        **GithubAuthDefaults**
            github authentication configuration settings

        **Settings**
            name='github',
            client_id=config_instance.GITHUB_CLIENT_ID,
            client_secret=config_instance.GITHUB_CLIENT_SECRET,
            access_token_url='https://github.com/login/oauth/access_token',
            access_token_params=None,
            authorize_url='https://github.com/login/oauth/authorize',
            authorize_params=None,
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'},

    ***REMOVED***
    def __init__(self):
        self.name = 'github',
        self.client_id = config_instance.GITHUB_CLIENT_ID,
        self.client_secret = config_instance.GITHUB_CLIENT_SECRET,
        self.access_token_url = 'https://github.com/login/oauth/access_token',
        self.access_token_params = None,
        self.authorize_url = 'https://github.com/login/oauth/authorize',
        self.authorize_params = None,
        self.api_base_url = 'https://api.github.com/',
        self.client_kwargs = {'scope': 'user:email'},

    def to_dict(self) -> dict:
        ***REMOVED***
            **to_dict**
                turns class instance into a dict
        :return: configuration settings for github authentication
        ***REMOVED***
        return dict(
            name=self.name, client_id=self.client_id, client_secret=self.client_secret,
            access_token_url=self.access_token_url, authorize_url=self.authorize_url,
            api_base_url=self.api_base_url, client_kwargs=self.client_kwargs)


git_auth_defaults: GithubAuthDefaults = GithubAuthDefaults()