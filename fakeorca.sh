#!/bin/bash

export BASENAME=job
CURRENT=$(pwd)

cd $PDYNAMO_SCRATCH #It's not enough to set the scratch from the script, it must be set from the shell


OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2T  #OrcaTranslator.py must be in the PATH

dscf > dscf.out
grad > grad.out

OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -T2O


cd $CURRENT

