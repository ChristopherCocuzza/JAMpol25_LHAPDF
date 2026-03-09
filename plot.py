#!/usr/bin/env python
import sys,os
import numpy as np
import copy
from subprocess import Popen, PIPE, STDOUT
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
from matplotlib.ticker import MultipleLocator
import pylab  as py
import lhapdf

cwd = os.getcwd()

#--index conventions:
#--908: g1    
#--909: g2    

#--mode 0: plot each replica
#--mode 1: plot 68% CI for replicas

cwd = '/ceph24/JAM/ccocuzza/JAMpol25_LHAPDF/'

os.environ["LHAPDF_DATA_PATH"] = cwd

X1=10**np.linspace(-4,-1)
X2=np.linspace(0.101,0.99)
X=np.append(X1,X2)

idxs = {}
idxs['g1'] = 908
idxs['g2'] = 909

def plot_pstf(Q2,mode=1):

    nrows,ncols=4,2
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11=py.subplot(nrows,ncols,1)
    ax12=py.subplot(nrows,ncols,2)
    ax21=py.subplot(nrows,ncols,3)
    ax22=py.subplot(nrows,ncols,4)
    ax31=py.subplot(nrows,ncols,5)
    ax32=py.subplot(nrows,ncols,6)
    ax41=py.subplot(nrows,ncols,7)
    ax42=py.subplot(nrows,ncols,8)

    hand = {}
    kinds = ['full', 'LT']
    tars = ['p','n','d','h']
    stfs = ['g1','g2']


    for kind in kinds:
        for tar in tars:
            if tar=='p' and kind=='full':  tablename = 'JAMpol25-PSTF_proton'
            if tar=='n' and kind=='full':  tablename = 'JAMpol25-PSTF_neutron'
            if tar=='d' and kind=='full':  tablename = 'JAMpol25-PSTF_deuteron'
            if tar=='h' and kind=='full':  tablename = 'JAMpol25-PSTF_helium'
            if tar=='p' and kind=='LT':    tablename = 'JAMpol25-PSTF_proton_LT_only'
            if tar=='n' and kind=='LT':    tablename = 'JAMpol25-PSTF_neutron_LT_only'
            if tar=='d' and kind=='LT':    tablename = 'JAMpol25-PSTF_deuteron_LT_only'
            if tar=='h' and kind=='LT':    tablename = 'JAMpol25-PSTF_helium_LT_only'
            STF = lhapdf.mkPDFs(tablename)
            for stf in stfs:
                data = [] 
                if stf=='g1' and tar=='p': ax = ax11
                if stf=='g1' and tar=='n': ax = ax21
                if stf=='g1' and tar=='d': ax = ax31
                if stf=='g1' and tar=='h': ax = ax41
                if stf=='g2' and tar=='p': ax = ax12
                if stf=='g2' and tar=='n': ax = ax22
                if stf=='g2' and tar=='d': ax = ax32
                if stf=='g2' and tar=='h': ax = ax42

                nrep = len(STF)


                for i in range(nrep):
                    _stf =  np.array([STF[i].xfxQ2(idxs[stf],x,Q2)*x for x in X])
                    data.append(_stf)

                #print(np.mean(data,axis=0))
                #print(np.std(data,axis=0))

                p = 16
                do = np.percentile(data,p    ,axis=0)
                up = np.percentile(data,100-p,axis=0)

                if kind=='full': color = 'red'
                if kind=='LT':   color = 'blue'

                #--plot each replica
                if mode==0:
                    for i in range(nrep):
                        hand[kind] ,= ax.plot(X,data[i],color=color,alpha=0.1)
                
                #--plot 68% CI
                if mode==1:
                    hand[kind] = ax.fill_between(X,do,up,color=color,alpha=0.9)


    for ax in [ax11,ax12,ax21,ax22,ax31,ax32,ax41,ax42]:
          ax.set_xlim(1e-4,1)
          #ax.semilogx()
            
          ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
          ax.set_xticks([0.0001,0.001,0.01,0.1,1])
          ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])

    for ax in [ax11,ax12,ax21,ax22,ax31,ax32]:
          ax.tick_params(labelbottom=False)

    #ax13.axhline(0,0,1,ls='--',color='black',alpha=0.5)

    #ax11.set_ylim(0,0.4)   
    #ax12.set_ylim(0,0.015) 
    #ax13.set_ylim(-1.0,2.0)

    ax41.set_xlabel(r'$x$' ,size=35)
    ax42.set_xlabel(r'$x$' ,size=35)   

    ax11.text(0.40,0.85,r'$Q^2 = %s$'%Q2 + ' ' + r'\textrm{GeV}' + r'$^2$', transform=ax11.transAxes,size=30)

    ax11.text(0.05,0.85,r'\boldmath$xg_1^p$'          ,transform=ax11.transAxes,size=30)
    ax12.text(0.05,0.85,r'\boldmath$xg_2^p$'          ,transform=ax12.transAxes,size=30)
    ax21.text(0.05,0.85,r'\boldmath$xg_1^n$'          ,transform=ax21.transAxes,size=30)
    ax22.text(0.05,0.85,r'\boldmath$xg_2^n$'          ,transform=ax22.transAxes,size=30)
    ax31.text(0.05,0.85,r'\boldmath$xg_1^D$'          ,transform=ax31.transAxes,size=30)
    ax32.text(0.05,0.85,r'\boldmath$xg_2^D$'          ,transform=ax32.transAxes,size=30)
    ax41.text(0.05,0.85,r'\boldmath$xg_1^{^3{\rm H}}$',transform=ax41.transAxes,size=30)
    ax42.text(0.05,0.85,r'\boldmath$xg_2^{^3{\rm H}}$',transform=ax42.transAxes,size=30)

    handles,labels=[],[]
    handles.append(hand['full'])
    handles.append(hand['LT'])
    labels.append(r'\textrm{\textbf{JAMpol25}}')
    labels.append(r'\textrm{\textbf{JAMpol25 (LT only)}}')
    ax11.legend(handles,labels,frameon=False,loc='lower left',fontsize=28, handletextpad = 0.5, handlelength = 1.5, ncol = 1, columnspacing = 0.5)

    py.tight_layout()

    filename = 'gallery/pstfs.png'
    if mode==1: filename += '-CI'
    filename+='.png'
    py.savefig(filename)
    print ('Saving figure to %s'%filename)
    py.clf()


if __name__=="__main__":

    Q2 = 10
    #plot_pstf(Q2,mode=0)
    plot_pstf(Q2,mode=1)







