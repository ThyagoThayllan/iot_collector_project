from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from iot_collector.models.mixins import Base
from iot_collector.models.mixins import ReadingBase


class Device(Base):
    __tablename__ = 'device'

    class Category(Enum):
        INVERTER = 'inverter'
        PROTECTION_RELAY = 'protection_relay'
        SOLAR_MONITORING_STATION = 'solar_monitoring_station'

    class Status(Enum):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        REMOVED = 'removed'

    # Device fields
    category: Mapped[Category] = mapped_column(SAEnum(Category), nullable=False)

    last_collection_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    serial_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    status: Mapped[Status] = mapped_column(SAEnum(Status), nullable=False, default=Status.ACTIVE)

    # Reading relationships
    inverter_reading: Mapped[list['InverterReading']] = relationship(back_populates='device')

    protection_relay_reading: Mapped[list['ProtectionRelayReading']] = relationship(
        back_populates='device'
    )

    solar_monitoring_station_reading: Mapped[list['SolarMonitoringStationReading']] = relationship(
        back_populates='device'
    )


class InverterReading(ReadingBase):
    __tablename__ = 'inverter_reading'

    device: Mapped[Device] = relationship(back_populates='inverter_reading')

    # Inverter fields
    cos: Mapped[float] = mapped_column(Float, nullable=False)

    eday: Mapped[float] = mapped_column(Float, nullable=False)
    etotal: Mapped[float] = mapped_column(Float, nullable=False)

    fac: Mapped[float] = mapped_column(Float, nullable=False)

    iac: Mapped[float] = mapped_column(Float, nullable=False)
    iac1: Mapped[float] = mapped_column(Float, nullable=False)
    iac2: Mapped[float] = mapped_column(Float, nullable=False)
    iac3: Mapped[float] = mapped_column(Float, nullable=False)

    ipv1: Mapped[float] = mapped_column(Float, nullable=False)
    ipv2: Mapped[float] = mapped_column(Float, nullable=False)
    ipv3: Mapped[float] = mapped_column(Float, nullable=False)

    pac: Mapped[float] = mapped_column(Float, nullable=False)
    pac1: Mapped[int] = mapped_column(Integer, nullable=False)
    pac2: Mapped[int] = mapped_column(Integer, nullable=False)
    pac3: Mapped[int] = mapped_column(Integer, nullable=False)

    temp: Mapped[float] = mapped_column(Float, nullable=False)

    uac: Mapped[float] = mapped_column(Float, nullable=False)
    uac1: Mapped[float] = mapped_column(Float, nullable=False)
    uac2: Mapped[float] = mapped_column(Float, nullable=False)
    uac3: Mapped[float] = mapped_column(Float, nullable=False)

    upv1: Mapped[float] = mapped_column(Float, nullable=False)
    upv2: Mapped[float] = mapped_column(Float, nullable=False)
    upv3: Mapped[float] = mapped_column(Float, nullable=False)


class ProtectionRelayReading(ReadingBase):
    __tablename__ = 'protection_relay_reading'

    device: Mapped[Device] = relationship(back_populates='protection_relay_reading')

    # Protection Relay fields
    flags: Mapped[dict] = mapped_column(JSON, nullable=False)

    r_freq: Mapped[float] = mapped_column(Float, nullable=False)

    r_ifase_a: Mapped[float] = mapped_column(Float, nullable=False)
    r_ifase_b: Mapped[float] = mapped_column(Float, nullable=False)
    r_ifase_c: Mapped[float] = mapped_column(Float, nullable=False)

    r_pac: Mapped[float] = mapped_column(Float, nullable=False)
    r_pac1: Mapped[int] = mapped_column(Integer, nullable=False)
    r_pac2: Mapped[int] = mapped_column(Integer, nullable=False)
    r_pac3: Mapped[int] = mapped_column(Integer, nullable=False)

    r_temp_interno: Mapped[float] = mapped_column(Float, nullable=False)

    r_vfase_a: Mapped[float] = mapped_column(Float, nullable=False)
    r_vfase_b: Mapped[float] = mapped_column(Float, nullable=False)
    r_vfase_c: Mapped[float] = mapped_column(Float, nullable=False)

    tp_lei: Mapped[str] = mapped_column(String, nullable=False)


class SolarMonitoringStationReading(ReadingBase):
    __tablename__ = 'solar_monitoring_station_reading'

    device: Mapped[Device] = relationship(back_populates='solar_monitoring_station_reading')

    # Solar Monitoring Station fields
    chu_total: Mapped[float] = mapped_column(Float, nullable=False)

    dir_vento: Mapped[float] = mapped_column(Float, nullable=False)

    ir_day: Mapped[float] = mapped_column(Float, nullable=False)
    ir_ghi: Mapped[float] = mapped_column(Float, nullable=False)
    ir_poa: Mapped[float] = mapped_column(Float, nullable=False)
    ir_total: Mapped[float] = mapped_column(Float, nullable=False)

    temp_amb: Mapped[float] = mapped_column(Float, nullable=False)
    temp_med_mod: Mapped[float] = mapped_column(Float, nullable=False)

    tp_lei: Mapped[str] = mapped_column(String, nullable=False)

    umid: Mapped[float] = mapped_column(Float, nullable=False)

    vel_vento: Mapped[float] = mapped_column(Float, nullable=False)
