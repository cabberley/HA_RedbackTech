"""Sensor platform for Redback Tech integration."""
from __future__ import annotations


from math import floor as floor
from typing import Any

from homeassistant.components.number import (
    NumberMode,
    NumberDeviceClass,
)

from homeassistant.const import(
    UnitOfPower,
    UnitOfTime,
)

ENTITY_DETAILS = {
    'power_setting_duration':{ 'name':'Set Duration','unit':UnitOfTime.MINUTES,'icon':'','device_class':None,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'power_setting_watts':{ 'name':'Set Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
}
