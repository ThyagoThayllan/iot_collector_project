from iot_collector.mixins import Collector


class InverterCollector(Collector):
    ENDPOINT = '/inversor'


class ProtectionRelayCollector(Collector):
    ENDPOINT = '/rele-protecao'


class SolarMonitoringStationCollector(Collector):
    ENDPOINT = '/estacao-solarimetrica'
