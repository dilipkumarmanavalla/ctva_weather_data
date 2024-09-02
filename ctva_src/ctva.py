import os
import logging
from . import utils

def get_weather_data(request, DataModel, stats=False):
    station_id = request.args.get('station_id')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    query = DataModel.query
    if stats:
        filter_attr = 'year'
        date_value = request.args.get('year')
    else:
        filter_attr = 'date'
        date_value = request.args.get('date')


    if station_id:
        query = query.filter_by(station_id=station_id)
    if date_value:
        query = query.filter_by(**{filter_attr: date_value})

    paginated_data = query.paginate(page, per_page, False)
    data = paginated_data.items

    if stats:
        response_data = [{
            'station_id': s.station_id,
            'year': s.year,
            'avg_max_temp': s.avg_max_temp,
            'avg_min_temp': s.avg_min_temp,
            'total_precipitation': s.total_precipitation
        } for s in data]
    else:
        response_data = [{
            'station_id': d.station_id,
            'date': d.date.isoformat() if d.date else None,
            'max_temp': d.max_temp,
            'min_temp': d.min_temp,
            'precipitation': d.precipitation
        } for d in data]

    response = {
        'page': paginated_data.page,
        'per_page': paginated_data.per_page,
        'total': paginated_data.total,
        'total_pages': paginated_data.pages,
        'data': response_data
    }

    return response

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

