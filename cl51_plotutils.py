#!/usr/bin/env python

# ==============================================================================
# PLOTTING UTILITIES MODULE FOR VAISALA CL51 CEILOMETER
#
# Author:        Chris Walden, NCAS
# History:       
# Version:	 0.1
# Last modified: 13/09/21
# ==============================================================================
module_version = 0.1

# ------------------------------------------------------------------------------
# Import required tools
# ------------------------------------------------------------------------------
import numpy as np
import numpy.ma as ma;
import os, re, sys, getopt, shutil, zipfile, string, pwd, getpass, socket
import glob
import netCDF4 as nc4

from datetime import tzinfo, datetime, time, timedelta

import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt  #import plotting package
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

from matplotlib.ticker import LogFormatter 
from matplotlib import colors
from matplotlib import rcParams

rcParams['axes.labelsize'] = 14
rcParams['axes.titlesize'] = 14
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12

import pyart
import cmocean
import cftime
import colorcet

# ------------------------------------------------------------------------------
# Quicklook generation
# ------------------------------------------------------------------------------
def make_quicklook(ncfile,figpath,colormap='pyart_HomeyerRainbow',qc_threshold=2,montage=False):
    
    '''Produce quicklooks for CL51 ceilometer attenuated backscatter

    Parameters:
    ===========
        ncfile (str):  Full path to NetCDF file
        figpath (str): Path to store quicklook file
        
    Keyword arguments:
        colormap       -- the chosen colormap (default 'pyart_HomeyerRainbow')
        qc_threshold   -- qc_flag threshold, data are masked for qc_flag > qc_threshold (default 2)
        montage (bool) -- when True plot both thresholded and unthresholded data (default False)
    '''

    head_tail = os.path.split(ncfile);
    
    tail = head_tail[1];
    
    Figurename=tail.replace(".nc",".png");

    print('Opening NetCDF file ' + ncfile)
    DS = nc4.Dataset(ncfile,'r',format='NETCDF3_CLASSIC')

    myFmt = mdates.DateFormatter('%H:%M')
        
    hmax = 12;

    DS.set_auto_mask(True);

    dtime0 = cftime.num2pydate(DS['time'][:],DS['time'].units)

    title_date = dtime0[0].strftime("%d-%b-%Y");
    instrument_str = "Chilbolton CL51 Ceilometer"

    dt_min = dtime0[0].replace(hour=0, minute=0, second=0, microsecond=0)
    dt_max = dt_min+timedelta(days=1)    
    
    if montage:
    
        fig, axs = plt.subplots(2, 1, figsize = (15, 8.5), constrained_layout=True);
        fig.set_constrained_layout_pads(w_pad=4 / 72, h_pad=4 / 72, hspace=0.2, wspace=0.2)

        axs[0].set_ylim(0,hmax);
        axs[1].set_ylim(0,hmax);

        axs[0].set_xlim(dt_min,dt_max);
        axs[1].set_xlim(dt_min,dt_max);

        var        = DS['attenuated_aerosol_backscatter_coefficient'][:,:];
        qc_flag    = DS['qc_flag'][:,:];
        var_masked = np.ma.masked_where(qc_flag >qc_threshold, var[:,:]);

        axs[0].xaxis.set_major_formatter(myFmt);
        h0=axs[0].pcolormesh(dtime0[:],DS['altitude'][:]/1000.,var_masked.transpose(),
                          norm=colors.LogNorm(vmin=1e-7,vmax=1e-4),
                          cmap=plt.get_cmap(colormap),shading='auto')
        cb0=plt.colorbar(h0,ax=axs[0],orientation='vertical')

        cb0.ax.set_ylabel('$\mathrm{m}^{-1} \mathrm{sr}^{-1}$');
        axs[0].set_title(title_date, loc='right')
        axs[0].set_title("Attenuated backscatter coefficient (calibrated)",loc='left')

        axs[0].grid(True)
        axs[0].set_xlabel('Time (UTC)')
        axs[0].set_ylabel('Altitude (km)')

        axs[1].xaxis.set_major_formatter(myFmt);
        h1=axs[1].pcolormesh(dtime0[:],DS['altitude'][:]/1000.,var.transpose(),
                          norm=colors.LogNorm(vmin=1e-7,vmax=1e-4),
                          cmap=plt.get_cmap(colormap),shading='auto');

        cb1=plt.colorbar(h1,ax=axs[1],orientation='vertical')
        cb1.ax.set_ylabel('$\mathrm{m}^{-1} \mathrm{sr}^{-1}$')

        axs[1].set_title(title_date,loc='right')
        axs[1].grid(True)
        axs[1].set_xlabel('Time (UTC)')
        axs[1].set_ylabel('Altitude (km)')

        plt.gcf().text(0.0, 0.0, instrument_str,horizontalalignment='left',fontsize=12)
	
    else:

        fig, axs = plt.subplots(1, 1, figsize = (15, 4), constrained_layout=True)
        fig.set_constrained_layout_pads(w_pad=4 / 72, h_pad=4 / 72, hspace=0.2, wspace=0.2)

        axs.set_ylim(0,hmax);
        axs.set_xlim(dt_min,dt_max);

        var        = DS['attenuated_aerosol_backscatter_coefficient'][:,:];
        qc_flag    = DS['qc_flag'][:,:];
        var_masked = np.ma.masked_where(qc_flag >qc_threshold, var[:,:]);

        axs.xaxis.set_major_formatter(myFmt);
        h0=axs.pcolormesh(dtime0[:],DS['altitude'][:]/1000.,var_masked.transpose(),norm=colors.LogNorm(vmin=1e-7,vmax=1e-4),cmap=plt.get_cmap(colormap),shading='auto')
        cb0=plt.colorbar(h0,ax=axs,orientation='vertical')

        cb0.ax.set_ylabel('$\mathrm{m}^{-1} \mathrm{sr}^{-1}$');
        axs.set_title(title_date, loc='right')
        axs.set_title("Attenuated backscatter coefficient (calibrated)",loc='left')

        axs.grid(True)
        axs.set_xlabel('Time (UTC)')
        axs.set_ylabel('Altitude (km)')
        
        plt.gcf().text(0.0, 0.0, instrument_str,horizontalalignment='left',fontsize=12)


    DS.close()

    plt.savefig(os.path.join(figpath,Figurename),dpi=200)

    plt.close()

