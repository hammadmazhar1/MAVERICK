#!/bin/sh

#run the helion trace case
python3 policy_synthesizer.py -t ./helion_vs_synth_exp/helion_case_1_traces.csv -p helion_vs_synth_exp/case1.prop -o helion_case_1 -n 10 -b ./helion_vs_synth_exp/base_state_1_trace
python3 policy_synthesizer.py -t ./helion_vs_synth_exp/synth_case_1_traces.csv -p helion_vs_synth_exp/case1.prop -o synth_case_1 -n 10 -b ./helion_vs_synth_exp/base_state_1_trace