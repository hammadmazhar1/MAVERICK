import argparse,subprocess

parser = argparse.ArgumentParser("Policy Synthesizer. Requires event trace files, predicates and SySLite")
parser.add_argument("-p",dest='predicate_filename',help="File containing predicates to use with definitions")
parser.add_argument("-t",dest="tracelist_filename",help="CSV file containing list of positive and negative traces")
parser.add_argument("-o",dest="output_filename",help='output filenames for synthesized policy')
parser.add_argument("-n",dest="invariant_num",help="Specify the number of policy invariants you want")
parser.add_argument("-b",dest="initial_trace",help="Trace filename that describes the initial state of the environment")

arguments = parser.parse_args()

output = subprocess.call(["python3","syslite_input_gen.py","--traces",arguments.tracelist_filename,"--preds",arguments.predicate_filename,"--output",arguments.output_filename,"--initial",arguments.initial_trace])
# out = subprocess.call(["./SySLite/tool_setup"])
proc = subprocess.Popen(["/bin/sh","./SySLite/env/bin/activate"],shell=True,stdin=subprocess.PIPE)
run_file = open('run.sh',"w")
run_file.write("#!/bin/sh\n")
run_file.write("cd ./SySLite\n")
run_file.write("./tool_setup\n")
run_file.write(". ./env/bin/activate\n")
run_file.write("python ./src/Driver.py -n" + arguments.invariant_num +' -r ../' +arguments.output_filename + "_invariants_ap" + " -a bv_sygus_ap_impl -dict"+  " -t ../" + arguments.output_filename+".trace\n")
run_file.write("python ./src/Driver.py -n" + arguments.invariant_num +' -r ../' +arguments.output_filename + "_invariants_ge" + " -a bv_sygus_ge_impl -dict"+  " -t ../" + arguments.output_filename+".trace\n")
run_file.close()

output = subprocess.call(["/bin/sh","./run.sh"])
# proc.communicate(bytes("python ./SySLite/src/Driver.py -n" + arguments.invariant_num +' -r ' +arguments.output_filename + "_invariants" + " -a bv_sygus -dict"+  " -t " + arguments.output_filename+".trace \n",'utf-8'))
# output2 = subprocess.call(["python", "./SySLite/src/Driver.py", '-n', arguments.invariant_num, '-r',arguments.output_filename + "_invariants","-a","bv_sygus","-dict","-t",arguments.output_filename+".trace"])
