import os
import datetime
import numpy as np

class LLCRegion:
    """ A class the describes a region MITgcm Lat-Lon-Cap setup """

    def __init__(self,
                 grid_dir = None,
                 data_dir = None,
                 Nlon = None,
                 Nlat = None,
                 Nz   = None,
                 tini = '20110913T000000',
                 tend = '20120128T120000',
                 dt   = 1.,
                 dtype = np.dtype('>f4')
                ):

        self.grid_dir = grid_dir     # Grid directory
        self.data_dir = data_dir     # Parent data directory
        self.Nlon = Nlon             # Number of longitude points in the regional subset
        self.Nlat = Nlat             # Number of latitude points in the regional subset
        self.Nz = Nz                 # Number of vertical levels in the regional subset

        self.tini = parse_time(tini) # Initial time
        self.tend = parse_time(tend) # End time
        self.dt   = datetime.timedelta(hours=dt)  # Time interval at which outputs are saved [hours]
        self.dtype = dtype           # Data type (default >f4, mean float single precision)

        self.grid_size = str(Nlon)+ 'x' + str(Nlat)  # grid size string

    def load_grid(self):

        self.lon = np.memmap(self.grid_dir+'/XC_'+self.grid_size,
                             dtype=self.dtype,shape=(self.Nlat,self.Nlon),
                             mode='r')

        self.lat = np.memmap(self.grid_dir+'/YC_'+self.grid_size,
                             dtype=self.dtype,shape=(self.Nlat,self.Nlon),
                             mode='r')

        self.dx = np.memmap(self.grid_dir+'/DXC_'+self.grid_size,
                             dtype=self.dtype,shape=(self.Nlat,self.Nlon),
                             mode='r')

        self.dy = np.memmap(self.grid_dir+'/DYC_'+self.grid_size,
                             dtype=self.dtype,shape=(self.Nlat,self.Nlon),
                             mode='r')

        try:
            self.z = np.memmap(self.grid_dir+'/RF.data',dtype=self.dtype,
                               shape=(self.Nz), mode='r')
        except:
             # this is a temporary hack
            self.z = np.memmap('/u/cbarbedo/llc/TropicalPacific/grid/RF.data',
                               dtype=self.dtype,shape=(self.Nz), mode='r')[:self.Nz]
        try:
            self.hb = np.memmap(self.grid_dir+'Depth_'+self.grid_size,
                                dtype=self.dtype,shape=(self.Nlat,self.Nlon),
                                mode='r')
        except:
            pass

    def load_2d_data(self, fni):
        return np.memmap(fni,dtype=self.dtype,
                         shape=(self.Nlat,self.Nlon), mode='r')

    def load_3d_data(self, fni):
        return np.memmap(fni,dtype=self.dtype,
                         shape=(self.Nz, self.Nlat,self.Nlon), mode='r')

    def init_time_series(self):

        delta = self.tend-self.tini
        delta_sec = delta.days * 24 * 60 * 60 + delta.seconds

        self.t = self.tini
        for sec in range(self.dt.seconds,delta_sec+self.dt.seconds,
                        self.dt.seconds):

            self.t = np.vstack([self.t, (self.tini +
                     datetime.timedelta(seconds=sec))])

# utils
def parse_time(ts):
    """ Converts MITgcm time in string format
        into datetime

        Parameters
        ----------
        ts: MITgcm time in string format (e.g.,
            20121009T180000 corresponds to
            Oct. 9th 2012, 18 h 0 min 0 sec)

        Return
        -------
        The associated time date object """

    return datetime.datetime(int(ts[:4]),int(ts[4:6]),
                             int(ts[6:8]),int(ts[9:11]),
                             int(ts[11:13]),int(ts[13:15]))
