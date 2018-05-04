# -*- coding: utf-8 -*-
import oss2
import time

auth = oss2.Auth('LTAIeEscH1ag5dWj', '1R6ukC8o98clQxNsLDCPI3Is0t4003')
service = oss2.Service(auth, 'oss-cn-huhehaote.aliyuncs.com')

print([b.name for b in oss2.BucketIterator(service)])

bucket = oss2.Bucket(auth, 'oss-cn-huhehaote.aliyuncs.com', 'apk2ali')

from itertools import islice
print(time.strftime('%Y-%m-%d %H:%M:%S'))

# for b in islice(oss2.ObjectIterator(bucket), 10):
#     print(b.key)
#     bucket.delete_object(b.key)
# print time.strftime('%Y-%m-%d %H:%M:%S')
#
for b in islice(oss2.ObjectIterator(bucket), 10):
    print(b.key)
#
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# bucket.put_object_from_file(
#     'qq.apk',
#     '/Users/lvjinzhao/Documents/onlineAutoTest/dailyTest/pageGet/media/appfile/dFSJ3D-release_2017_09_04_1843正式_205_5.0.3.apk'
#     )
print(time.strftime('%Y-%m-%d %H:%M:%S'))
bucket.get_object_to_file('qq.apk', 'local-backup2.apk')
print(time.strftime('%Y-%m-%d %H:%M:%S'))