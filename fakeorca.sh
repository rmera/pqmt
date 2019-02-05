#!/bin/bash

export BASENAME=job
export PDQMT=/your/installation

CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH #It's not enough to set the scratch from the script, it must be set from the shell


$PDQMT/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2T 

dscf > dscf.out
grad > grad.out

$PDQMT/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -T2O


cd $CURRENT

