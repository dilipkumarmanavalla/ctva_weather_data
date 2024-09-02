class Dev:
    config = {
    'DB_USER': 'ctva',
    'DB_PASSWORD': 'ctva',
    'DB_HOST': 'db',
    'DB_NAME': 'weather_db',
    'SQLALCHEMY_TRACK_MODIFICATIONS':False,
    'REPO_URL': 'https://github.com/corteva/code-challenge-template',
    'REPO_PATH': '/ctva_data',
    'DATA_FOLDER': 'wx_data',
}


class Prod:
    config = {
    'DB_USER': 'prod_ctva',
    'DB_PASSWORD': 'prod_ctva',
    'DB_HOST': 'db',
    'DB_NAME': 'weather_db',
    'SQLALCHEMY_TRACK_MODIFICATIONS':False,
    'REPO_URL': 'https://github.com/corteva/code-challenge-template',
    'REPO_PATH': '/ctva_data',
    'DATA_FOLDER': 'wx_data',
}
def load_settings(env):
    if env.lower()=='local' or env.lower()=='test':
        return Dev.config
    if env.lower()=='prod':
        return Prod.config
    return Dev.config