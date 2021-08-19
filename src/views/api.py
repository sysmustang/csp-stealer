from flask import jsonify, request
from src import webapp, db
from src.model import Event
from src import payload
import flask_login
import os


@webapp.route('/api/makePayload', methods=['POST'])
@flask_login.login_required
def make_payload():
    args = request.get_json(force=True)
    if not args.get('grubbers') or not args.get('payload_type'):
        return jsonify({'success': 0, 'error': 'Invalid request'})

    ptype = args.get('payload_type').upper()
    domain = request.headers.get("Host")
    host = f'//{domain}' if request.url.startswith('https:') else f'http://{domain}'

    try:
        response = payload.make_payload(host, args['grubbers'], f'PAYLOAD_{ptype}')
    except Exception as e:
        return jsonify({'success': 0, 'error': str(e)})

    return jsonify({'success': 1, 'payload': response})


@webapp.route('/api/delete', methods=['POST'])
@flask_login.login_required
def del_event():
    args = request.get_json(force=True)
    if args.get('action') not in ['delete_one', 'delete_all']:
        return jsonify({'success': False, 'error': 'Invalid action'})
    elif args['action'] == 'delete_one' and not isinstance(args.get('id'), int):
        return jsonify({'success': False, 'error': 'Invalid id'})

    if args['action'] == 'delete_one':
        event = db.session.query(Event).filter_by(id=args['id']).one()
        if not event:
            return jsonify({'success': False, 'error': 'Invalid id'})

        if os.path.exists(f'src/static/upload/f{event.img_path}'):
            os.remove(f'src/static/upload/f{event.img_path}')
        db.session.delete(event)
    else:
        for screenfile in os.listdir('src/static/upload'):
            os.remove(f'src/static/upload/{screenfile}')
        db.session.query(Event).delete()

    db.session.commit()
    return jsonify({'success': True})
