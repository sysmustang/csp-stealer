import hashlib
import secrets
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'config.env')


username = input("Enter your login [admin]: ").strip()
if not username:
    username = 'admin'

password = input("Enter your password: ").strip()
while not password:
    password = input("Enter your password: ").strip()
password_hash = hashlib.md5(bytes(password, 'utf-8')).hexdigest()


with open(os.path.join(current_dir, 'config-sample.env')) as f:
    config_template = f.read()

config = config_template.format(
    LOGIN=username, 
    PASSWD_HASH=password_hash, 
    SEC_KEY=secrets.token_hex(16)
)
with open(config_file, 'w') as f:
    f.write(config)

# restart app to apply changes if it's docker
if os.name == 'posix':
    first_process = os.popen('ps -o pid=,comm=').read().split('\n')[0].strip()
    if first_process == '1 gunicorn.sh':
        os.popen('pkill -f gunicorn')
