import os
import logging
from . import utils


def load_data(repo, config, db, WeatherData, WeatherStats):
    repo.remotes.origin.pull()
    try:
        data_dir = os.path.join(config["REPO_PATH"], config["DATA_FOLDER"])
        logging.info(data_dir)
        if os.path.isdir(data_dir):
            info = utils.update_db_new_data(db, data_dir, WeatherData, WeatherStats)
            if isinstance(info, dict):
                return {'status': 'error', 'message': info['error']}
        return {'status': 'success', 'message': 'The data is up-to-date and all tables are current'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
