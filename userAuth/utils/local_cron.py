import os
import json
import urllib
import urllib2
import logging

logger=logging.getLogger ('django')

def get_apk():
    url='http://47.93.220.141/'

    req=urllib2.Request(url+'p2c/')
    res_data=urllib2.urlopen(req)
    res=res_data.read()
    res_dict = json.loads(res)

    def Schedule(a,b,c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        if int(per)%2==0:
            pre = int(per)
            print '%.2f%%' % int(per)

    local = os.path.join('./',res_dict['app_file'])

    urllib.urlretrieve(url + '/pageGet/media/'+res_dict['app_file'],local,Schedule)


def get_po():
    print 123

if __name__ == '__main__':
    get_apk()