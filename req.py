import requests
from bs4 import BeautifulSoup

s = requests.session()
soup = BeautifulSoup(s.get('https://www.bigbasket.com/').content,'lxml')
csrftoken = soup.find('input', dict(name='csrfmiddlewaretoken'))['value']


payload = {'identifier': 8606358178,
           'csrfmiddlewaretoken':csrftoken,
           }


head = {
'access-control-allow-origin':'https://business.bigbasket.com',
'content-length':'58',
'content-type':'application/json',
'date': 'Tue, 06 Jul 2021 10:06:04 GMT',
'server': 'nginx',
'set-cookie':' _bb_cid=1; Domain=.bigbasket.com; expires=Mon, 01-Jul-2041 10:06:04 GMT; Max-Age=630720000; Path=/; secure',
'set-cookie':' ts="2021-07-06 15:36:04.632"; Domain=.bigbasket.com; expires=Wed, 06-Jul-2022 10:06:04 GMT; Max-Age=31536000; Path=/; secure',
'set-cookie': '_bb_rd=1; Domain=.bigbasket.com; expires=Wed, 06-Jul-2022 10:06:04 GMT; Max-Age=31536000; Path=/; secure',
'set-cookie': '_bb_aid="MzAwNDkxOTI2MA=="; Domain=.bigbasket.com; expires=Mon, 01-Jul-2041 10:06:04 GMT; Max-Age=630720000; Path=/; secure',
'via': '1.1 679e2d9de234c68f799a62d542db3975.cloudfront.net (CloudFront)',
'x-amz-cf-id':'bCmkr9cA-TEQpc9W8wNHho673eDu2YuZHBmnAWCGVnbl3h61SgyCzg==',
'x-amz-cf-pop':'MAA51-C2',
'x-cache':'Miss from cloudfront',
'x-content-type-options':'nosniff',
'x-frame-options':'SAMEORIGIN',
}


response = s.post('https://business.bigbasket.com/mapi/v4.0.0/member-svc/otp/send/',data=payload,headers=head)
print(response,'HELLOMW')