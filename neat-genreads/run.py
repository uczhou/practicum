import os
import sys
import argparse
import subprocess

SIM_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
sys.path.append(SIM_PATH+'/py/')

'''
For detailed information, please refer to https://github.com/zstephens/neat-genreads
'''

parser = argparse.ArgumentParser(description='run.py')


parser.add_argument('-m',    type=str,    required=False,  metavar='<str>',   default='sem',          help="run different mode: sem, cfg, cfl")
parser.add_argument('-flag',              required=False,  metavar='<str>',   default=False,          help="generate model: True/False")
parser.add_argument('-l',    type=int,    required=False,  metavar='<str>',   default=126,            help="fragment length")
parser.add_argument('-ref',  type=str,    required=False,  metavar='<str>',   default='data/chr1.fa', help="reference file")
parser.add_argument('-i',    type=str,    required=True,   metavar='<str>',   default=None,           help="sem: input_read1.fq (.gz) / input_read1.sam; cfg: input_read.bam; cfl: input_read.bam")

args = parser.parse_args()

(MODE, FLAG, REF, DEFAULT_SIZE, INF) = (args.m, args.flag, args.ref, args.l, args.i)

print FLAG
print INF

DEFAULT_WINDOW = 1000

MODEL_PREFIX = 'models/'
DATA_PREFIX = 'data/'

if INF is not None:
    FILE_NAME = INF.split('/')[-1].split('.')[0]
    print FILE_NAME
    SE_OUTF = MODEL_PREFIX + FILE_NAME + 'SE.p'
    GC_OUTF = MODEL_PREFIX + FILE_NAME + 'GC.p'
    GC_INF = DATA_PREFIX + FILE_NAME + 'GCINPUT'
    # FL_INF = DATA_PREFIX + FILE_NAME + 'FLINPUT'
    FL_OUTF = 'fraglen.p'
    OUTFN = DATA_PREFIX + FILE_NAME 
else:
    SE_OUTF = None
    GC_OUTF = None
    FL_OUTF = None
    OUTFN = DATA_PREFIX + 'testoutput'

def main():
    # Generates sequence error model for genReads.py -e option
    if MODE == 'sem':
        if FLAG == 'True':
            if INF is None:
                print "Error: no input file."
                return
            else:
                subprocess.call(['python', 'utilities/genSeqErrorModel.py', '-i', INF, '-o', SE_OUTF])
                subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '-e', SE_OUTF, '-o', OUTFN])
        else:
            subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '-o', OUTFN])
    # Computes GC% coverage bias distribution from sample (bedrolls genomecov) data 
    elif MODE == 'cfg':
        if FLAG == 'True':
            if INF is None:
                print "Error: no input file."
                return
            else:
                subprocess.call(['./bedtools/bin/bedtool', 'genomecov', '-d', '-ibam', INF,  '-g', REF, '>>', GC_INF])
                subprocess.call(['python', 'utilities/computeGC.py', '-r', REF, '-i', GC_INF, '-w', DEFAULT_WINDOW, '-o', GC_OUTF])
                subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '--gc-model', GC_OUTF, '-o', OUTFN])
        else:
            subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '-o', OUTFN])
    # Computes empirical fragment length distribution from sample data and creates fraglen.p model in working directory.   
    elif MODE == 'cfl':
        if FLAG == 'True':
            if INF is None:
                print "Error: no input file."
                return
            else:
                view = subprocess.Popen(['./samtools/samtools', 'view', INF], stdout=subprocess.PIPE)
                print "Finished samtools"
                subprocess.call(['python', 'utilities/computeFraglen.py'], stdin=view.stdout)
                subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '--pe-model', FL_OUTF, '-o', OUTFN])

        else:
            subprocess.Popen([sys.executable, 'genReads.py', '-r', REF, '-R', DEFAULT_SIZE, '-o', OUTFN])
if __name__ == '__main__':
    main()