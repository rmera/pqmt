#!/bin/bash

export BASENAME=job
export PDQMT=/your/installation
export OMP_NUM_THREADS=32 #Adjust it for your machine
CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH
$PDQMT/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2X


xtb coords.xyz --grad -c=0 --input xcontrol -P $OMP_NUM_THREADS  > out.dat

$PDQMT/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -X2O


cd $CURRENT
