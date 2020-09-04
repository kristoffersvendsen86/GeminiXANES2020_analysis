# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:11:48 2020

This is an example script.
Ross main takes an image as argument and returns critical energy, photons/steradian, residual.
The residual is just to make sure that it has converged to a somewhat acceptable solution. This value is usually lower than 0.045 (in a perfect world it would be 0).

Some common variables such as camera response and distance can be changed in rossSetup.py that all modules will import. 

@author: poff
"""

from PIL import Image
from rossMain import rossMain



#load image that is to be analysed    
raw = Image.open("Run13_Shot001_8xAl.tif")


#call the main function, if the second argument it True it will also return 2 plots, if it's left blank it defaults to False
Ec, phPerSr, residual = rossMain(raw, True)



print('Critical energy = '+str(round(Ec*1e-3,2))+' KeV'+'\n', 'photons/s r= ' + str(round(phPerSr,0)) + '\n', 'squared residual = '+str(round(residual,4)))
