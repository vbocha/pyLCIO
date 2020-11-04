from ROOT import TH1D, TCanvas, TF1, std
from pyLCIO import EVENT, UTIL, IOIMPL, IMPL
import matplotlib.pyplot as plt
import numpy as np

import math
import sys
import string




## returns fractional energy: first 20 layers and last 10 layers
def fracEsum(fName, maxEvt, collection):
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( fName )
    
    esum20l = []
    esum10l = []

    
    nEvt = 0

    for evt in reader:
        nEvt += 1
        if nEvt > maxEvt:
                break
        ecalBarrel = evt.getCollection(collection)
        cellIDString = ecalBarrel.getParameters().getStringVal("CellIDEncoding")
        decoder = CellIDDecoder( cellIDString ) 
        esum20 = 0.0
        esum10 = 0.0 
        for hit in ecalBarrel:
            l = decoder.layer( hit.getCellID0() ) 
            e = hit.getEnergy() 
            #print ("Energy:", hit.getEnergy(), " Cell ID0:", hit.getCellID0(), " layer: ", decoder.layer( hit.getCellID0() )) 
            if l < 20:
                esum20 += e 
            elif l >= 20:
                esum10 = esum10 + e*2
        
        esum20l.append(esum20)
        esum10l.append(esum10)
        
    esum20np = np.asarray(esum20l)
    esum10np = np.asarray(esum10l)
    
    return esum20np, esum10np
    


def Esumhit(fName, maxEvt, collection):
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( fName )
    
    esuml = []

    nEvt = 0

    for evt in reader:
        nEvt += 1
        if nEvt > maxEvt:
                break
        ecalBarrel = evt.getCollection(collection)
    
        cellIDString = ecalBarrel.getParameters().getStringVal("CellIDEncoding")
        decoder = CellIDDecoder( cellIDString ) 
        esum = 0.0
        for hit in ecalBarrel:
            l = decoder.layer( hit.getCellID0() ) 
            e = hit.getEnergy() 
            esum += e
        
        esuml.append(esum)
        
        
    esumnp = np.asarray(esuml)
    
    
    return esumnp

def nhits(fName, maxEvt, collection):
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( fName )
    
    esuml = []

    nEvt = 0
    nhits = []
    for evt in reader:
        nEvt += 1
        if nEvt > maxEvt:
                break
        col = evt.getCollection(collection)
        
        for c in col:
            hits = c.getCalorimeterHits().size()
        nhits.append(hits)    
     
    nphits = np.asarray(nhits)
    return nphits

def nhits_sim(fName, maxEvt, collection):
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( fName )
    
    nhits = []

    nEvt = 0
    #cut = 0.1e-03
    cut = 0.0
    for evt in reader:
        nEvt += 1
        if nEvt > maxEvt:
                break
        ecalBarrel = evt.getCollection(collection)
    
        cellIDString = ecalBarrel.getParameters().getStringVal("CellIDEncoding")
        decoder = CellIDDecoder( cellIDString ) 
        hits = 0
        for hit in ecalBarrel:
            if (hit.getEnergy() > cut):  
                hits += 1 
         
        
        nhits.append(hits)
        
        
    nsumnp = np.asarray(nhits)
    
    
    return nsumnp



class CellIDDecoder:

    """ decoder for LCIO cellIDs """

    def __init__(self,encStr):
        self.encStr=encStr
        self.funs = {} 

        tokens = encStr.split(',')
        
        offset = 0
        
        for t in tokens:
        
         # print "token: " , t
        
          st = t.split(':')
        
          if len(st)==2:
            name = st[0]
            start = offset 
            width = int(st[1])
            offset += abs( width )
        
          elif len(st)==3:
            name = st[0]
            start = int(st[1]) 
            width = int(st[2])
            offset = start + abs( width )
        
        
          else:
            print ("unknown token:" , t)
        
          mask = int(0x0)
          for i in range(0,abs(width)):
            mask = mask | ( 0x1 << ( i + start) )
        
          setattr( CellIDDecoder , name , self.makefun( mask, start , width) )


    def makefun(self, mask,start,width):
      if( width > 0 ):
        return ( lambda ignore, cellID : (( mask & cellID) >> start )  )
      else:
        return ( lambda ignore, cellID : (~(( mask & cellID) >> start )  ^ 0xffffffff) )
