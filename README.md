## MAVERICK

This repo holds the version of MAVERICK used in evaluation for the ACM WiSec 2023 [publication][1]. The repo contains the following:

* __config_files__: contains the configuration files used for setting up MAVERICK's MQTT broker for each of the testbeds used in the evaluation
* __maverick_mqtt_broker__: contains MAVERICK's code for the MQTT broker, essentially a modified instance of [Mosquitto][2]

Instructions for compiling the MQTT are as follows:

__Compilation environment__: Linux x86/64, YMMV on Windows/Mac

__Dependencies__: g++, openssl

1. navigate to `./maverick_mqtt_broker/src`
2. run `make` i.e. `$ make`

On successful compilation, you should have a `mosquitto` executable in the `src` directory, this is the executable to run MAVERICK's MQTT broker.

### Running MAVERICK

To start up the MQTT broker, run the command:
``mosquitto -c <config_filepath>``

Where `<config_filepath>` points to the configuration file to be used (`.conf` extension). The config file format follows Mosquitto config file format with 3 additional options for MAVERICK:

* __prop_file:__ points to the file with _proposition_ definitions required (use `.prop` extension to differentiate).
* __inv_file:__ points to the file with definitions of _invariants_ with _corrective actions_ to be applied on device statuses (use `.inv` extension to differentiate)
* __pol_file:__ points to the file with definitions of _invariants_ to be applied on incoming commands with the _'drop' corrective action_ (use `.pol` extension).

**Remember, filepaths are relative to the location of the execution location, so either use absolute filepaths or check your relative paths.**

Example config files (called `test_system` with indicative extensions) are included in the `maverick_mqtt_broker` to test your compiled executable.

### Defining Propositions, Invariants and Corrective Actions



[1]: <https://dl.acm.org/doi/abs/10.1145/3558482.3590188>
[2]: <https://github.com/eclipse/mosquitto>