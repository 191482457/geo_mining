#-*- coding:utf8 -*-
#coding=utf-8
__author__ = 'feitianyu'
#提供geohash编码与经纬度之前的转换功能
import numpy as np;
class geohash:

    base32 =[ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
    default_precision = 12;

    bits = [16, 8, 4, 2, 1]

    def encode(self, longitude, latitude, precision=12):
        lat_interval = [-90.0, 90.0];
        lng_interval = [ -180.0, 180.0];
        geohash="";
        is_even = 1;
        bit=0
        ch = 0;
        while len(geohash) < precision :
            mid = 0.0;
            if (is_even==1) :
                mid = (lng_interval[0] + lng_interval[1]) / 2;
                if (longitude > mid):
                    ch|= self.bits[bit]
                    lng_interval[0] = mid;
                else:
                    lng_interval[1] = mid;

            else:
                mid = (lat_interval[0]+lat_interval[1]) / 2;
                if (latitude > mid):
                     ch |= self.bits[bit];
                     lat_interval[0] = mid;
                else:
                    lat_interval[1] = mid;

            is_even = 1-is_even
            if (bit < 4):
                bit=bit+1;
            else:
                geohash=geohash+self.base32[ch];
                bit = 0; ch = 0;
        return geohash;

    def decode_exactly(self, geohash):
        lat_interval = [-90.0, 90.0];
        lng_interval = [ -180.0, 180.0];
        lat_err = 90.0; lon_err = 180.0;
        _decodemap={}
        for i, char in enumerate(self.base32):
            _decodemap[char]=i

        is_even = 1;
        bsz = len(self.bits);
        latitude=0
        longitude=0;
        for z in geohash:
            cd = _decodemap[z];
            for mask in self.bits:
                if is_even==1:
                    lon_err /= 2;
                    if ((cd & mask) != 0) :
                        lng_interval[0] = (lng_interval[0] + lng_interval[1]) / 2;
                    else :
                        lng_interval[1] = (lng_interval[0] + lng_interval[1]) / 2;
                else:
                    lat_err /= 2;
                    if (cd & mask) != 0:
                        lat_interval[0] = (lat_interval[0] + lat_interval[1]) / 2;
                    else:
                        lat_interval[1] = (lat_interval[0] + lat_interval[1]) / 2;
                is_even = 1-is_even ;


        latitude = (lat_interval[0] + lat_interval[1]) / 2;
        longitude = (lng_interval[0] + lng_interval[1]) / 2;
        return [ longitude,latitude, lon_err,lat_err,];


    def decode(self, geohash):
        gap = self.decode_exactly(geohash);
        mgap=[np.round(-np.log10(item))-1 for item in gap[2:4]]
        return [np.round(gap[i], int(mgap[i]) if mgap[i]>0 else 0) for i in xrange(2)]



test=geohash();
print(test.encode(120.53916300000003,31.277631));
print(test.encode(120.53916300000003,31.277631,8));
print(test.decode("wtt9yvvvqj42"));
