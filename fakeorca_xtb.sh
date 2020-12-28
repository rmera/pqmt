#!/bin/bash
export PDYNAMO_SCRATCH=./
export BASENAME=job
export PQMT=/wrk/programs/pqmt
export OMP_NUM_THREADS=32 #Adjust it for your machine
CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH

$PQMT/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2X -99

xtb coords.xyz --grad -c 0 -I xtb.input  -P $OMP_NUM_THREADS  > out.dat

$PQMT/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -X2O 

cd $CURRENT



