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
swag_config = {
    '/api/weather':{
    'summary': 'Get weather data',
    'parameters': [
        {'name': 'station_id', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Filter by station ID'},
        {'name': 'date', 'in': 'query', 'type': 'string', 'format': 'date', 'required': False, 'description': 'Filter by date (YYYY-MM-DD)'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1, 'required': False, 'description': 'Page number for pagination'},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 10, 'required': False, 'description': 'Number of items per page'}
    ],
    'responses': {
        '200': {
            'description': 'A list of weather data',
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'},
                    'total': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'station_id': {'type': 'string'},
                                'date': {'type': 'string', 'format': 'date'},
                                'max_temp': {'type': 'integer'},
                                'min_temp': {'type': 'integer'},
                                'precipitation': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
},
    '/api/weather/stats':{
    'summary': 'Get weather statistics',
    'parameters': [
        {'name': 'station_id', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Filter by station ID'},
        {'name': 'year', 'in': 'query', 'type': 'integer', 'required': False, 'description': 'Filter by year'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1, 'required': False, 'description': 'Page number for pagination'},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 10, 'required': False, 'description': 'Number of items per page'}
    ],
    'responses': {
        '200': {
            'description': 'A list of weather statistics',
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'},
                    'total': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'station_id': {'type': 'string'},
                                'year': {'type': 'integer'},
                                'avg_max_temp': {'type': 'number'},
                                'avg_min_temp': {'type': 'number'},
                                'total_precipitation': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        }
    }
}
}

def load_settings(env):
    if env.lower()=='local' or env.lower()=='test':
        return Dev.config, swag_config
    if env.lower()=='prod':
        return Prod.config, swag_config
    return Dev.config, swag_config