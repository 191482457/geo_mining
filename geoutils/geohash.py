#-*- coding:utf8 -*-
#coding=utf-8
__author__ = 'feitianyu'
#提供geohash编码与经纬度之前的转换功能
import numpy as np;
class geohash:

    base32 =[ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
    bits = [16, 8, 4, 2, 1]

# 将经纬度编码成指定精度的geohash
    def encode(self, longitude, latitude, precision=12):
        lat_interval = [-90.0, 90.0];
        lng_interval = [ -180.0, 180.0];
        geohash="";
        is_even = 1; bit=0; ch = 0;
        while len(geohash) < precision :
            mid = 0.0;
            if (is_even==1) :
                mid = np.mean(lng_interval)
                if (longitude > mid):
                    ch|= self.bits[bit]
                    lng_interval[0] = mid;
                else:
                    lng_interval[1] = mid;

            else:
                mid = np.mean(lat_interval);
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

#将geohash解码成对应的经纬度，并给出对应的经纬度精度
    def decode_exactly(self, geohash):
        lat_interval = [-90.0, 90.0];
        lng_interval = [ -180.0, 180.0];
        decode_map={}
        for i, char in enumerate(self.base32): decode_map[char]=i

        is_even = 1;
        bsz = len(self.bits);
        for z in geohash:
            cd = decode_map[z];
            for mask in self.bits:
                if is_even==1:
                    lng_interval[0 if (cd & mask) != 0 else 1]=np.mean(lng_interval)
                else:
                    lat_interval[0 if (cd & mask) != 0 else 1]=np.mean(lat_interval)
                is_even = 1-is_even ;

        return [np.mean(lng_interval),np.mean(lat_interval),
                (lng_interval[1]-lng_interval[0])/2,(lat_interval[1]-lat_interval[0])/2];

#对结果进行规范化，去除当前精度无法准确指定的过多的小数位
    def decode(self, geohash):
        gap = self.decode_exactly(geohash);
        mgap=[np.round(-np.log10(item))-1 for item in gap[2:4]]
        return [np.round(gap[i], int(mgap[i]) if mgap[i]>0 else 0) for i in xrange(2)]



test=geohash();
print(test.encode(120.53916300000003,31.277631));
print(test.encode(120.53916300000003,31.277631,8));
print(test.decode("wtt9yvvvqj42"));
