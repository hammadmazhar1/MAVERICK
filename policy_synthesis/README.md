Setup:

1. Create your positive/negative traces of events. Each IoT event is described as <Device, Attribute, value> with a single event on each new line. Create separate positive and negative traces

2. List your traces in a CSV file. As an example, assume we created 4 traces files (2 positive, 2 negative) named example_ptrace1, example_ptrace2, example_ntrace1, example_ntrace2 respectively. List positive traces under a 'Positive' column and negative traces in a 'Negative' column (as done in the example_case_1_traces.csv file)

3. create your Predicates in a predicate file as in the 'example_case_1.prop' file


Run.
Run policy_synthesizer.py as follows:
`python3 policy_synthesizer.py -t <tracelist_csv> -p <predicate_filename> -o <output_filename_prefix> -n <number_of_policy_invariants> `
The output policy will be written in a file named <output_filename_prefix>_invariants.

for example, with 'example_case_1_traces.csv', 'example_case_1.prop', 'example_case_1' and 3 invariants needed

`python3 policy_synthesizer.py -t example_case_1_traces.csv -p example_case_1.prop -o example_case_1 -n 3`