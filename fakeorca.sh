#!/bin/bash

export BASENAME=job
export PQMT=/your/installation

CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH #It's not enough to set the scratch from the script, it must be set from the shell


$PQMT/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2T 

dscf > dscf.out
grad > grad.out

$PQMT/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -T2O


cd $CURRENT

