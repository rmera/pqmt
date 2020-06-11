#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
#       OrcaTranslator.py
#       
#       Copyright 2018 Raul Mera
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

#To the long life of the Ven. Khenpo Phuntsok Tenzin Rinpoche.




import sys, os 


#takes ORCA coordinates for atoms and point charges,
#transforms them into TM format.
#The user is supposed to prepare everything else
#in the control file, including the "point charges" option 
#in $drvopt. Also,  after preparing the control file,
#the user must move o copy it to a file named control-template
#in the control file.  for regular QMMM reading TM coordinates
#is not necesary so is not implemented now.


atomn2symbol={"1":"h","6":"c","7":"n","8":"o","29":"cu","30":"zn","16":"s","17":"cl","11":"na"} #incomplete

#Angstrom 2 Bohr
def a2b(angstrom):
    return angstrom/0.529177249
#Bohr 2 Angstrom
def b2a(bohr):
    return bohr*0.529177249

class OrcaRW:
    def __init__(self):
        self.charges=[]
        self.coords=[]
        self.energy=0
        self.gradients=[]
        self.chargegradients=[]
        pass
    def givedata(self):
        return self.energy,self.coords,self.charges,self.gradients,self.chargegradients
    def getdata(self,d):
        self.energy=d[0]
        self.coords=d[1]
        self.charges=d[2]
        self.gradients=d[3]
        self.chargegradients=d[4]
    def readorcacoords(self,orcainp):
        orca=open(orcainp,"r")
        reading=False #True when the coordinates begin.
        for i in orca:
            if "*" in i:
                #The coordinates in orca begin and end with "*".
                reading= not(reading)
            elif reading:
                fields=i.split()
                #Symbol x y z.
                self.coords.append([fields[0],float(fields[1]),float(fields[2]),float(fields[3])])
        orca.close()
    def readorcacharges(self,chargesname):
        try:
            charges=open(chargesname,"r")
        except IOError: #there are no charges to read, it is just a QM calculation
            return
        charges.readline()
        for i in charges:
            if i == "\n":
                break
            fields=i.split()
            #Charge x y z.
            self.charges.append([float(fields[0]),float(fields[1]),float(fields[2]),float(fields[3])])
    def writeorcagradients(self,filename):
        orcagrad=open(filename,"w")
        for i in range(3):
            orcagrad.write("#Bruce\n") #we need not-to-be-read lines.
        orcagrad.write(" "+str(len(self.gradients)/3)+"\n") #3 because the gradients are 3 times the number of atoms, which is what should go here.
        for i in range(3):
            orcagrad.write("#Jackie, Sammo, Bolo\n") #we need not-to-be-read lines.
        orcagrad.write(" "+str(self.energy)+"\n")
        for i in range(3):
            orcagrad.write("#Yaoh!\n") #3 more...
        for i in self.gradients:
            orcagrad.write("{0:24.15f}".format(i)+"\n")  #This should do the trick.
        orcagrad.write("#\n#\n#\n")
        orcagrad.close()
    def writeorcachargegrads(self,filename):
        outgrads=open(filename,"w")
        outgrads.write(str(len(self.chargegradients))+"\n") #Bruce has his own line.
        for i in self.chargegradients:
            outgrads.write(" {0:16.12f} {1:16.12f} {2:16.12f}\n".format(i[0],i[1],i[2]))
        outgrads.close()    
    def writeorcaoutput(self): #writes parts of an  Orca output to stdin. Hopefully enough so it seems that Orca actually ran.
        print "               *           SCF CONVERGED AFTER  23 CYCLES          *"
        print "Total Dipole Moment    :     -1.05903      -6.48762       9.33188" #This should  not be needed for optimization, so let's just put anything.
        print "FINAL SINGLE POINT ENERGY    ", self.energy #maybe more format is needed. The point of this is to make the output look like an orca output.
        print "                                     ****ORCA TERMINATED NORMALLY****    "

class TurbomoleRW():
    def __init__(self):
        self.charges=[]
        self.energy=0
        self.chargegradients=[]
        self.coords=[] #list of lists with an atomic number and coordinates, in Bohrs, for each thing.
        self.gradients=[] #Gradient is just a big list, close to orca format.
        pass

    def givedata(self):
        return self.energy,self.coords,self.charges,self.gradients,self.chargegradients
    def getdata(self,d):
        self.energy=d[0]
        self.coords=d[1]
        self.charges=d[2]
        self.gradients=d[3]
        self.chargegradients=d[4]
    def readtmenergy(): #No need to call this, energies are read from the gradients file by readtmgrads.
        en=open("energy","r")
        en.readline() #useless header
        line=en.readline().split()
        self.energy=float(line[1])
        en.close()
        os.system("rm energy")
    def writetmcoords(self):
        tmcoords=open("coord","w")
        tmcoords.write("$coord\n")
        for i in self.coords:
            tmcoords.write("{0:20.14f}   {1:20.14f}   {2:20.14f}     {3:2s}\n".format(a2b(i[1]),a2b(i[2]),a2b(i[3]),i[0].lower()))
        tmcoords.write("$user-defined-bonds\n$end\n")
        tmcoords.close()
    def writetmcharges(self):
        template=open("control-template","r")
        target=open("control","w")
        for i in template:
            if "$grad" in i: #Copy the point charges after "$grad".
                target.write("$point_charges nocheck\n")
                for j in self.charges:
                    target.write("{0:8.5f}   {1:8.5f}   {2:8.5f}     {3:8.5f}\n".format(a2b(j[1]),a2b(j[2]),a2b(j[3]),j[0]))
            target.write(i)
    def readtmgrads(self):
        tmgrad=open("gradient","r")
        tmgrad.readline()   # Don't need first line.    
        self.energy=float(tmgrad.readline().split()[6])
        for i in tmgrad:
            if "$end" in i:
                break
            fields=i.split()
            #In tubomole you have first the coordinates, which
            #has 4 fields so we easily skip them.
            if len(fields)!=3: 
                continue
            self.gradients.append(float(fields[0].replace("D","E")))
            self.gradients.append(float(fields[1].replace("D","E")))
            self.gradients.append(float(fields[2].replace("D","E")))
        tmgrad.close()
        os.system("mv gradient gradient-old") #Ensures that we always read the first set of gradients. POSIX only, and quite dirty. Sorry, I'm tired.
    def readtmchargegrads(self):
        control=open("control","r")
        readint=False
        for i in control:
            if "$point_charge_gradients" in i:
                readint=True
            elif readint==True:
                fields=i.split()
                if len(fields)!=3:
                    break #No more gradients.
                self.chargegradients.append([float(fields[0].replace("D","E")),float(fields[1].replace("D","E")),float(fields[2].replace("D","E"))])
        control.close()



class xtbRW(TurbomoleRW):
    def __init__(self):
        self.charges=[]
        self.energy=0
        self.chargegradients=[]
        self.coords=[] #list of lists with an atomic number and coordinates, in Bohrs, for each thing.
        self.gradients=[] #Gradient is just a big list, close to orca format.
        pass

    def givedata(self):
        return self.energy,self.coords,self.charges,self.gradients,self.chargegradients
    def getdata(self,d):
        self.energy=d[0]
        self.coords=d[1]
        self.charges=d[2]
        self.gradients=d[3]
        self.chargegradients=d[4]
    def writextbcoords(self):
        os.system("rm xtbrestart") #This file can cause a lot of trouble
        xtbcoords=open("coords.xyz","w")
        xtbcoords.write(str(len(self.coords))+"\n\n")
        for i in self.coords:
            xtbcoords.write("{3:2s} {0:20.14f} {1:20.14f} {2:20.14f}\n".format(i[1],i[2],i[3],i[0]))
        xtbcoords.close()
    def writextbcharges(self,name,col5):
        if len(self.charges)==0: #Just a regular QM calculation, no charges.
            return 
        target=open(name,"w")
        target.write(str(len(self.charges))+"\n")
        if "--debug" in sys.argv:
            debug=open("debug_pcharges.xyz","w") # debug only
            debug.write(str(len(self.charges))+"\n\n") # debug only
        for j in self.charges:
            target.write("{3:8.5f} {0:8.5f} {1:8.5f} {2:8.5f} {4:s} \n".format(j[1],j[2],j[3],j[0],col5)) # interface=orca must be used in the xtb input file
         #   target.write("{3:8.5f} {0:8.5f} {1:8.5f} {2:8.5f} 99 \n".format(a2b(j[1]),a2b(j[2]),a2b(j[3]),j[0])) #Prof. Grimme has confirmed that these should indeed be Bohrs.
            if "--debug" in sys.argv:
                debug.write("Li  {0:8.5f} {1:8.5f} {2:8.5f}\n".format(j[1],j[2],j[3])) # debug only
        target.close()
        if "--debug" in sys.argv:
            debug.close()
    def writexcontrol(self): #for now this do anything. It's best that the use builds their own xcontrol, or just uses the defaults.
        return
        xcont=open("xcontrol","w")
        xcont.close()
    def readxtbgrads(self):
        os.system("rm xtbrestart") #This file can cause a lot of trouble
        tmgrad=open("gradient","r")
        tmgrad.readline()   # Don't need first line.    
        en=tmgrad.readline()[32:53]
        energy=en.lstrip("=")
        if "***" in energy:
            print en
            raise ValueError
        else:
            self.energy=float(energy)
        for i in tmgrad:
            if "$end" in i:
                break
            fields=i.split()
            #In tubomole you have first the coordinates, which
            #has 4 fields so we easily skip them.
            if len(fields)!=3: 
                continue
            self.gradients.append(float(fields[0].replace("D","E")))
            self.gradients.append(float(fields[1].replace("D","E")))
            self.gradients.append(float(fields[2].replace("D","E")))

        tmgrad.close()
        os.system("mv gradient gradient-old") #Ensures that we always read the first set of gradients. POSIX only, and quite dirty. Sorry, I'm tired.
    def readxtbchargegrads(self):
        try:
            control=open("pcgrad","r")
        except IOError:
            return #I just assume there weren't charges there to begin with.
        readint=False
        for i in control:
            grad=[0,0,0]
            gi=[[0,12],[12,24],[24,-1]]
            for j,v in enumerate(grad):
                #try:
                grad[j]=float(i[gi[j][0]:gi[j][1]])
                #except ValueError:
                #    grad[j]=0.0
            self.chargegradients.append(grad)
        control.close()
        os.system("rm pcgrad")
    def readxtbenergy(self):
        self.readtmenergy()




#TODO: Make the following part more modeular so less code is repeated.


if "-O2T" in sys.argv:
    fromOrca=OrcaRW()
    fromOrca.readorcacoords(sys.argv[1])
    fromOrca.readorcacharges(sys.argv[2])
    toTM=TurbomoleRW()
    toTM.getdata(fromOrca.givedata())
    toTM.writetmcoords()
    toTM.writetmcharges()
elif "-T2O" in sys.argv:
    fromTM=TurbomoleRW()
    fromTM.readtmgrads() #also reads the energy
    fromTM.readtmchargegrads()
    toOrca=OrcaRW()
    toOrca.getdata(fromTM.givedata())
    toOrca.writeorcagradients(sys.argv[1])
    toOrca.writeorcachargegrads(sys.argv[2])
    toOrca.writeorcaoutput()

elif "-O2X" in sys.argv:
    fromOrca=OrcaRW()
    fromOrca.readorcacoords(sys.argv[1])
    fromOrca.readorcacharges(sys.argv[2])
    toX=xtbRW()
    toX.getdata(fromOrca.givedata())
    toX.writextbcoords()
#    os.system("cp "+sys.argv[2]+" "+sys.argv[2].replace(".pc","-orcamade.pc"))
    if "-99" in sys.argv:
        toX.writextbcharges(sys.argv[2],"99")
    else:
        toX.writextbcharges(sys.argv[2],"")
elif "-X2O" in sys.argv:
    fromX=xtbRW()
    #fromX.readxtbgrads()
    os.rename(".engrad",sys.argv[1])
    fromX.readxtbchargegrads()
    toOrca=OrcaRW()
    toOrca.getdata(fromX.givedata())
    
    #toOrca.writeorcagradients(sys.argv[1])
    toOrca.writeorcachargegrads(sys.argv[2])
    toOrca.writeorcaoutput()
    os.system("rm energy") # just in case
