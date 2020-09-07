## Non-parametric fitting with gaussian process regression
## Matthew Streeter 2020

import numpy as np
from scipy.ndimage.filters import median_filter
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic,
                                              ExpSineSquared, DotProduct,
                                              ConstantKernel, WhiteKernel)
from scipy.interpolate import interp1d, interp2d, RectBivariateSpline

from scipy.ndimage import gaussian_filter


class GP_beam_fitter():
    
    def __init__(self,beam_mask,N_samples = 1000, N_pred =(100,100)):
        self.beam_mask = beam_mask
        self.mask_ind = np.nonzero(beam_mask.flatten())
        self.N_samples = N_samples
        self.N_pred = N_pred
        
        kernel = 1**2* Matern(
            length_scale=0.1, length_scale_bounds=(1e-2, 10.0),nu=1.5
        ) + WhiteKernel()
        
        self.gp = GaussianProcessRegressor(kernel=kernel)
        self.x,self.y,self.XY = self._make_image_grid(beam_mask)
        self.x_pred,self.y_pred,self.XY_pred = self._make_image_grid(np.ones(N_pred))
        self._determine_pixel_weights()
        
        
    def _make_image_grid(self,img):
        x = np.linspace(-1,1,num=img.shape[1],endpoint=True)
        y = np.linspace(-1,1,num=img.shape[0],endpoint=True)
        [X,Y] = np.meshgrid(x,y)
        XY = np.array([X.flatten(),Y.flatten()]).T
        return x,y,XY
        
    def _determine_pixel_weights(self):
        bmf = gaussian_filter(self.beam_mask,100)        
        pixel_w = 1/bmf.flatten()[self.mask_ind]
        self.pixel_w = pixel_w/np.sum(pixel_w)
        
    def fit_beam(self,image,med_filter=5):
  
        imgMax = np.max(image)
        imgMin = np.min(image)
        if med_filter is not None:
            image = median_filter(image.astype(float),med_filter)
        I  = (image.flatten()-imgMin)/(imgMax-imgMin)
        I_index = np.arange(len(I))

        selected_index = np.random.choice(I_index[self.mask_ind],
                                          size=self.N_samples,replace=False,p=self.pixel_w)

        x_train = self.XY[selected_index,:]
        I_train = I[selected_index]
        self.gp.fit(x_train,I_train)
       

        I_pred,I_pred_err = self.gp.predict(self.XY_pred,return_std=True)
        I_pred = I_pred.reshape(self.N_pred)
        I_pred_err = I_pred_err.reshape(self.N_pred)

        beam_image = RectBivariateSpline(self.x_pred,self.y_pred,I_pred)(self.x,self.y)*(imgMax-imgMin)+imgMin
        beam_unc = RectBivariateSpline(self.x_pred,self.y_pred,I_pred_err)(self.x,self.y)*(imgMax-imgMin)
        
        trans_image = image/beam_image
        null_trans_vals = trans_image[np.nonzero(self.beam_mask)]
        null_trans_mean = np.mean(null_trans_vals)
        null_trans_rms = np.std(null_trans_vals,dtype=np.float64)
        # print(f'Null transmission mean = {null_trans_mean:1.06f}')
        # print(f'Null transmission rms = {null_trans_rms:1.06f}')

        return beam_image, beam_unc
        

# def gauss2Dbeam(U,a0,a1,a2,a3,a4,a5):
#     # a0 peak,
#     # a2,a4 widths
#     # a1,a3 centers
#     # a5 angle
#     f = a0*np.exp( -(
#         ( U[:,0]*np.cos(a5)-U[:,1]*np.sin(a5) - a1*np.cos(a5)+a3*np.sin(a5) )**2/(2*a2**2) + 
#         ( U[:,0]*np.sin(a5)+U[:,1]*np.cos(a5) - a1*np.sin(a5)-a3*np.cos(a5) )**2/(2*a4**2) ) )

#     return f
# def gauss2DbeamFit(pG,U,I):
    
#     f = gauss2Dbeam(U,*pG)
#     fErr = np.sqrt(np.mean((f-I)**2))
#     return fErr

# def polyBeam(U,a0,a1,a2,a3,a4):
#     R = np.sqrt((U[:,0]-a0)**2 + (U[:,1]-a1)**2)
#     P = (a2,a3,a4)
        
#     N = np.size(P)
#     f = np.zeros(np.shape(R))
#     for n in range(0,N):
#         f = f + P[n]*R**(N-n-1)

#     return f

# def setRange2one(x):
#     xMin = np.min(x)
#     xMax = np.max(x)
#     xRange = xMax-xMin
#     x = 2*(x-xMin)/xRange-1
#     return x

# def fitBeam(x,y,img,beamMask,method):
#     x = setRange2one(x)
#     y = setRange2one(y)
#     (Ny,Nx) = np.shape(img)
#     (X,Y) = np.meshgrid(x,y)
#     imgMean = np.mean(img)
#     I = img[beamMask]/imgMean
#     XY = np.zeros((np.size(I),2))
#     XY[:,0] = X[beamMask]
#     XY[:,1] = Y[beamMask]
#     XYfull = np.zeros((np.size(X),2))
#     XYfull[:,0] = X.flatten()
#     XYfull[:,1] = Y.flatten()

#     if method.lower() in 'polynomial':
#         pGuess = (0, 0, -0.1 ,-0.1  ,-0.5)
#         (pFit,pcov) = sci.optimize.curve_fit(polyBeam, XY, I,p0=pGuess,ftol=0.1, xtol=0.5e-3, maxfev=400)
#         Ibeam = polyBeam(XYfull,*pFit)*np.max(img)
#     elif method.lower() in 'gaussian':
#         pGuess = (1,0,1,0,1,0)
#         #(pFit,pcov) = sci.optimize.curve_fit(gauss2Dbeam, XY, I,p0=pGuess)
#         a = (XY,I)
#         z = optimize.minimize(gauss2DbeamFit,pGuess,args=a, tol=0.01,method='Nelder-Mead')
#         pFit = z.x
#         Ibeam = gauss2Dbeam(XYfull,*pFit)*imgMean



#     imgBeam = np.reshape(Ibeam,(Nx,Ny),order='C')
#     return imgBeam, pFit
