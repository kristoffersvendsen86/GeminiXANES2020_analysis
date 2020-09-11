# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:04:13 2020

This is the main script of the Ross analysis. It takes an image as argument and returns critical energy, photons/steradian and the residual.
The positions of the filters are hard coded here, so if alignment or filters are changed, this script needs to be changed. 
To cut down on excecution time, this script only performs a linear 1d interpolation for the background gradient, making it fast but less precise. 
Fluence calculation assumes a uniform background, taken as the mean across the image (faster but again, less precise) 

There is also an option to plot at a second argument

The results from this script should be within 10 % of the more accurate (but slow) script that uses a 2d biharmonic spline interpolation

@author: Kristoffer Svendsen
"""
import os, sys

rossPath = os.path.dirname(os.path.realpath(__file__))
if rossPath not in sys.path:
    sys.path.append(rossPath)

import numpy as np
from scipy import interpolate
from rossTheoretical import rossTheoretical
from scipy.special import kv
import matplotlib.pyplot as plt

from PIL import Image

import pickle


def rossMain(raw, calibFile,  plots =False, debug=False):    
    # %% image processing
    # raw=rawInput[0]
    
    # calibName=rawInput[1]
    
    infile = open(calibFile,'rb')
    calib= pickle.load(infile)
    infile.close()
    

    Tth, Ec, QE_data, camResp, Ttotal, E=rossTheoretical(calib)

    x=calib['x']
    y=calib['y']
    w=calib['w']
    BGcoord=calib['BGcoord']
    rot=calib['rot']
    flip=calib['flip']
    camResp=calib['camResp']
    xb=calib['xb']
    yb=calib['yb']
    x_ind=calib['x_ind']
    filtMat_ind=calib['filtMat_ind']
    filtLeg=calib['filtLeg']
    r=calib['r']
    pixelSize=calib['pixelSize']   
    Ec=calib['Ec']  




    # raw = Image.fromarray(raw, 'RGB')


        
    
        
    

    # raw = Image.open("Run4_Shot022_2020-09-03.tif")
    nFilt=len(x);   #number of filters to be analysed (count duplicated)

    
    #image rotation and BG subtraction    
    raw=raw.rotate(rot)  #totate the image to get it straigth, changes with alignment...
    if flip:
        raw=np.fliplr(raw)  #flip horizontally to match the layout in the excel file with all the filter locations

    # w=120;    #width of box for bg subtraction
    BG=np.mean(raw[int(BGcoord[1]):int(BGcoord[1]+w), int(BGcoord[0]):int(BGcoord[0]+w)]) #mean of background 
    raw=raw-BG


    # # #use to make sure background is taken at a good position
    if debug:
        plt.imshow(raw)
        rect = plt.Rectangle(BGcoord,w,w,linewidth=1,edgecolor='w',facecolor='none')
        currentAxis = plt.gca()
        currentAxis.add_patch(rect)
    
    
    
    # %% take mean at each filter position
   
    #manually put in coords for all filters...also changes with alignment
    # y = np.array([134, 141, 146, 150, 158, 160, 438, 434, 438, 734, 746, 753, 753, 748, 1054, 1063, 1365, 1365])-34-w/2; 
    # x = np.array([176, 408, 636, 859, 1091, 1321, 415, 637, 868, 173, 402, 647, 872, 1092, 1318, 1552, 1312, 1561])-26-w/2; 
   

    
    
    counter=0;
    imgMeans=np.zeros( nFilt )
           
    # plt.imshow(raw)       #used during coordinate allocation for new alignments
    for i in range(0,nFilt):        
        # use to plot rectangles to make sure mean is taken at correct filter positions  
        if debug:
            rect = plt.Rectangle((x[i],y[i]),w,w,linewidth=1,edgecolor='r',facecolor='none')
            currentAxis = plt.gca()
            currentAxis.add_patch(rect)
        
        imgMeans[counter]=np.mean(raw[int(y[i]):int(y[i]+w),int(x[i]):int(x[i]+w)])     #mean of each filter, same order as in the theoretical calculation in rossTheoretical
        counter=counter+1;               
    
    
    # %% interpolating background gradient
    
    wb=50   #widthbox for background gradient
    
    # #input coordinates, these will generate a meshgrid. i.e. each value represents an entire row/column
    # xb=np.array([120, 340, 580, 810, 1040, 1260, 1500]) 
    # yb=np.array([230, 520, 830, 1140, 1450, 1750])

    nx=len(xb)
    ny=len(yb)
    
    
    Xb, Yb = np.meshgrid(xb, yb)    #generate a meshgrid from the coordinates
    
    #define vectors
    meansBG=np.zeros((ny, nx))
    BG_interp=np.zeros(nFilt)
    
    #list to store the interpolations in
    f_list=[]
    
    #index to know which row each y value is located in...This is ugly but i couldn't think of a better way at the moment
    # x_ind = np.array([0, 1, 2, 3, 4, 5, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 5, 6])
    
    # plt.imshow(raw)    #used to check position
    
    #loop over each row
    for i in range(0,nx):
         #loop over each column in the image and interpolate along the column
        for j in range(0,ny):
            #plot rectangles, used to check position
            if debug:
                rect = plt.Rectangle((Xb[j,i],Yb[j,i]),wb,wb,linewidth=1,edgecolor='g',facecolor='none')
                currentAxis = plt.gca()
                currentAxis.add_patch(rect)  
            
            meansBG[j,i]=np.mean(raw[int(Yb[j,i]):int(Yb[j,i]+wb),int(Xb[j,i]):int(Xb[j,i]+wb)])    #take the mean
        f_list.append(interpolate.interp1d(yb, meansBG[:,i] , fill_value="extrapolate", kind = 'linear'))   #store the interpolation for this column
    
    #loop over all filters
    for i in range(0, nFilt):
        f=f_list[x_ind[i]]        #take the interpolation for this filter, which depends on the column the filter is present in, which is defined by x_ind
        BG_interp[i]=f(y[i])  #take the interpolated value at the filters position
     
        
    # %% Calculating residuals

    #normalise the filter means to the interpolated background means
    filtMeans=imgMeans/BG_interp 
    
    sumResid=0;
   
    # Calculating the least square residual between the theoretical filter transmissions, Tth, and the measured filter transmissions, filtMeans.
    for i in range(0, nFilt):
            temp = (Tth[:,i] - filtMeans[i])**2   #calculate the square residual
            sumResid=sumResid+temp #total residual (sum over the filters)        
    
    
    critical_energy=Ec[np.argmin(sumResid)] #critical energy that minimises the total residual
    
    Ec_error = min(sumResid)
    # %% Photon calculations
    
    nonFiltCountPerPixel = np.mean(meansBG);
    
    # Ratio photon emitted / camera count [photon/count]
    phPerCount = np.trapz((E/critical_energy)**2*kv(2/3, (E/critical_energy)/2)**2, E)/np.trapz((E/critical_energy)**2*kv(2/3, (E/critical_energy)/2)**2*Ttotal*QE_data*E/camResp, E);    #total number of photons that are detectable (due to QE and windows/air) in COUNTS
    
    photonsPerPixel=nonFiltCountPerPixel*phPerCount;    #photons per pixel (using only the gaps means)
    photonperSteradian = photonsPerPixel/np.arctan(pixelSize/r)   #photons per sr
    
    # %% Plotting
    
    if plots:
        #plot total residual
        fig1, ax1 = plt.subplots() 
        plt.semilogy(Ec*1e-3, sumResid)
        plt.ylabel('Squared residual')
        plt.xlabel('Energy [KeV]')
        plt.grid()
     
        
        #plot theoretical and measured values
        # from rossTheoretical import filtMat_ind
        # from rossTheoretical import filtLeg
        
        uniFiltMean=np.zeros(len(filtLeg))
        uniTthMean=np.zeros(len(filtLeg))
        filtStd=np.zeros(len(filtLeg))

        # this part is messy but we have to find wich filters are the same so we can average them, this is set by filtMat_ind
        for i in range(1,len(filtLeg)+1):
            ind2 = np.where(filtMat_ind==i) #search filtMat_ind for all filters of same i
            filtStd[i-1]=np.std(filtMeans[ind2])    #take std of the i'th similar filters
            uniFiltMean[i-1]=np.mean(filtMeans[ind2])   #take mean of the i'th similar filters
            uniTthMean[i-1]=np.mean(Tth[np.argmin(sumResid),ind2])  #do the same search for the theoretical, since they are arranged the same way we also take the mean to make it easy, altougth it's useless
        
        #plotting comes here
        fig2, ax1 = plt.subplots()  
        plt.errorbar(np.linspace(0,len(filtLeg),len(filtLeg)), uniFiltMean, yerr=filtStd,fmt='o',color='green', ecolor='green', elinewidth=3, capsize=0) 
        plt.plot(np.linspace(0,len(filtLeg),len(filtLeg)), uniTthMean,'o', color='black')        
        ax1.set_xticks(np.linspace(0,len(filtLeg),len(filtLeg)))
        ax1.set_xticklabels(filtLeg, rotation='horizontal', fontsize=18)
        ax1.grid()
        plt.ylabel('Transmission')
        plt.legend(['Theoretical', 'Measured'])

    # %% returning values
       
    return critical_energy, photonperSteradian, Ec_error


    
    
    
    
    
    
    