import requests
import urllib.request
import json      
import datetime
from pprint import pprint
import time

#BLOCK CHAIN SERVER IP:PORT
host = 'http://54.238.152.114:9000/'

def run_transaction(_id, card, element, amount):
    body = {
            "jsonrpc":"2.0",
            "id": _id,
            "method": "invoke_foo1",
            "params": {
                "card" : card,
                "ts" : int(time.mktime(datetime.datetime.now().timetuple())),
                "element": element,
                "amount": amount
                }
            }

    prefix = 'api/v1/transactions'
    req = urllib.request.Request(host+prefix)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return response.status

#input:tx_hash
#localhost:9000/api/v1/transactions/result?hash={tx_hash}
def is_valid(tx_hash):
    prefix = 'api/v1/transactions/result?hash={}'.format(tx_hash)
    response = requests.get(host+prefix)
    assert response.status_code == requests.codes.ok
    ret = json.loads(response.text)
    pprint('is_valid', ret)
    return ret['response']['code']

#input: channel
#localhost:9000/api/v1/blocks?channel=channel1
def check_last(min_time, lim_time):
    main = []
    prefix = 'api/v1/blocks?channel=channel1'
    response = requests.get(host+prefix)
    assert response.status_code == requests.codes.ok
    ret = json.loads(response.text)
    ret = check_chain(ret['block_data_json']['block_hash'])
    while ret['block_data_json']['height'] != '0':
      ret = check_chain(ret['block_data_json']['prev_block_hash'])
      if ret['tx_data_json'] =='':
        break
      cur = json.loads(ret['tx_data_json'][0]['data_string'])
      print(cur['params']['ts'])
      if int(cur['params']['ts']) < min_time:
        break
      if int(cur['params']['ts']) < lim_time:
        main.append({'card': cur['params']['card'], 'ts': cur['params']['ts'], 'element': cur['params']['element'], 'amount': cur['params']['amount']})

    return main

#input: hash, channel
#localhost:9000/api/v1/blocks?channel=channel1&hash={hash}
def check_chain(_hash):
    prefix = 'api/v1/blocks?channel=channel1&hash={}'.format( _hash)
    response = requests.get(host+prefix)
    assert response.status_code == requests.codes.ok
    ret = json.loads(response.text)
    return ret
if __name__ == '__main__':
  ret = check_last(1527946447, 1527946730)
  for x in ret:
    print(x)

	#for x in range(11,20):
	#   run_transaction(str(x), '1238-1241-2387-7812', 'corn', str(x*10))
	#   time.sleep(2)
