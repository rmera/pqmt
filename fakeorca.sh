#!/bin/bash
/wrk/QMMM/TM/OrcaTranslator.py $BASENAME.inp $BASENAME.pc -O2T

echo "Calling TURBOMOLE"
dscf > dscf.out
grad > grad.out

/wrk/QMMM/TM/OrcaTranslator.py $BASENAME.engrad $BASENAME.pcgrad -T2O

rm gradient #otherwise it will accumulate results from previous runs

echo "TURBOMOLE output translated to ORCA."
