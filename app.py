
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from functools import wraps

app = Flask(__name__, static_folder='static')
app.static_folder = 'static'
app.template_folder = 'templates'

# Serve attached_assets
from flask import send_from_directory

@app.route('/attached_assets/<path:filename>')
def attached_assets(filename):
    return send_from_directory('attached_assets', filename)
app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/prepare')
def prepare():
    return render_template('prepare.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking')
def booking():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('booking.html', today=today)

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('portal'))
    return render_template('login.html')

@app.route('/auth-callback', methods=['POST'])
def auth_callback():
    # Handle Replit Auth callback
    data = request.get_json()
    if data and 'id' in data:
        session['user_id'] = data['id']
        session['username'] = data.get('name', 'User')
        # Set admin status - you might want to have a proper admin list
        if data.get('id') == 'your-admin-id':
            session['is_admin'] = True
        return jsonify({"success": True, "redirect": url_for('portal')})
    return jsonify({"success": False}), 400

@app.route('/portal')
@login_required
def portal():
    is_admin = session.get('is_admin', False)
    return render_template('portal.html', is_admin=is_admin)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
