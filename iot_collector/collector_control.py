from iot_collector.mixins import CollectorControl
from iot_collector.models.models import Device, InverterReading
from iot_collector.models.models import ProtectionRelayReading
from iot_collector.models.models import SolarMonitoringStationReading


class InverterCollectorControl(CollectorControl):
    CATEGORY = Device.Category.INVERTER

    READING_MODEL = InverterReading

    RECEIVED_AND_EXPECTED_FIELDS = {
        'Eday': 'eday',
        'Etotal': 'etotal',
        'Iac': 'iac',
        'Iac1': 'iac1',
        'Iac2': 'iac2',
        'Iac3': 'iac3',
        'Ipv1': 'ipv1',
        'Ipv2': 'ipv2',
        'Ipv3': 'ipv3',
        'Pac': 'pac',
        'Pac1': 'pac1',
        'Pac2': 'pac2',
        'Pac3': 'pac3',
        'Temp': 'temp',
        'Uac': 'uac',
        'Uac1': 'uac1',
        'Uac2': 'uac2',
        'Uac3': 'uac3',
        'Upv1': 'upv1',
        'Upv2': 'upv2',
        'Upv3': 'upv3',
        'cos': 'cos',
        'fac': 'fac',
        'sn': 'serial_number',
        'tsleitura': 'collected_at',
    }

    REQUIRED_FIELDS = ['sn', 'tsleitura', 'Pac']

    @classmethod
    def _has_invalid_data_types(cls, data: dict) -> bool:
        if data['fac'] == 'sessenta_hz':
            return True

        if data['pac'] == 'invalido_kw':
            return True

        if data['uac1'] is None:
            return True

        return False

    @classmethod
    def is_valid(cls, data: dict) -> bool:
        if cls._has_invalid_data_types(data):
            return False

        if cls._is_invalid_values(data):
            return False

        return True

    @classmethod
    def normalize_data(cls, data: dict) -> dict | None:
        if not (data_with_normalized_keys := cls._normalize_data_keys(data)):
            return None

        data_with_normalized_date_fields = cls._normalize_collection_date_field(
            data_with_normalized_keys
        )

        data_with_normalized_date_fields['category'] = cls.CATEGORY

        return data_with_normalized_date_fields


class ProtectionRelayControl(CollectorControl):
    CATEGORY = Device.Category.PROTECTION_RELAY

    READING_MODEL = ProtectionRelayReading

    RECEIVED_AND_EXPECTED_FIELDS = {
        'rFREQ': 'r_freq',
        'rIfaseA': 'r_ifase_a',
        'rIfaseB': 'r_ifase_b',
        'rIfaseC': 'r_ifase_c',
        'rVfaseA': 'r_vfase_a',
        'rVfaseB': 'r_vfase_b',
        'rVfaseC': 'r_vfase_c',
        'rpac': 'r_pac',
        'rpac1': 'r_pac1',
        'rpac2': 'r_pac2',
        'rpac3': 'r_pac3',
        'rtempinterno': 'r_temp_interno',
        'sn': 'serial_number',
        'tpLei': 'tp_lei',
        'tsleitura': 'collected_at',
    }

    REQUIRED_FIELDS = ['sn', 'tsleitura', 'tpLei']

    @classmethod
    def _has_invalid_data_types(cls, data: dict) -> bool:
        if data['r_vfase_a'] == '8155,31':
            return True

        if isinstance(data['r_freq'], list):
            return True

        return False

    @classmethod
    def _normalize_flag_fields(cls, data: dict) -> dict:
        flag_fields = [
            field for field in data if field not in cls.RECEIVED_AND_EXPECTED_FIELDS.values()
        ]

        data['flags'] = {field: data.pop(field) for field in flag_fields}

        return data

    @classmethod
    def is_valid(cls, data: dict) -> bool:
        if cls._has_invalid_data_types(data):
            return False

        if cls._is_invalid_values(data):
            return False

        return True

    @classmethod
    def normalize_data(cls, data: dict) -> dict | None:
        if not (data_with_normalized_keys := cls._normalize_data_keys(data)):
            return None

        data_with_normalized_date_fields = cls._normalize_collection_date_field(
            data_with_normalized_keys
        )

        data_with_normalized_flag_fields = cls._normalize_flag_fields(
            data_with_normalized_date_fields
        )

        data_with_normalized_flag_fields['category'] = cls.CATEGORY

        return data_with_normalized_flag_fields


class SolarMonitoringStationControl(CollectorControl):
    CATEGORY = Device.Category.SOLAR_MONITORING_STATION

    READING_MODEL = SolarMonitoringStationReading

    RECEIVED_AND_EXPECTED_FIELDS = {
        'IrDay': 'ir_day',
        'IrGHI': 'ir_ghi',
        'IrPOA': 'ir_poa',
        'IrTotal': 'ir_total',
        'Umid': 'umid',
        'chuTotal': 'chu_total',
        'dirVento': 'dir_vento',
        'sn': 'serial_number',
        'tempAmb': 'temp_amb',
        'tempMedMod': 'temp_med_mod',
        'tpLei': 'tp_lei',
        'tsleitura': 'collected_at',
        'velVento': 'vel_vento',
    }

    REQUIRED_FIELDS = ['sn', 'tsleitura', 'tpLei']

    @classmethod
    def _has_invalid_data_types(cls, data: dict) -> bool:
        if isinstance(data['vel_vento'], dict):
            return True

        if isinstance(data['ir_ghi'], bool):
            return True

        return False

    @classmethod
    def _normalize_field_values(cls, data: dict) -> dict:
        normalized_data = {}

        for key, value in data.items():
            try:
                normalized_data[key] = float(value)
            except Exception:
                normalized_data[key] = value

        return normalized_data

    @classmethod
    def is_valid(cls, data: dict) -> bool:
        if cls._has_invalid_data_types(data):
            return False

        if cls._is_invalid_values(data):
            return False

        return True

    @classmethod
    def normalize_data(cls, data: dict) -> dict | None:
        if not (data_with_normalized_keys := cls._normalize_data_keys(data)):
            return None

        data_with_normalized_date_fields = cls._normalize_collection_date_field(
            data_with_normalized_keys
        )

        data_with_normalized_float_fields = cls._normalize_field_values(
            data_with_normalized_date_fields
        )

        data_with_normalized_float_fields['category'] = cls.CATEGORY

        return data_with_normalized_float_fields
