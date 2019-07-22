import json
import sys

config_guid = sys.argv[1]
config_list = []
with open(f'config_{config_guid}.json') as file:
    txt = file.read()
    config_list = json.loads(txt)

config_obj = config_list[0]

print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
import time
print(time.time())
for i in range(15):
    print(i+1)
    with open(f'result_abc_{str(i+1)}.json', 'w') as file:
        file.write('[{"id": "' + str(i+1) + '", "config": ' + json.dumps(config_obj) + ', "label": "categoria","config": {"a": "params"},"result": {"real": [123],"pred": [122],"metrics": {"free": 123,"to": "abc","write": [1,2,3]}},"start": 123,"end": 123}]')
    with open(f'result_abc_{str(i+1+15)}.json', 'w') as file:
        file.write('{"id": "' + str(i+1+15) + '", "config": ' + json.dumps(config_obj) + ', "label": "categoria","config": {"a": "params"},"result": {"real": [123],"pred": [122],"metrics": {"free": 123,"to": "abc","write": [1,2,3]}},"start": 123,"end": 123}')
    time.sleep(1)
print(time.time())