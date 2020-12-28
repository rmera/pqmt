Copyright (c) 2018 Raul Mera

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2.0 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General
Public License along with this program.  If not, see
<http://www.gnu.org/licenses/>.

To the long life of the Ven. Khenpo Phuntsok Tenzin Rinpoche.


# This is the Python QM translator (pQMT)

Originally written to adapt QM programs to work with the QM/MM pDynamo library (https://sites.google.com/site/pdynamomodeling)

pQMT allows any program that can interact with the ORCA program, to interact with other QM software as well (currently, Tubomole and xtb
are supported)

It works by simply translating inputs and outputs back and forth between ORCA and the target code. This is a reasonable approach 
as long as that the time used to translate inputs and outputs is minimal compared to the lenght of the QM calculation, which is
most commonly the case nowadays.

pQMT has only been tested with pDynamo, but there is no reason it shouldn't work with any other program, such as ChemShell.

## How to run a QM/MM-Turbomole calculation

Assuming Turbomole is correctly installed in the machine to be used:

1. Use e.g. pDynamo to obtain a XYZ file with the QM atoms only (link atoms included!).
2. Prepare a Turbomole calculation with the desired methodology.
3. Edit the control file: 

   Add the following line:

      $grad file=gradient

   Also add the keyword "point charges" in the section $drvopt

4. Copy the provided fakeorca.sh file to your work directory, and edit it to carry out the calculation you need (if unmodified, it runs dscf and grad, you will need to change dscf for ridft if you wish to run calculations with RI). 

5. If you want single-point calculations, add the -SP flag to the calls to OrcaTranslator.py in the fake_orca.sh script, and comment out the grad calculation.

6. Rename the control file to control-template

7. Make sure the script OrcaTranslator.py is in the path

8. In pDynamo, Set the PDYNAMO_SCRATCH shell variable to your scratch directory (it is not enough to set it in the pDynamo script). I'd advice to use the same working directory as scratch.

9. Prepare the  QMMM calculation and set the command for orca to call the script fakeorca.sh

10. Run the calculation normally.

## How to run a QM/MM-xtb calculation

Assuming that xtb 6.3 is correctly installed.

1. Prepare the QM/MM calculation normally.

2. Copy the provided xtb.inp file to your working directory. Edit it if you want to add something.

3. Copy the provided fake_orca.sh to your work directory and edit it. Set the correct charge/multiplicity for your systems and, optionally, the number of cores to be used. Remember that only the GFN1 and GFN2 methods support point charges, so do not attempt to use, say GFN0, which would not result on a proper QM/MM calculation.

4. Prepare the QMMM calculation and set the command for orca to call the script fakeorca_xtb.sh

5. Run the calculation normally.


**

The developer of pQMT is in no way involved with the pDynamo, Orca, Turbomole or xtb development.
Please comply with the license of every program you use, and cite the appropiate references.

pQMT has not been thoroughly tested. Since it is fairly small, the author finds likely
that it will perform similarly in every case. Still, use it at your own risk.


