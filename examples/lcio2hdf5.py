from pyLCIO import EVENT, UTIL, IOIMPL, IMPL
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import h5py 
import awkward1 as ak 

import argparse

from functions import CellIDDecoder

hmap = np.array([1811, 1814, 1824, 1827, 1836, 1839, 1849,
                    1852, 1861, 1864, 1873, 1877, 1886, 1889, 1898, 1902,
                    1911, 1914, 1923, 1926, 1938, 1943, 1955, 1960,
                    1971, 1976, 1988, 1993, 2005, 2010])

def fill_record(inpLCIO, collection):

    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( inpLCIO )

    b = ak.ArrayBuilder()

    nEvt = 0
    for evt in reader:
        nEvt += 1
        if nEvt > nevents:
            break

        b.begin_list()
        ecalBarrel = evt.getCollection(collection)
        cellIDString = ecalBarrel.getParameters().getStringVal("CellIDEncoding")
        decoder = CellIDDecoder( cellIDString ) 
        
        
        mcparticle = evt.getCollection("MCParticle")    
        
        for enr in mcparticle:
            b.begin_record()
            b.field("E")
            b.real(enr.getEnergy())
            b.end_record() 
    
        
        for hit in ecalBarrel:

            l = decoder.layer( hit.getCellID0() ) 
            e = hit.getEnergy()
            pos = hit.getPosition()
            b.begin_record() 
            b.field("x")
            b.real(pos[0])
            b.field("y")
            b.real(pos[1])
            b.field("z")
            b.real(pos[2])
            b.field("e")
            b.real(e * 1000)
            b.field("layer")
            b.integer(l)
            b.end_record() 

        b.end_list()


    return b


def fill_numpy(record):
    
    binX = np.arange(-81, 82, 5.088333)
    binZ = np.arange(-77, 78, 5.088333)

    l = []
    E = []
    for i in range(0, nevents):

        z = ak.to_numpy(record[i].z)
        x = ak.to_numpy(record[i].x)
        y = ak.to_numpy(record[i].y)
        e = ak.to_numpy(record[i].e)

        incE = ak.to_numpy(record[i].E)
        E.append(incE.compressed()[0])


        layers = []

        for j in range(0,30):
            idx = np.where((y <= (hmap[j] + 0.9999)) & (y > (hmap[j] + 0.0001)))
            xlayer = x.take(idx)[0]
            zlayer = z.take(idx)[0]
            elayer = e.take(idx)[0]
            H, xedges, yedges = np.histogram2d(xlayer, zlayer, bins=(binX, binZ), weights=elayer)
            layers.append(H)


    l.append(layers)
    shower = np.asarray(l)
    e0 = np.reshape(np.asarray(E),(-1,1))

    return shower, e0

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='input LCIO file')
    parser.add_argument('--maxEvent', type=int, default=10, help='Number of events read')
    parser.add_argument('--collection', type=str, required=True, help='input collection in the LCIO file')
    parser.add_argument('--output', type=str, required=True, help='output name hdf5 file')

    opt = parser.parse_args()

    inpLCIO = str(opt.input)
    nevents = int(opt.maxEvent)
    collection = str(opt.collection)
    out = str(opt.output)

    record = fill_record(inpLCIO, collection)
    showers, e0 = fill_numpy(record)
    
    #Open HDF5 file for writing
    hf = h5py.File(out, 'w')
    grp = hf.create_group("ecal")


    ## write to hdf5 files
    grp.create_dataset('energy', data=e0)
    grp.create_dataset('layers', data=showers)

    hf.close()

    

    
