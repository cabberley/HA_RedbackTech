"""Sensor platform for Redback Tech integration."""
from __future__ import annotations


from math import floor as floor
#from typing import Any

from homeassistant.components.number import (
    NumberMode,
    NumberDeviceClass,
)

from homeassistant.const import(
    UnitOfPower,
    UnitOfTime,
    UnitOfApparentPower,
)

ENTITY_DETAILS = {
    'power_setting_duration':{ 'name':'Set Duration','unit':UnitOfTime.MINUTES,'icon':'','device_class':None,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'power_setting_watts':{ 'name':'Set Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'op_env_create_max_import':{ 'name':'Set Max Import Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'op_env_create_max_export':{ 'name':'Set Max Export Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'op_env_create_max_discharge':{ 'name':'Set Max Discharge Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'op_env_create_max_charge':{ 'name':'Set Max Charge Power Level','unit':UnitOfPower.WATT,'icon':'','device_class':NumberDeviceClass.POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
    'op_env_create_max_generation':{ 'name':'Set Max Generation Level','unit':UnitOfApparentPower.VOLT_AMPERE,'icon':'','device_class':NumberDeviceClass.APPARENT_POWER,'state_class':None,'display_precison':0,'options':None,'mode':NumberMode.BOX,'category':None},
}
