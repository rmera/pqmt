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


# This is the pDynamo QM translator (pDQMT)

pDynamo is a Python library for MM, QM and especially QMMM calculations, available at https://sites.google.com/site/pdynamomodeling/

pDynamo allows the use of the ORCA program for QM calculations. In some cases, the use of a different QM program may be desirable. This Python script translates the relevant input and ouput files between ORCA and other programs (as of now, Turbomole and xtb are supported), so different QM programs can be employed.

The pDQMT scripts works assuming that the time used to translate inputs and outputs is minimal compared to the lenght of the QM calculation.

Of course, any program that writes/reads Orca files can be used with pDQMT for interaction with Turbomole and xtb.

## How to run a pDynamo/Turbomole calculation.

Assuming Turbomole is correctly installed in the machine to be used:

1. Use e.g. pDynamo to obtain a XYZ file with the QM atoms only.
2. Prepare a Turbomole calculation with the desired methodology.
3. Edit the control file: 

   Add the following line:

      $grad file=gradient

   Also add the keyword "point charges" in the section $drvopt

4. Copy the provided fakeorca.sh file to your work directory, and edit it to carry out the calculation you need (if unmodified, it runs dscf and grad, you will need to change dscf for ridft if you wish to run calculations with RI). 

5. If you want single-point calculations, add the -SP flag to the calls to OrcaTranslator.py in the fake_orca.sh script, and comment out the grad calculation.

6. Rename the control file to control-template

7. Make sure the script OrcaTranslator.py is in the path

8. Set the PDYNAMO_SCRATCH shell variable to your scratch directory (it is not enough to set it in the pDynamo script). I'd advice to use the same working directory as scratch.

9. Prepare the pDynamo QMMM calculation and set the command for orca to call the script fakeorca.sh

10. Run the calculation normally.

## How to run a pDynamo/XTB calculation

Assuming that xtb 6.3 is correctly installed.

1. Prepare the pDynamo calculation normally.

2. Copy the provided xtb.inp file to your working directory. Edit it if you want to add something.

3. Copy the provided fake_orca.sh to your work directory and edit it. Set the correct charge/multiplicity for your systems and, optionally, the number of cores to be used. 

4. Prepare the pDynamo QMMM calculation and set the command for orca to call the script fakeorca_xtb.sh

5. Run the calculation normally.


**

The developer of pDQMT is in no way involved with the pDynamo, Orca, Turbomole or xtb development.
Please comply with the license of every program you use, and cite the appropiate references.

pDQMT has not been thoroughly tested. Since it is fairly small, the author finds likely
that it will perform similarly in every case. Still, use it at your own risk.


