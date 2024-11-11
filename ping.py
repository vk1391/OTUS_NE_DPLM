import subprocess
import ipaddress
for ip in ipaddress.IPv4Network('10.0.2.0/24'):
    def ping(host):
        result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
        return 'Успех!' if result.returncode == 0 else 'Ошибка!'
    print(ping(f'{ip}'))
