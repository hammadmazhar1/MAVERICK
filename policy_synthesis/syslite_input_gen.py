from lib2to3.pytree import convert
import sys,os,csv,json,re,argparse,copy



## nested prefix+parentheses parsing code from: https://stackoverflow.com/a/58394958
def convert_to_tuple(text):
    """ Take an expression and convert it to tuple
      'neg(or(p,q))'  -->  ('neg', ('or', 'p', 'q'))
    """
    # used to extract not nested expression
    pattern = re.compile('(\w+|\W+)\(([^\(]*?)\)')
    # extract the index of the expression
    index_pattern = re.compile('#(\d+)#')
    # contains all expression extracted from the text
    expressions = []
    # you only need to extract most global expression only
    global_expressions = []


    def fix_expression(expression):
        """  a recursive solution to rebuild nested expression. """
        if isinstance(expression, str):
            # if the expression is like #index# return the correct expression else return this str expression
            m = index_pattern.search(expression)
            if m:
                return tuple(fix_expression(expressions[int(m.group(1))]))
            return expression
        # if the expression is a tuple extract all fixed nested expression in a tuple
        return tuple(fix_expression(subexp) for subexp in expression)


    def extract_expression(code):
        """ keep extracting nested expressions list,  """

        def add_exp(match):
            """ handle the match return by sub to save the expression and return its index."""
            expressions.append(None)
            index = len(expressions) - 1
            name, args = match.groups()

            if ',' in args:
                # if what is between parentheses contains ',' split is
                args = tuple(args.split(','))
            else:
                # args should always be a tuple to support unpacking operation
                args = (args,)

            # expression transformed to a tuple
            expressions[index] = (name, *args)
            return '#{}#'.format(index)

        while pattern.search(code):
            code = re.sub(pattern, add_exp, code)

        # for debuging string after removing all expression
        # print(code)


    # this extract all nested expression in the  text
    extract_expression(text)

    # Global expression there index is not used in any other expression
    # the last expression is for sure a global one because.
    global_expressions.append(expressions[-1])
    for i, exp in enumerate(expressions[:-1]):
        for other_exp in expressions[i + 1:]:
            if any('#{}#'.format(i) in sub_exp for sub_exp in other_exp):
                break
        else:
            # this expression is not used in any expression it's a global one
            global_expressions.append(exp)

    # for debugging
    # print(expressions)
    # print(global_expressions)

    return fix_expression(global_expressions[0])
def eval_exp(tup,trace,cur_state_number):
    value =None
    state_model=trace[cur_state_number]
    if tup[0] == "CURRENT":
        # print(tup)
        instance = tup[1].split('/')
        # print(state_model)
        # print(instance)
        if instance[0] not in state_model.keys():
            return False
        else:
            variable_split = instance[1].split("_")
            variable_type = variable_split[0]
            variable_name = variable_split[1]
            # print(variable_type)
            if variable_name in state_model[instance[0]]:
                # print(variable_name)
                if variable_type == "bool":
                    if state_model[instance[0]][variable_name] == "on":
                        value = True
                    else:
                        value = False
                else:
                    value = state_model[instance[0]][variable_name]                                        
            else:
                return False
    elif tup[0] == "PREVIOUS":
        instance = tup[1].split('/')
        if state_number ==0:
            return False
        old_state_model = trace[cur_state_number-1]
        if instance[0] not in old_state_model.keys():
            return False
        else:
            variable_split = instance[1].split("_")
            variable_type = variable_split[0]
            variable_name = variable_split[1]
            # print(variable_name)
            # print(variable_type)
            if variable_name in old_state_model[instance[0]]:
                if variable_type == "bool":
                    if state_model[instance[0]][variable_name] == "on":
                        value = True
                    else:
                        value = False
                else:
                    value = old_state_model[instance[0]][variable_name]                                        
            else:
                return False
    elif tup[0] == "CONSTANT_BOOL":
        if tup[1] == "TRUE":
            return True
        else:
            return False
    elif tup[0] == "CONSTANT_STR":
        return tup[1]
    elif tup[0] == "CONSTANT_INT":
        return int(tup[1])
    elif tup[0] == "==":
        # print(tup)
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value == right_value
    elif tup[0] == "!=":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value != right_value
    elif tup[0] == "<=":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value <= right_value
    elif tup[0] == ">=":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value >= right_value
    elif tup[0] == "<":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value < right_value
    elif tup[0] == ">":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        if left_value == "fixed_value" and type(right_value) == int:
            return True
        else:
            return left_value >= right_value
    elif tup[0] == "|":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        else:
            return left_value or right_value
    elif tup[0] == "&":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        right_value = eval_exp(tup[2],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        else:
            return left_value and right_value
    elif tup[0] == "!":
        left_value = eval_exp(tup[1],trace,cur_state_number)
        if left_value == "Prop false" or right_value == "Prop false":
            return False
        else:
            return not left_value 
    return value
parser = argparse.ArgumentParser(description="Generate a SySLite input file from trace and predicate files")
parser.add_argument("--traces",dest="trace_filename", help="filename of CSV file with positive and negative trace filenames")
parser.add_argument("--preds",dest="pred_filename", help="filename of predicates to be used in policy")
parser.add_argument("--output",dest="output_filename",help="name of output file, created in both JSON and SySLITE format")
parser.add_argument("--initial",dest="initial_tracepath",help="trace that describes initial state of system")
args = parser.parse_args()
positive_trace_names = []
negative_trace_names = []
trace_csv = csv.DictReader(open(args.trace_filename,'r'))
for line in trace_csv:
    positive_trace_names.append(line['Positive'])
    negative_trace_names.append(line['Negative'])

# load propositions
prop_lines = open(args.pred_filename,'r').readlines()
props = {}
for line in prop_lines:
    line_data = line.split(": ")
    # print(line_data)
    prop_name = line_data[0]
    prop_line = line_data[1]
    # print(prop_line)
    prop = {}
    extracted_exp = convert_to_tuple(prop_line)
    # print(extracted_exp)
    props[prop_name] = extracted_exp

# load inital trace
initial_state = {}
initial_trace_file = open(args.initial_tracepath,'r').readlines()
for line in initial_trace_file:
    token_string_parts = line.split(',')
    # print(token_string_parts)
    device = token_string_parts[0].replace("<","")
    capability = token_string_parts[1]
    variable = token_string_parts[2].replace(">","").replace("\n","")
    if device not in initial_state.keys():
        initial_state[device] ={}
    initial_state[device][capability] = variable
# load positive system traces
print("Loading Positive Traces")
positive_traces = {}
for trace_name in positive_trace_names:
    positive_traces[trace_name]={}
    positive_traces[trace_name][0] = copy.deepcopy(initial_state)
    with open('./'+trace_name,'r') as fromFile:
        old_state_model = positive_traces[trace_name][0]
        tokens = fromFile.readlines()
        for c_token, token_string in enumerate(tokens):
            new_state_model = copy.deepcopy(old_state_model)
            # if (token_string != '<s>' and token_string !='</s>'):
            token_string_parts = token_string.split(',')
            # print(token_string_parts)
            device = token_string_parts[0].replace("<","")
            capability = token_string_parts[1]
            variable = token_string_parts[2].replace(">","").replace("\n","")
            if device not in new_state_model.keys():
                new_state_model[device] ={}
            new_state_model[device][capability] = variable
            # print(c_token)
            # print(old_state_model)
            # print(new_state_model)
           
            positive_traces[trace_name][c_token+1] = new_state_model
            # for device in new_state_model.keys():
            #     old_state_model[device]={}
            #     for capability in old_state_model[device].keys():
            #         old_state_model[device][capability] = new_state_model[device][capability]
            old_state_model = copy.deepcopy(new_state_model)
           
# load negative system traces
print("Loading Negative Traces")
negative_traces = {}
for trace_name in negative_trace_names:
    negative_traces[trace_name]={}
    negative_traces[trace_name][0] = copy.deepcopy(initial_state)
    with open(trace_name,'r') as fromFile:
        old_state_model = negative_traces[trace_name][0]
        tokens = fromFile.readlines()
        for c_token, token_string in enumerate(tokens):
            new_state_model = copy.deepcopy(old_state_model)
            # if (token_string != '<s>' and token_string !='</s>'):
            token_string_parts = token_string.split(',')
            # print(token_string_parts)
            device = token_string_parts[0].replace("<","")
            capability = token_string_parts[1]
            variable = token_string_parts[2].replace(">","").replace("\n","")
            if device not in new_state_model.keys():
                new_state_model[device] ={}
            new_state_model[device][capability] = variable
            # print(new_state_model)
            # print(c_token)
            # print(old_state_model)
            # print(new_state_model)
            negative_traces[trace_name][c_token+1] = new_state_model
            old_state_model = copy.deepcopy(new_state_model)
    
#ordered proposition list for bit vectors    
ordered_prop_names = sorted(props.keys())
# print("propositions:" + str(len(ordered_prop_names)))
positive_trace_bit_vectors = []
negative_trace_bit_vectors = []
for trace_name in positive_traces.keys():
    positive_trace = positive_traces[trace_name]
    # print(positive_trace)
    state_numbers = sorted(positive_trace.keys())
    trace_vector = []
    for state_number in state_numbers:
        state_model = positive_trace[state_number]
        prop_values =[]
        for prop_name in ordered_prop_names:
            prop_structure = props[prop_name]
            prop_value = eval_exp(prop_structure,positive_trace,state_number)
            if prop_value:
                prop_values.append(1)
            else:
                prop_values.append(0)
        trace_vector.append(prop_values)
        # print(len(prop_values))
    # print(trace_vector)
    positive_trace_bit_vectors.append(trace_vector)

for trace_name in negative_traces.keys():
    negative_trace = negative_traces[trace_name]
    state_numbers = sorted(negative_trace.keys())
    trace_vector = []
    for state_number in state_numbers:
        state_model = negative_trace[state_number]
        prop_values =[]
        for prop_name in ordered_prop_names:
            prop_structure = props[prop_name]
            prop_value = eval_exp(prop_structure,negative_trace,state_number)
            if prop_value:
                prop_values.append(1)
            else:
                prop_values.append(0)
        trace_vector.append(prop_values)
    negative_trace_bit_vectors.append(trace_vector)
max_trace_length =0
for trace in positive_trace_bit_vectors:
    if len(trace) > max_trace_length:
        max_trace_length = len(trace)
# print(max_trace_length)
for trace in negative_trace_bit_vectors:
    if len(trace) > max_trace_length:
        max_trace_length = len(trace)

for index,trace in enumerate(positive_trace_bit_vectors):
    if len(trace)<max_trace_length:
        for i in range(len(trace),max_trace_length):
            positive_trace_bit_vectors[index].append(trace[:-1][0])
    # print(max_trace_length)
    # print(len(positive_trace_bit_vectors[index]))
for index,trace in enumerate(negative_trace_bit_vectors):
    if len(trace)<max_trace_length:
        for i in range(len(trace),max_trace_length):
            negative_trace_bit_vectors[index].append(trace[:-1][0])
    # print(max_trace_length)
    # print(len(negative_trace_bit_vectors[index]))
json_output_file = open(args.output_filename + ".json",'w')
output_json = {}
output_json["propositions"]= ordered_prop_names
output_json["positive_traces"] = positive_trace_bit_vectors
output_json["negative_traces"] = negative_trace_bit_vectors
output_json["optional_unary_ops"] = ["!","Y","O"]
output_json["optional_binary_ops"] = ["S","&","|","=>"]
output_json["optional_num_formulas"] = 10
output_json["optional_target_match"] = "=>(p2,p2)"
json.dump(output_json,json_output_file)
json_output_file.close()
normal_output_file = open(args.output_filename+".trace","w")
# for prop in ordered_prop_names:
#     normal_output_file.write(prop)
#     normal_output_file.write(",")
prop_names = str(ordered_prop_names).replace("[","")
# print(prop_names)
prop_names = prop_names.replace("]","").replace("'","").replace(" ","")
normal_output_file.write(prop_names)
normal_output_file.write("\n")
normal_output_file.write("---\n")
for trace in positive_trace_bit_vectors:
    trace_str = str(trace)
    trace_str = trace_str.replace("[[","")
    # print(trace_str)
    trace_str = trace_str.replace("]]","")
    trace_str = trace_str.replace('], [',";")
    trace_str = trace_str.replace(" ","")
    trace_str = trace_str.replace("]","")
    # print(trace_str)
    normal_output_file.write(trace_str)
    normal_output_file.write("\n")
normal_output_file.write("---\n")
for trace in negative_trace_bit_vectors:
    trace_str = str(trace)
    trace_str = trace_str.replace("[[","")
    # print(trace_str)
    trace_str = trace_str.replace("]]","")
    trace_str = trace_str.replace('], [',";")
    trace_str = trace_str.replace(" ","")
    trace_str = trace_str.replace("]","")
    # print(trace_str)
    normal_output_file.write(trace_str)
    normal_output_file.write("\n")
normal_output_file.write("---\n")
normal_output_file.write("!,Y,O\n")
normal_output_file.write("---\n")
normal_output_file.write("S,&,|,=>\n")
normal_output_file.write("---\n")
normal_output_file.write("10\n")
normal_output_file.write("---\n")
normal_output_file.write("=>(p2,p2)")


# for trace in positive_trace_bit_vectors[::-1]:
#     for state in trace[::-1]:
#         for value in state[::-1]:
#             normal_output_file.write(value)
#             normal_output_file.write(',')
#         normal_output_file.write(state[-1])
#         normal_output_file.write(";")
#     for value in trace[-1]:
#         normal_output_file.write(value)
    