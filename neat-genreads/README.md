## Ref: https://github.com/zstephens/neat-genreads

## Note

1. The required binaries: betools, samtools, bcftools and htslib have been compiled and could be used directly.
2. run.py script is used to generate the sequencing data based on input file along with reference file. The script basically reduced the complexity of running neat-genreads. It provides 4 running modes to generate the sequencing data.

## Usage

```
python run.py [-m <str>] [-flag <str>] [-l <str>] [-ref <str>] -i <str>
```

## Parameters

1. -m: mode type
	'sem': Running with Sequencing error model
	'cgc': Running with GC coverage bias distribution model
	'cfl': Running with fragment length distribution model
2. -flag: flag type
	True: Running each mode with self defined model
	False: Running each mode with default model
3. -l: fragment length
4. -ref: reference genome
5. -i: input file
