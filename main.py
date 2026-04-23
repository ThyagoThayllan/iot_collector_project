import logging
from datetime import datetime
from datetime import timedelta
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from iot_collector.collector import InverterCollector
from iot_collector.collector import ProtectionRelayCollector
from iot_collector.collector import SolarMonitoringStationCollector
from iot_collector.collector_control import InverterCollectorControl
from iot_collector.collector_control import ProtectionRelayControl
from iot_collector.collector_control import SolarMonitoringStationControl
from iot_collector.database import Database
from iot_collector.mixins import Collector
from iot_collector.mixins import CollectorControl


log = logging.getLogger(__name__)

COLLECTION_INTERVAL = 60 * 5

TIME_LIMIT = datetime.now() + timedelta(hours=1)


def run_collector(
    collector_class: Collector, collector_control: CollectorControl, database: Database
) -> None:
    collector = collector_class(collector_control)

    try:
        data = collector.get_data()
    except Exception as exc:
        log.exception(f'An error occurred while collecting {collector_class.__name__}: {exc}')
        return None

    if not data:
        return None

    try:
        collector_control.save(data=data, database=database)
    except Exception as exc:
        log.exception(f'An error occurred while saving {collector_class.__name__}: {exc}')
        return None

    print(f'{collector_class.__name__} collected succesfully!')


def main() -> None:
    collectors = [
        (InverterCollector, InverterCollectorControl),
        (ProtectionRelayCollector, ProtectionRelayControl),
        (SolarMonitoringStationCollector, SolarMonitoringStationControl),
    ]

    database = Database()

    scheduler = BackgroundScheduler()

    for collector_class, collector_control in collectors:
        scheduler.add_job(
            run_collector,
            'interval',
            args=[collector_class, collector_control, database],
            coalesce=True,
            max_instances=1,
            next_run_time=datetime.now(),
            seconds=COLLECTION_INTERVAL,
        )

    scheduler.start()

    while datetime.now() < TIME_LIMIT:
        sleep(1)

    scheduler.shutdown(wait=True)

    print('Collection completed!')


if __name__ == '__main__':
    main()
