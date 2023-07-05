## MAVERICK

This repo holds the version of MAVERICK used in evaluation for the ACM WiSec 2023 [publication][1]. The repo contains the following:

* __mqtt_config_files__: contains the configuration files used for setting up MAVERICK's MQTT broker for each of the testbeds used in the evaluation
* __maverick_mqtt_broker__: contains MAVERICK's code for the MQTT broker, essentially a modified instance of [Mosquitto][2]
* __openhab_config_files__: contains config files for the device interface (labelled _proxy_) and automation platform (labelled _automation_) used in the evaluation
* __policy_synthesis__: contains code for generating candidate invariants given positive and negative event sequences.

Instructions for compiling the MQTT broker are as follows:

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

## Defining Propositions, Invariants and Corrective Actions

### Propositions
A __proposition__ is a boolean variable that reflects whether a given device state satisifies some logical formula. Propositions are defined in a text file with each proposition on a separate line as:

`<proposition_name>: <proposition_logical_formula>`

where `proposition_name` is a human-readable name for the proposition and `proposition_logical_formula` denotes the propositional formula. Note the space between the colon and the logical formula. After definition, a proposition can be referred to by name in invariant formulas. 

Propositions utilize the following operators:

* __Comparision__ (Binary): `==` (EQUAL), `!=` (NEQ), `<=` (LEQ), `>=` (GEQ), `<` (LESS), `>` (GREAT) 
* __Temporal State__ (Unuary): `CURRENT` (the current device state), `PREVIOUS` (the prior device state)
* __Constants__ (Unuary): `CONSTANT_INT` (integer), `CONSTANT_BOOL` (boolean), `CONSTANT_STR`(string) 

Operators use function notation i.e. `==(arg1,arg2)`.

As an example, consider a smart bulb called `Bulb` that exposes two variables: `Temperature` that reports the color temperature as an integer between 0(cool white) and 100 (warm yellow) via the MQTT topics `Bulb/int_Temp` (status topic) and `Bulb/int_Temp/set` (command topic), and `Intensity` that reports the brightness of the bulb as an integer from 0 (off) to 100 (full) via the MQTT topics `Bulb/int_Intensity` (status) and `Bulb/int_Intensity/set`(command). We want to define two propositions: `ColorTemp100` that checks if the current temperature is set to 100, and `BulbIsOn` that checks if the bulb is on currently. These can be defined as:

`ColorTemp100: ==(CURRENT(Bulb/int_Temp),CONSTANT_INT(100))`

`BulbIsOn: ==(CURRENT(Bulb/int_Intensity),CONSTANT_INT(100))`

For clarity purposes, define all propositions in a text file with a `.prop` extension.
### Invariants

An __invariant__ is a logical condition that must be satisfied by the IoT system at all times. MAVERICK uses two types of invariants; (1) Invariants that evaluate _current_ system state and prescribe corrective actions if the invariant is violated and (2) Invariants that evaluate _future_ system state resulting from an incoming automation command and prescribe the _drop_ corrective action.
Invariants of type (1) are defined in a text file, each on a separate line as:

`<invariant_logical_formula>;<corrective_action_1>:<corrective_action_2>:...`

Note that the invariant and corrective actions are separated by `;` and each corrective action is separated by `:`. All such invariants are defined in a file denoted with a `.inv` extension.

Similarly, invariants of type (2) are defined in a separate text file as:

`<invariant_logical_formula>`

which are defined in a file denoted with a `.pol` extension

Invariants use the following operators:

* __Logical operators__ : `=>` (imply), `&` (AND), `|` (OR), `!` (NOT),
* __Temporal operators__ : `Y` (yesterday), `S`

As an example, consider the smart bulb example above with the two propositions `ColorTemp100` and `BulbIsOn`. We want to ensure that the bulb temperature is never set to 100 from the device side while the bulb is on, and in the event that it is, we set the color temperature to 25. We write this invariant as a type (1) invariant as:

`=>(BulbIsOn,!(ColorTemp100));(Bulb/int_Temp/set,25)`

Note that the corrective action is to send the value `25` on the bulb temperature _command topic_.
This reads as _If the bulb is on, then color temperature should not be 100. Otherwise, set color temperature to 25_.

To also ensure that an automation command does not set the color temperature to 100 while the bulb is on, we define an invariant of type (2) as:

`=>(BulbIsOn,!(ColorTemp100))`

Note that this invariant does _not_ have a defined corrective action, as its corrective action is to _drop_ the incoming command.

[1]: <https://dl.acm.org/doi/abs/10.1145/3558482.3590188>
[2]: <https://github.com/eclipse/mosquitto>