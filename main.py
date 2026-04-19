import logging
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from iot_collector.collector import InverterCollector
from iot_collector.collector import ProtectionRelayCollector
from iot_collector.collector import SolarMonitoringStationCollector
from iot_collector.collector_control import InverterCollectorControl
from iot_collector.collector_control import ProtectionRelayControl
from iot_collector.collector_control import SolarMonitoringStationControl
from iot_collector.database import Database


log = logging.getLogger(__name__)


def run_collector(collector_class, collector_control) -> None:
    collector = collector_class(collector_control)

    try:
        data = collector.get_data()
    except Exception as exc:
        log.exception(f'An error occurred while collecting {collector_class.__name__}: {exc}')
        return None

    if not data:
        return None

    database = Database()

    try:
        collector_control.save(data=data, database=database)
    except Exception as exc:
        log.exception(f'An error occurred while saving {collector_class.__name__}: {exc}')
        return None

    log.info(f'{collector_class.__name__} collected succesfully!')


scheduler = BackgroundScheduler()


collectors = [
    (InverterCollector, InverterCollectorControl),
    (ProtectionRelayCollector, ProtectionRelayControl),
    (SolarMonitoringStationCollector, SolarMonitoringStationControl),
]


for collector_class, collector_control in collectors:
    scheduler.add_job(
        run_collector,
        'interval',
        args=[collector_class, collector_control],
        coalesce=True,
        max_instances=1,
        seconds=1,
    )


scheduler.start()


while True:
    sleep(1)
