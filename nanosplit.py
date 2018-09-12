import argparse
from os import makedirs
from os.path import exists, isdir, isfile

def main():
    #USER: inputfile(s), outputfile, runtime
    args = get_arguments()
    #Read inputfile
    ##Check if multiple files
    if isdir(args.input):
        files = [file for file in listdir(args.input)
                 if isfile(join(args.input, file)) and
                 (file.split('.')[-1]=="fastq" or file.split('.')[-1]=="fq")]
    elif isfile(args.input) and (args.input.split('.')[-1]=="fastq" or args.input.split('.')[-1]=="fq"):
        files = [args.input]
    else:
        raise NameError("Input file is not fastq format or does not exist.")
    #Get start time
    start_time = ["2018", "05", "15", "14", "33", "30"]
    limit = get_limit(start_time, args.runtime)
    print(limit)
    return
    outputfile = open(args.output, "w")
    for file in files:
        reads_within_limit = get_reads_within_limit(file, limit)
        outputfile.write(reads_within_limit)
    outputfile.close()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input fastq files")
    parser.add_argument("-v", "--verbose", help="print more info",
                        action="store_true")
    parser.add_argument("-o", "--output", help="name of output file",
                        required=True)
    parser.add_argument("-t", "--runtime",
                        help="Runtime to include, format HH:MM",
                        required=True)
    args = parser.parse_args()
    #Correct for errors in output
    if args.output.split(".")[-1]!="fastq":
        print("WARNING: Output file must be in fastq format, renaming output file")
        args.output = args.output + ".fastq"
    #Check correct runtime format
    rt = args.runtime.split(":")
    if len(rt[0])>2 or len(rt[1])>2:
        print("ERROR: Runtime argument (t) should be formatted as HH-MM")
    
    if args.verbose:
        print("--- INPUT PARAMETERS ---")
        print("Input file(s): {}".format(args.input))
        print("Output file: {}".format(args.output))
        print("Runtime: {}".format(args.runtime))
    return args

def get_limit(start_time, runtime):
    runtime = [float(i) for i in runtime.split(":")]
    limit = [float(i) for i in start_time]
    limit[3] = float(start_time[3]) + runtime[0]
    limit[4] = float(start_time[4]) + runtime[1]
    while limit[4]>60:
        limit[4] = limit[4]-60
        limit[3] += 1
    while limit[3]>24:
        limit[3] = limit[3]-24
        limit[2] += 1
    return limit

def get_reads_within_limit(file, limit):
    reads = ""
    with open(file) as input:
        for line in input:
            #Check if it is a header
            if line[0]=='@':
                time = line.split("start_time=")[1].split(" ")[0].strip()
                if time_within_limit(time, limit):
                    reads = reads + line
    return reads

def time_within_limit(time, limit):
    time_parsed = [time[0:4], time[5:7], time[8:10], time[11:13], time[14:16], time[17:19]]
    for i in range(0, 5):
        if float(time_parsed[i])>float(limit[i]):
            return False
    return True

main()
