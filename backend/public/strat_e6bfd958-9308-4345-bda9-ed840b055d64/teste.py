print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
import time
print(time.time())
for i in range(15):
    print(i+1)
    with open(f'result_abc_{str(i+1)}.json', 'w') as file:
        file.write('{"id": "' + str(i+1) + '","label": "categoria","config": {"a": "params"},"result": {"real": [123],"pred": [122],"metrics": {"free": 123,"to": "abc","write": [1,2,3]}},"start": 123,"end": 123}')
    time.sleep(1)
print(time.time())