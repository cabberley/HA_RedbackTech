# Redback Technologies - Smart Hybrid Inverters integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Redback Technologies (https://redbacktech.com/) produces a range of inverter and battery systems. This integration uses the Redback Technologies Portal (public API) and portal (portal.redbacktech.com) to sync and control your solar and battery energy data with Home Assistant.

## Pre-requisites

You need to contact Redback Technologies support team to request API access. This appears to be available to any customer who asks. You will receive access details including "Client ID" and "Client_Secret" which are necessary for this integration.

## Installation

You will need to add this as a custom repository first before installing!!!!
 or by manually copying the `custom_components/redback_tech` folder into your `custom_components` folder.

## Configuration

This first release you will need to add
both your:

- Public API Client_ID and Client_Secret 
- Portal Email address and password

THe next release will enable you to Control your inverter
