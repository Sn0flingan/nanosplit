

def main():
    #USER: inputfile(s), outputfile, runtime
    args = get_arguments()
    #Read inputfile
    #Get start time
    #Save all reads pre start+runtime

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input fastq files")
    parser.add_argument("-v", "--verbose", help="print more info",
                        action="store_true")
    parser.add_argument("-o", "--output", help="name of output directory",
                        required=True)
    parser.add_argument("-t", "--runtime",
                        help="Runtime to include, format HH-MM",
                        required=True)
    args = parser.parse_args()
    #Correct for errors in output
    if args.output[len(args.output)-1]=='/':
        args.output = args.output[len(args.output)-2]
    if not exists(args.output):
        makedirs(args.output)
    #Check correct runtime format
    rt = args.runtime.split("-")
    if len(rt[0])>2 or len(rt[1])>2:
        print("ERROR: Runtime argument (t) should be formatted as HH-MM")
    return args
