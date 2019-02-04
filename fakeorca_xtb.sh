#!/bin/bash

export BASENAME=job
export XTBCORES=15 #Adjust it for your machine.

CURRENT=$(pwd)
cd $PDYNAMO_SCRATCH

OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2X

xtb coords.xyz --grad --charge=0 --input xcontrol -P $XTBCORES  > out.dat

OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -X2O


cd $CURRENT
