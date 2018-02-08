import oss2

auth = oss2.Auth('LTAIeEscH1ag5dWj', '1R6ukC8o98clQxNsLDCPI3Is0t4003')
service = oss2.Service(auth, 'oss-cn-huhehaote.aliyuncs.com')

print([b.name for b in oss2.BucketIterator(service)])