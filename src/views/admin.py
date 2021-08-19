from src import webapp, db, User
from src.model import Event
from flask import request, render_template
from flask import redirect, url_for
from src.payload import make_payload
import flask_login


@webapp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return redirect(url_for('login'))

    if not User.check_auth(username, password):
        return redirect(url_for('login'))

    flask_login.login_user(User())
    return redirect(url_for('index'))


@webapp.route('/admin/', defaults={'page_num': 1})
@webapp.route('/admin/page/<int:page_num>')
@flask_login.login_required
def index(page_num):
    domain = request.headers.get("Host")
    host = f'//{domain}' if request.url.startswith('https:') else f'http://{domain}'

    payload_dict = {}
    for ptype in ['JSURI', 'DATAURI', 'ANGULAR', 'UNSAFEINLINE', 'RAW']:
        payload = make_payload(host, ['current_url', 'cookie', 'dom', 'localstorage'], f'PAYLOAD_{ptype}')
        payload_dict[f'PAYLOAD_{ptype}'] = payload

    event = Event.query.order_by(Event.id.desc()).paginate(per_page=10, page=page_num)
    return render_template('index.html', **payload_dict, events=event)


@webapp.route('/admin/info/<int:event_id>')
@flask_login.login_required
def view_info(event_id):
    event = db.session.query(Event).filter_by(id=event_id)
    if not event.count():
        return redirect(url_for('index'))
    return render_template('info.html', event=event.one())
