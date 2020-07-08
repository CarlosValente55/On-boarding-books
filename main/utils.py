import logging

logging.basicConfig(
    format='%(asctime)s::%(levelname)s---->%(message)s')
logging.getLogger().setLevel(logging.INFO)


def info_logger(file, iterator, number_of_countries):
    logging.info('File {} || Country {} of {}'.format(
        file, iterator, number_of_countries))


def integrity_error_logger(country, record_reference):
    logging.error("IntegrityError :Country {} is already assigned to book {}.".format(
        country, record_reference))


def data_error_logger():
    logging.error('DataError :One or multiple fields in the wrong format.')


def database_log(errorType, country='', record_reference='', file='', iterator='', number_of_countries=''):
    if errorType == 'IntegrityError':
        integrity_error_logger(country, record_reference)
    elif errorType == 'DataError':
        data_error_logger()
    else:
        info_logger(file, iterator, number_of_countries)
