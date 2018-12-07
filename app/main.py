import etcd
import json
import time
from os import environ as env
import requests

import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)-15s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO}
    },
    root={
        'handlers': ['h'],
        'level': logging.INFO,
    },
)

dictConfig(logging_config)
_logger = logging.getLogger()


def run():

    client = etcd.Client('10.81.0.1', port=2379)

    _logger.info('Prometheus Kontena Service Discovery running')

    address_path = env.get('ADDRESS_PATH', '/kontena/ipam/addresses/kontena')
    filename = env.get('FILE_SD_PATH', '/discovery/kontena_sd.json')
    sleep_time = int(env.get('SLEEP_TIME', 60*5))  # Default = 5 minutes
    ports = env.get('PORTS', '9100,9101').split(',')

    while True:
        try:
            result = client.read(address_path).children
            addresses = sorted([json.loads(r.value)['address'].split('/')[0]
                                for r in result])

            hosts = []
            for address in addresses:
                for port in ports:
                    host = '{}:{}'.format(address, port)
                    try:
                        _logger.debug('Looking for metrics: {}'.format(host))
                        response = requests.get('http://{}/metrics'
                                                .format(host), timeout=3)
                        if response.status_code == 200:
                            _logger.debug('Metrics found: {}'.format(host))
                            hosts.append(host)
                    except requests.exceptions.ConnectionError:
                        pass
                    except requests.exceptions.Timeout:
                        pass

            _logger.info('Found the following hosts: {}'.format(hosts))

            with open(filename, 'w') as f:
                f.write(json.dumps([{'targets': hosts}]))
        except etcd.EtcdConnectionFailed:
            _logger.error('Connection to etcd failed. Waiting for {} seconds '
                          'before next connection attempt.'.format(sleep_time))

        time.sleep(sleep_time)


if __name__ == "__main__":
    run()
