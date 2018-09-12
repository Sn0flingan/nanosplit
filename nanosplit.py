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
    outputfile = open(args.output, "w")
    for file in files:
        with open(file) as input:
            for line in input:
                #Check if it is a header
                if line[0]=='@':
                    timestamp = line.split("start_time=")[1].split(" ")[0]
                    print(timestamp)
                #Check if date is passed, then exit.
            #Else print to output file
    outputfile.close()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input fastq files")
    parser.add_argument("-v", "--verbose", help="print more info",
                        action="store_true")
    parser.add_argument("-o", "--output", help="name of output file",
                        required=True)
    parser.add_argument("-t", "--runtime",
                        help="Runtime to include, format HH-MM",
                        required=True)
    args = parser.parse_args()
    #Correct for errors in output
    if args.output.split(".")[-1]!="fastq":
        print("WARNING: Output file must be in fastq format, renaming output file")
        args.output = args.output + ".fastq"
    #Check correct runtime format
    rt = args.runtime.split("-")
    if len(rt[0])>2 or len(rt[1])>2:
        print("ERROR: Runtime argument (t) should be formatted as HH-MM")
    
    if args.verbose:
        print("--- INPUT PARAMETERS ---")
        print("Input file(s): {}".format(args.input))
        print("Output file: {}".format(args.output))
        print("Runtime: {}".format(args.runtime))
    return args

main()
