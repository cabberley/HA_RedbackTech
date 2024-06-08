<h1 align="center">
  <a href="https://petkit.com"><img src="https://raw.githubusercontent.com/cabberley/ha_redbacktech/main/ha_redbacktech_logo.png" width="480"></a>
  <br>
  <i>Redback Smart Inverters Home Assistant Integration</i>
  <br>
  <h3 align="center">
    <i> Custom Home Assistant component for controlling and monitoring Redback Technologies Smart Inverters. </i>
    <br>
  </h3>
</h1>

<p align="center">
  <href="https://github.com/cabberley/HA_RedbackTech/releases"><img src="https://img.shields.io/github/v/release/cabberley/HA_RedbackTech?display_name=tag&include_prereleases&sort=semver" alt="Current version">
  <img alt="GitHub" src="https://img.shields.io/github/license/cabberley/HA_RedbackTech">
  <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/cabberley/ha_redbacktech"> <img alt="GitHub User's stars" src="https://img.shields.io/github/stars/cabberley">

</p>
<p align="center">
    <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg"></a>
</p>
<p align="center">
  <a href="https://www.buymeacoffee.com/cabberley" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</p>

[Redback Technologies](https://redbacktech.com/) produces a range of inverter and battery systems. This integration uses the Redback Technologies Portal (public API) and portal (portal.redbacktech.com) to sync and control your solar and battery energy data with Home Assistant.

This release of the integration adds some **MAJOR** enhancements!!

- **Supports Controller your Inverter, more details below!**
- Supports multiple API Accounts
- Supports multiple RedBack inverters on the same site
- Supports multiple inverters on the same API Account
- Creates an Inverter and a Battery devices for each inverter it finds (Adds the Battery device only if it finds batteries in your setup)

> [!IMPORTANT]
> **Please make sure you read and understand the infomation below on how this integration controls your inverter!**

## Pre-requisites

You need to contact Redback Technologies support team to request API access. This appears to be available to any customer who asks. You will receive access details including "Client ID" and "Client_Secret" which are necessary for this integration.

You will also need your username(email) and password for the Redback Portal Website as well.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=cabberley&repository=HA_RedbackTech&category=integration)

To install this Home Assistant Custom Integration, either Click on the open HACS Repository or by manually copying the `custom_components/redback_tech` folder into your Home assistant `custom_components` folder.

> [!TIP]
> Don't forget to restart your Home Assistant after adding the integration to your HACS!

## Configuration

After adding the Integration to HACS go to your settings and add the Integration.
Complete the form and submit.

- Redback API Client_ID
- Redback Client_Secret
- Redback Portal Email address
- Redback Portal Password

If successful you should now find devices for all your Inverters and Battery stacks.

## Controlling your Inverter with the Integration

Most users will be familiar with the Redback Portal Settings Page, which enables you to either create timed schedule to set the inverter to operate during a window of time or the alternative of set the Inverter to a mode and power setting and it will stay like that until you change it.

For this integration, I decided to take the schedule path, the reasoning for this was my previous controls to set the inverter using the 'Set" method relied on HA setting a date time value to a DateTime entity and triggering a HA event to turn it back to Auto when the time triggered. If HA restarted, there was no guarantee that the datetime value would persist and the trigger would fire when expected.

This integration, uses the scheduling so the Redback System will return its state after the 'Window' has completed. This also enables you to set schedules in advance to meet your desired inverter\battery power flows. You could integrate with [EMHASS](https://github.com/davidusb-geek/emhass) to setup a set off predefined schedules.

### The Redback Integration Controls

On the Inverter Device are a set of controls
**Scheduled ID Selection**
If you have any "scheduled events" (Scheduled inverter control periods) this selector will provide a list of the current schedules sitting in the Redbacks systems. When you select one from this list the following sensors will refresh with the details of this schedule

- Scheduled Start Time
- Scheduled Finish Time
- Scheduled Duration (minutes between start and finish)
- Scheduled Inverter Mode (Charge Battery, Discharge Battery, Import, Export, Conserve)
- Scheduled Power Level (power in Watts)

**Schedule Creation Fields**
The following fields enable you to set the parameters to create a scheduled event

- Power Mode Selection (Set the Inverter Mode for the Event)
- Set Power Level (Set the Power level in Watts for the Event)
- Set Duration (Set the number of minutes that this event should run for)
- Set Start Time (Date time entity to set the start time for the event)

After you have set those parameters, press the **Create Schedule** button and th integration will send the data to Redback to add onto your schedule. After a few seconds the unique ID Redback assigned the event will become visible in the Scheduled ID Selection Selector.

> [!NOTE]
> If you want to change the mode of the inverter immediately for a period of time, just set the start time to now, along with the other settings desired and press the **create Schedule** button.
> To help I have added a Button "Reset Start Time to Now' to set the time to the current time.

> [!IMPORTANT]
> When creating a schedule, don't rush it as the system needs to update the data for each field. 

### The Redback Integration Buttons

On the Inverter Device are a set of buttons

- Create Schedule (Explained above)
- Delete All Schedules (This will delete all events in the system and return to the inverter to the mode it was in before the any current occurring events)
- Delete Selected Schedule (Deletes only the event selected in the Selector )
- Reset Inverter to AUTO (Will delete all schedules in the Inverter and also then reset the Inverter mode to 'Auto')
- Reset Start Time to Now (Explained above)

## TO DO LIST

- Create a HA Calender to surface the all the scheduled events.
- Use something more user friendly for the event ids in the Schedule Selector list.
- expose the api calls behind the buttons as HA Services

