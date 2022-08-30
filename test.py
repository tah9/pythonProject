myjson='{ "nihao":"你好", "a":"b"}'
import json
data=json.loads(myjson)
a=0
while True:
   print(str(a))
   a=a+1
   if a == 3:
       break

# try:
#     print('nihao' in data)
# except KeyError:
#     print('不好')

