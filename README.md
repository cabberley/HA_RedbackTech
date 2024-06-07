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
  <a href="https://github.com/RobertD502/home-assistant-petkit/releases"><img src="https://img.shields.io/github/v/release/RobertD502/home-assistant-petkit?display_name=tag&include_prereleases&sort=semver" alt="Current version"></a>
  <img alt="GitHub" src="https://img.shields.io/github/license/RobertD502/home-assistant-petkit">
  <img alt="GitHub manifest.json dynamic (path)" src="https://img.shields.io/github/manifest-json/requirements/RobertD502/home-assistant-petkit%2Fmain%2Fcustom_components%2Fpetkit?label=requirements">
  <img alt="Total lines count" src="https://tokei.rs/b1/github/RobertD502/home-assistant-petkit"
</p>

<p align="center">
  <a href="https://www.buymeacoffee.com/RobertD502" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="90" width="381.6"></a>
  <a href="https://liberapay.com/RobertD502/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg" height="90" width="270"></a>
</p>

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
