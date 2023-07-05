## OpenHAB Configuration files.

This folder contains the configuration files for the OpenHAB instances. Config files for the device interface are indicated with the `_proxy` suffix, for the automation platform with `_automation`. Following OpenHAB's concepts [found here][1], you will find 3 file types:

* __Items__: Denoted by `.items` extension. Contains definitions of OpenHAB Items which represent device state variables.
* __Things__: Denoted by `.things` extension. Contains definitions of OpenHAB Things which represent devices (this is also where we define OpenHAB connections to MAVERICK's MQTT broker). 
* __Rules__: Denoted by `.things` extension. Contains definition of OpenHAB Rules, which are trigger-action automation rules/apps. We define some rules to ensure that updates from MQTT topics reach items and vice versa.

[1]: https://www.openhab.org/docs/
