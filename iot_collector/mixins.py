import logging
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from http import HTTPStatus
from typing import Type

import requests
from sqlalchemy import select

from iot_collector.database import Database
from iot_collector.models.mixins import ReadingBase
from iot_collector.models.models import Device


log = logging.getLogger(__name__)

MAX_RETRIES = 5


class Collector(ABC):
    BASE_URL = 'http://127.0.0.1:5050'

    ENDPOINT: str

    def __init__(self, collector_control: CollectorControl) -> None:
        self.collector_control = collector_control

    def get_data(self) -> dict | None:
        url = self.BASE_URL + self.ENDPOINT

        for _ in range(1, MAX_RETRIES + 1):
            try:
                request = requests.get(url)
            except Exception:
                continue

            if request.status_code != HTTPStatus.OK:
                continue

            try:
                data = request.json()
            except Exception:
                continue

            if not (normalized_data := self.collector_control.normalize_data(data)):
                continue

            if self.collector_control.is_valid(normalized_data):
                return normalized_data

        log.error(f'An error occurred while collecting {self.__class__.__name__}')
        return None


class CollectorControl(ABC):
    READING_MODEL: Type[ReadingBase]

    RECEIVED_AND_EXPECTED_FIELDS: dict[str, str]

    REQUIRED_FIELDS: list[str]

    @classmethod
    @abstractmethod
    def _has_invalid_data_types(cls, data: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def is_valid(cls, data: dict) -> bool:
        pass

    @classmethod
    @abstractmethod
    def normalize_data(cls, data: dict) -> dict | None:
        pass

    @classmethod
    def _is_invalid_values(cls, data: dict) -> bool:
        required_normalized_fields = [
            cls.RECEIVED_AND_EXPECTED_FIELDS[field] for field in cls.REQUIRED_FIELDS
        ]

        return not any(
            value
            for key, value in data.items()
            if key not in required_normalized_fields
            and key in cls.RECEIVED_AND_EXPECTED_FIELDS.values()
        )

    @classmethod
    def _is_missing_required_fields(cls, data: dict) -> bool:
        return not all(required_field in data for required_field in cls.REQUIRED_FIELDS)

    @classmethod
    def _normalize_collection_date_field(cls, data: dict) -> dict:
        data['collected_at'] = datetime.fromisoformat(data['collected_at'])

        return data

    @classmethod
    def _normalize_data_keys(cls, data: dict) -> dict | None:
        if cls._is_missing_required_fields(data):
            return None

        normalized_data = {}

        for key, value in data.items():
            if key in cls.RECEIVED_AND_EXPECTED_FIELDS:
                normalized_data[cls.RECEIVED_AND_EXPECTED_FIELDS[key]] = value
                continue

            normalized_data[key] = value

        return normalized_data

    @classmethod
    def save(cls, data: dict, database: Database) -> None:
        category = data.pop('category')

        serial_number = data.pop('serial_number')

        try:
            with database.get_session() as session:
                with session.begin():
                    query = select(Device).where(Device.serial_number == serial_number)

                    if not (device := session.execute(query).scalar_one_or_none()):
                        device = Device(category=category, serial_number=serial_number)

                        session.add(device)

                    device.last_collection_at = data['collected_at']

                    reading_model_object = cls.READING_MODEL(**data, device=device)

                    session.add(reading_model_object)
        except Exception:
            log.exception(f'An error occurred while saving {cls.__class__.__name__}')
            raise
