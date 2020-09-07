import time
import numpy as np
import matplotlib as plt
import os
import requests
import re
import csv
from scipy.interpolate import interp1d
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def getMu(materialType,name,Eaxis_MeV):
#     driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
#     # Open the website
#     driver.get('https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html')

#     # navigate first page 
#     if 'el' in materialType.lower():
#         driver.find_element_by_css_selector("input[type='radio'][name='Method'][value='Elem']").click()
#     elif 'com' in materialType.lower():
#         driver.find_element_by_css_selector("input[type='radio'][name='Method'][value='Comp']").click()
#     elif 'mix' in materialType.lower():
#         driver.find_element_by_css_selector("input[type='radio'][name='Method'][value='Mix']").click()
        
#     driver.find_element_by_css_selector("input[type='radio'][name='Output2'][value='File']").click()
            
#     driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()


    
#     nE=np.size(Eaxis_MeV)
#     mu = []
#     driver.implicitly_wait(2)
#     Nloop = np.uint16(np.ceil(nE/100))
#     filePath ='/Users/streeter/Google Drive/Colab Notebooks/testfile.txt'
#     for n in range(0,Nloop):
#         if n>=(Nloop-1):
#             ind = range((n)*100,nE)
#         else:
#             ind = range((n)*100,(n+1)*100)
#         Etemp = Eaxis_MeV[ind]
#         file = open(filePath,'w') 
#         for E in Etemp:
#             s = "%8.6e" % E
#             file.write(s + '\n') 

#         file.close() 

#         if 'el' in materialType.lower():
#             a=driver.find_element_by_css_selector("input[type='text'][name='ZSym']")
#         elif 'com' in materialType.lower():
#             a=driver.find_element_by_css_selector("input[type='text'][name='ZSym']")
#         elif 'mix' in materialType.lower():
#             a=driver.find_element_by_css_selector("input[type='text'][name='ZSym']")
#         a.clear()
#         a.send_keys(name)
#         b=driver.find_element_by_css_selector("input[type='checkbox'][name='Output']")
#         if b.is_selected():
#             b.click()
            
#         c = driver.find_element_by_css_selector("input[type='file'][name='userfile']")
#         c.send_keys(filePath)
#         driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()
#         time.sleep(2)
#         a = driver.find_element_by_css_selector("input[type='checkbox'][name='with']")
#         if ~a.is_selected():    
#             a.click()
            
        
#         driver.find_element_by_css_selector("input[type='submit'][value='Download data']").click()
#         a=driver.find_element_by_xpath('//pre')
#         fText=a.text.split(sep='\n')
#         ftLines = fText[3:]
        
#         for s in ftLines:
#             fStr = s.split(sep=' ')
#             fStr = fStr[1]
#             mu.append(float(fStr))
            
#         driver.back()
#         driver.back()

#     driver.close()
#     return np.array(mu)

def getMu_element(name,Eaxis_MeV):
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # Open the website
    driver.get('https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html')

    # navigate first page 
    
    driver.find_element_by_css_selector("input[type='radio'][name='Method'][value='Elem']").click()
  
    driver.find_element_by_css_selector("input[type='radio'][name='Output2'][value='File']").click()
            
    driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()
   
    nE=np.size(Eaxis_MeV)
    mu = []
    driver.implicitly_wait(2)
    Nloop = np.uint16(np.ceil(nE/100))
    filePath ='/Users/streeter/Google Drive/python/testfile.txt'
    for n in range(0,Nloop):
        if n>=(Nloop-1):
            ind = range((n)*100,nE)
        else:
            ind = range((n)*100,(n+1)*100)
        Etemp = Eaxis_MeV[ind]
        file = open(filePath,'w') 
        for E in Etemp:
            s = "%8.6e" % E
            file.write(s + '\n') 
        file.close() 

        a=driver.find_element_by_css_selector("input[type='text'][name='ZSym']")
        a.clear()
        a.send_keys(name)

        b=driver.find_element_by_css_selector("input[type='checkbox'][name='Output']")
        if b.is_selected():
            b.click()
            
        c = driver.find_element_by_css_selector("input[type='file'][name='userfile']")
        c.send_keys(filePath)
        driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()
        time.sleep(2)
        a = driver.find_element_by_css_selector("input[type='checkbox'][name='with']")
        if ~a.is_selected():    
            a.click()
            
        
        driver.find_element_by_css_selector("input[type='submit'][value='Download data']").click()
        a=driver.find_element_by_xpath('//pre')
        fText=a.text.split(sep='\n')
        ftLines = fText[3:]
        
        for s in ftLines:
            fStr = s.split(sep=' ')
            fStr = fStr[1]
            mu.append(float(fStr))
            
        driver.back()
        driver.back()

    driver.close()
    return np.array(mu)

def getMu_compound(name,Eaxis_MeV):
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # Open the website
    driver.get('https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html')

    # navigate first page 
    
    driver.find_element_by_css_selector("input[type='radio'][name='Method'][value='Comp']").click()
  
    driver.find_element_by_css_selector("input[type='radio'][name='Output2'][value='File']").click()
            
    driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()
   
    nE=np.size(Eaxis_MeV)
    mu = []
    driver.implicitly_wait(2)
    Nloop = np.uint16(np.ceil(nE/100))
    filePath ='/Users/streeter/Google Drive/python/testfile.txt'
    for n in range(0,Nloop):
        if n>=(Nloop-1):
            ind = range((n)*100,nE)
        else:
            ind = range((n)*100,(n+1)*100)
        Etemp = Eaxis_MeV[ind]
        file = open(filePath,'w') 
        for E in Etemp:
            s = "%8.6e" % E
            file.write(s + '\n') 
        file.close() 

        a=driver.find_element_by_css_selector("input[type='text'][name='Formula']")
        a.clear()
        a.send_keys(name)

        b=driver.find_element_by_css_selector("input[type='checkbox'][name='Output']")
        if b.is_selected():
            b.click()
            
        c = driver.find_element_by_css_selector("input[type='file'][name='userfile']")
        c.send_keys(filePath)
        driver.find_element_by_css_selector("input[type='submit'][value='Submit Information']").click()
        time.sleep(2)
        a = driver.find_element_by_css_selector("input[type='checkbox'][name='with']")
        if ~a.is_selected():    
            a.click()
            
        
        driver.find_element_by_css_selector("input[type='submit'][value='Download data']").click()
        a=driver.find_element_by_xpath('//pre')
        fText=a.text.split(sep='\n')
        ftLines = fText[3:]
        
        for s in ftLines:
            fStr = s.split(sep=' ')
            fStr = fStr[1]
            mu.append(float(fStr))
            
        driver.back()
        driver.back()

    driver.close()
    return np.array(mu)

def saveMu2file(materialType,name,Eaxis_MeV,dirPath):
    if 'el' in materialType.lower():
        mu = getMu_element(name,Eaxis_MeV)
    elif 'com' in materialType.lower():
        mu = getMu_compound(name,Eaxis_MeV)
    elif 'cq' in materialType.lower():
        (Eaxis_MeV,mu) = getMu_compound_quick(name,Eaxis_MeV)
    

    #mu = getMu(materialType,name,Eaxis_MeV)
    filePath = os.path.join(dirPath,name +'.txt')
    nE = np.size(Eaxis_MeV)
    file = open(filePath,'w') 
    for n in range(0,nE):
        s = "%8.6e" % Eaxis_MeV[n] + ', ' "%8.6e" % mu[n]
        file.write(s + '\n') 

    file.close() 
    return mu, filePath

def getDensity(name,dirPath):
    filePath = os.path.join(dirPath,name +'.txt')   
    if os.path.exists(filePath):
        file = open(filePath,'r')
        s = file.readline() 
        rho_gpcc = np.float(s)

    else:    
        r = requests.get("http://physics.nist.gov/PhysRefData/XrayMassCoef/tab1.html")
        html = r.text
        rows = re.findall(r"<TR.*?>(.*?)</TR>", html, re.DOTALL)[3:]  # Pick the rows, excluding the headers
        output = []
        for row in rows:
            parsed_row = re.findall(r"<TD.*?>(.*?)</TD>", row)
            # Remove some cells with only "&nbsp;" (which are only in H, probably a bad formatting practice)
            parsed_row = list(filter(lambda s: s != "&nbsp;", parsed_row))
            # Remove trailing spaces
            parsed_row = list(map(lambda x: x.strip(), parsed_row))
            # Dictionary entries by atomic number (as string), symbol and name.
            output.append(parsed_row)

        matching = [s for s in output if name in s]
        rho_gpcc = np.float(matching[0][-1])
        filePath = saveRho2File(rho_gpcc,name,dirPath)
         

    return rho_gpcc

def saveRho2File(rho_gpcc,name,dirPath):
    filePath = os.path.join(dirPath,name +'.txt')   
    file = open(filePath,'w') 
    s = "%8.6e" % rho_gpcc
    file.write(s + '\n') 
    file.close()
    return filePath

def getMu_compound_quick(name,Eaxis_MeV):
    hPath = 'https://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/' + name + '.html'
    r = requests.get(hPath)
    html = r.text
    html = str(html).split("</DIV>")[2]  # Pick the div with the ascii table
    # How numbers are represented in the NIST web.
    number_pattern = r'-?[0-9]+\.?[0-9]*E[-+][0-9]+'
    lines = re.findall(number_pattern + "  " + number_pattern + "  " + number_pattern, html)
    data = []
    for l in lines:
        l2 = list(map(float, l.split("  ")))
        data.append([l2[0], l2[1], l2[2]])

    data = np.array(data)
    E_MeV = data[:,0]
    mu = data[:,1]
    f = interp1d(np.log10(E_MeV),np.log10(mu))
    mu = 10**(f(np.log10(Eaxis_MeV)))
    return Eaxis_MeV, mu

def loadMuFile(name,dirPath,Eaxis_MeV):

    filePath = os.path.join(dirPath,name +'.txt')
    
    a = csv.reader(open(filePath,'r') , delimiter=',')
    e_MeV = []
    mu = []
    for row in a:
        e_MeV.append(np.float(row[0]))
        mu.append(np.float(row[1]))
    e_MeV=np.array(e_MeV)
    mu=np.array(mu)
    f = interp1d(e_MeV,mu)
    mu = f(Eaxis_MeV)
    
    return mu