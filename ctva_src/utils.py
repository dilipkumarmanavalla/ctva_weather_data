import os
import git
import logging
from datetime import datetime

def clone_repo(config):
    """Clone the repository if it doesn't already exist locally."""
    repo = None
    if not os.path.isdir(config['REPO_PATH']):
        logging.info(f'Cloning repository from {config["REPO_URL"]}...')
        git.Repo.clone_from(config["REPO_URL"], config["REPO_PATH"])
        repo = git.Repo(config["REPO_PATH"])
    return repo

def ingest_data(db, file_path, WeatherData):
    logging.info(f'Starting ingestion for file: {file_path} at {datetime.now()}')
    error_dict = {}
    record_count = 0
    batch_data = []
    try:
        with open(file_path, 'r') as f:
            data = [line.strip().split('\t') for line in f.readlines()]

            for record in data:
                station_id = os.path.basename(file_path).split('.')[0]
                date, max_temp, min_temp, precipitation = record

                # Convert missing data to None
                max_temp = None if max_temp == "-9999" else int(max_temp)
                min_temp = None if min_temp == "-9999" else int(min_temp)
                precipitation = None if precipitation == "-9999" else int(precipitation)

                # Prepare the model instance
                weather_record = WeatherData(
                    station_id=station_id,
                    date=date,
                    max_temp=max_temp,
                    min_temp=min_temp,
                    precipitation=precipitation
                )
                batch_data.append(weather_record)
                record_count += 1

        # Add all the records to the session in one go
        if batch_data:
            try:
                db.session.add_all(batch_data)
                db.session.commit()
                logging.info(f'{record_count} records ingested successfully for file: {file_path}')
            except Exception as db_error:
                db.session.rollback()  # Rollback the session in case of an error
                if 'already exists.' in str(db_error):
                    error_dict['error'] = 'Database Error ->  Might Be No New Records/Data to Update.'
                else:
                    error_dict['error'] = f'Database Error -> {str(db_error)}.'
                logging.error(f'Database error while inserting batch data from file {file_path}: {db_error}')

        logging.info(f'Completed ingestion for file: {file_path} at {datetime.now()}')
    except Exception as e:
        error_dict = {'error': f'Ingest Data Exception -> {str(e)}'}
        logging.error(f'Exception during ingestion for file: {file_path}: {e}')
    return error_dict

def calculate_and_store_stats(db, WeatherStats):
    """Calculate and store weather statistics for each station and year."""
    logging.info(f'Starting statistics calculation at {datetime.now()}')

    try:
        # Query to calculate statistics
        query = '''
            SELECT 
                station_id,
                EXTRACT(YEAR FROM date) as year,
                AVG(NULLIF(max_temp, -9999) / 10.0) as avg_max_temp,
                AVG(NULLIF(min_temp, -9999) / 10.0) as avg_min_temp,
                SUM(NULLIF(precipitation, -9999) / 10.0) as total_precipitation
            FROM weather_data
            GROUP BY station_id, year
        '''

        stats = db.session.execute(query).fetchall()
        stat_count = len(stats)

        # Prepare data for insertion
        for stat in stats:
            station_id, year, avg_max_temp, avg_min_temp, total_precipitation = stat

            # Create or update statistics records
            weather_stat = WeatherStats(
                station_id=station_id,
                year=year,
                avg_max_temp=avg_max_temp,
                avg_min_temp=avg_min_temp,
                total_precipitation=total_precipitation
            )

            # Add to session (this will handle insert or update)
            db.session.merge(weather_stat)

        # Commit the transaction
        db.session.commit()
        logging.info(f'{stat_count} statistics records calculated and stored successfully.')

    except Exception as e:
        db.session.rollback()
        logging.error(f'Exception during statistics calculation: {e}')

    logging.info(f'Completed statistics calculation at {datetime.now()}')

def update_db_new_data(conn, directory, WeatherData, WeatherStats):
    """Update the database with new data files."""
    files = os.listdir(directory)

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        error_dict = ingest_data(conn, file_path, WeatherData)
        if 'error' in error_dict:
            return error_dict

    calculate_and_store_stats(conn, WeatherStats)
    return None
