"""Sensor platform for Redback Tech integration."""
from __future__ import annotations

from typing import Any

from .const import (
    INVERTER_MODES,
)

ENTITY_DETAILS = {
    'power_setting_mode':{ 'name':'Power Mode Selection','unit':None,'icon':None,'device_class':None,'state_class':None,'display_precison':None,'options':INVERTER_MODES,'mode':'None','category':None},
    'schedule_id_selected':{ 'name':'Scheduled ID Selection','unit':None,'icon':None,'device_class':None,'state_class':None,'display_precison':None,'options':'data_options','mode':'None','category':None},

}
