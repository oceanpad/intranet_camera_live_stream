import requests

for j in range(10, 256):
    for i in range(1, 256):
        try:
            ip = 'http://192.168.' + str(j) + '.' + str(i)
            print ip
            r = requests.get(ip, timeout=0.2)
            if r.status_code == 200:
                print '@@@@@@@@@@@@@@@@@@@@@@@@@@'
                with open('available_ips.txt', 'a') as the_file:
                    the_file.write(ip + '\n')
        except Exception as err:
            pass

