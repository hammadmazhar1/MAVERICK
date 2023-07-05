#!/bin/sh
cd ./SySLite
./tool_setup
. ./env/bin/activate
python ./src/Driver.py -n10 -r ../synth_case_1_invariants_ap -a bv_sygus_ap_impl -dict -t ../synth_case_1.trace
python ./src/Driver.py -n10 -r ../synth_case_1_invariants_ge -a bv_sygus_ge_impl -dict -t ../synth_case_1.trace
