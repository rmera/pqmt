#!/bin/bash
export PDYNAMO_SCRATCH=./
export BASENAME=job
export PDQMT=/wrk/programs/pdqmt
export OMP_NUM_THREADS=32 #Adjust it for your machine
CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH

$PDQMT/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2X -99

xtb coords.xyz --grad -c 0 -I xtb.input  -P $OMP_NUM_THREADS  > out.dat

$PDQMT/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -X2O 

cd $CURRENT



