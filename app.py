from flask import Flask, render_template, request, session, send_from_directory, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'techhaven_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.get(session.get('user_id'))
        if not user or user.role != 'admin':
            flash("Admin access required.")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function



# ─── Models ──────────────────────────────────────────────
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── Routes ──────────────────────────────────────────────
@app.route('/')
@login_required
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        flash("Session expired. Please log in again.")
        return redirect(url_for('login'))

    return render_template('home-page.html', first_name=user.first_name, user=user)

@app.route('/products')
@login_required
def products():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        flash("Session expired. Please log in again.")
        return redirect(url_for('login'))

    items = Product.query.all()
    return render_template('products-page.html', products=items, user=user)

@app.route('/add-products')
@login_required
def add_products():
    sample_products = [
        {"name": "iPhone 16", "price": 799, "image": "iPhone16.png"},
        {"name": "AirPods Max", "price": 549, "image": "AirPods Max.png"},
        {"name": "iPad Pro", "price": 999, "image": "iPad Pro.png"},
        {"name": "Apple TV", "price": 129, "image": "Apple TV.png"},
        {"name": "Apple Watch Ultra", "price": 249, "image": "Apple Watch Ultra.png"},
        {"name": "Logitech Doorbell", "price": 199, "image": "Logitech Doorbell.png"}
    ]
    for p in sample_products:
        db.session.add(Product(**p))
    db.session.commit()
    return "✅ Sample products added!"

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.json.get('id')
    quantity = request.json.get('quantity', 1)
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += quantity
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'image': product.image
        })

    session['cart'] = cart
    session.modified = True
    return jsonify({'status': 'success', 'cart': cart})

@app.route('/cart')
@login_required
def cart():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        flash("Session expired. Please log in again.")
        return redirect(url_for('login'))

    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart-page.html', cart=cart_items, total=total_price, user=user)

@app.route('/update-cart', methods=['POST'])
@login_required
def update_cart_quantity():
    product_id = int(request.form['product_id'])
    action = request.form['action']
    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == product_id:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease' and item['quantity'] > 1:
                item['quantity'] -= 1
            break

    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = int(request.form['product_id'])
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    session['cart'] = []
    session.modified = True
    return jsonify({'status': 'success'})

@app.route('/clear-cart', methods=['POST'])
@login_required
def clear_cart():
    session['cart'] = []
    session.modified = True
    return jsonify({'status': 'success'})

@app.route('/contact')
@login_required
def contact():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        flash("Session expired. Please log in again.")
        return redirect(url_for('login'))

    return render_template('contact-page.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
    return render_template('login-page.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        admin_key = request.form.get('admin_key', '')

        if role == 'admin' and admin_key != 'admin':
            flash("Invalid admin access code.")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for('register'))
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

# ─── App Entry ───────────────────────────────────────────


@app.route('/update-product', methods=['POST'])
@login_required
def update_product():
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        flash("Unauthorized")
        return redirect(url_for('products'))

    product = Product.query.get(request.form['product_id'])
    product.name = request.form['name']
    product.price = float(request.form['price'])
    db.session.commit()
    return redirect(url_for('products'))


@app.route('/delete-product', methods=['POST'])
@login_required
def delete_product():
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        flash("Unauthorized")
        return redirect(url_for('products'))

    product = Product.query.get(request.form['product_id'])
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))


@app.route('/add-product', methods=['POST'])
@login_required
def add_product():
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        flash("Unauthorized")
        return redirect(url_for('products'))

    name = request.form['name']
    price = float(request.form['price'])
    file = request.files['image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_product = Product(name=name, price=price, image=filename)
        db.session.add(new_product)
        db.session.commit()
    else:
        flash("Invalid image file.")
    return redirect(url_for('products'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)

