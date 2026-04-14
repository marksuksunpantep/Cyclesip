from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
BRAND_NAME = "Cyclesip"
app.secret_key = 'dev-secret-key-change-me'


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    phase: str
    price: float
    short_desc: str
    description: str
    ingredients: list[str]
    image: str = 'images/default.png'


PRODUCTS: Dict[int, Product] = {
    1: Product(
        id=1,
        name='Blend 1',
        phase='Menstrual Phase',
        price=0.00,
        short_desc='Frozen strawberries, blueberries, spinach, and Greek yogurt.',
        description='Frozen strawberries: 150 g | Frozen blueberries: 60 g | Frozen spinach: 25 g | Frozen Greek yogurt: 25 g | Ground flaxseed: 5 g | Add when blending: orange juice | Optional honey',
        ingredients=[
            'Frozen strawberries: 150 g',
            'Frozen blueberries: 60 g',
            'Frozen spinach: 25 g',
            'Frozen Greek yogurt: 25 g',
            'Ground flaxseed: 5 g',
            'Add when blending: orange juice',
            'Optional honey',
        ],
        image='images/blend1.png',
    ),
    2: Product(
        id=2,
        name='Blend 2',
        phase='Follicular Phase',
        price=0.00,
        short_desc='Frozen mango, pineapple, banana, spinach, and chia seeds.',
        description='Frozen mango: 140 g | Frozen pineapple: 70 g | Frozen banana: 40 g | Frozen spinach: 25 g | Chia seeds: 5 g | Add when blending: almond milk',
        ingredients=[
            'Frozen mango: 140 g',
            'Frozen pineapple: 70 g',
            'Frozen banana: 40 g',
            'Frozen spinach: 25 g',
            'Chia seeds: 5 g',
            'Add when blending: almond milk',
        ],
        image='images/blend2.png',
    ),
    3: Product(
        id=3,
        name='Blend 3',
        phase='Ovulatory Phase',
        price=0.00,
        short_desc='Frozen avocado, banana, spinach, hemp seeds, and vanilla protein.',
        description='Frozen avocado: 70 g | Frozen banana: 100 g | Frozen spinach: 25 g | Hemp seeds: 10 g | Vanilla protein powder: 45 g | Cinnamon: 1 g | Add when blending: almond milk',
        ingredients=[
            'Frozen avocado: 70 g',
            'Frozen banana: 100 g',
            'Frozen spinach: 25 g',
            'Hemp seeds: 10 g',
            'Vanilla protein powder: 45 g',
            'Cinnamon: 1 g',
            'Add when blending: almond milk',
        ],
        image='images/blend3.png',
    ),
    4: Product(
        id=4,
        name='Blend 4',
        phase='Luteal Phase',
        price=0.00,
        short_desc='Frozen banana, oats, Greek yogurt, cacao, and protein powder.',
        description='Frozen banana: 110 g | Oats: 20 g | Frozen Greek yogurt: 25 g | Cacao powder: 10 g | Protein powder: 45 g | Cinnamon: 1 g | Add when blending: almond milk and almond butter',
        ingredients=[
            'Frozen banana: 110 g',
            'Oats: 20 g',
            'Frozen Greek yogurt: 25 g',
            'Cacao powder: 10 g',
            'Protein powder: 45 g',
            'Cinnamon: 1 g',
            'Add when blending: almond milk',
            'Add when blending: almond butter',
        ],
        image='images/blend4.png',
    ),
    5: Product(
        id=5,
        name='Cyclesip 10-Pack Subscription',
        phase='Monthly Subscription',
        price=90.00,
        short_desc='10 smoothies per month for flexible usage.',
        description='A monthly subscription including 10 smoothies aligned with your cycle. Ideal for lighter usage.',
        ingredients=['Menstrual Blend', 'Follicular Blend', 'Ovulatory Blend', 'Luteal Blend'],
    ),
    6: Product(
        id=6,
        name='Cyclesip 20-Pack Subscription',
        phase='Monthly Subscription',
        price=172.00,
        short_desc='20 smoothies per month aligned to your cycle.',
        description='A monthly subscription including 20 smoothies designed for each phase of the menstrual cycle. Best value for consistent users.',
        ingredients=['Menstrual Blend', 'Follicular Blend', 'Ovulatory Blend', 'Luteal Blend'],
    ),
    7: Product(
        id=7,
        name='Cyclesip Starter Box',
        phase='One-Time Purchase',
        price=20.00,
        short_desc='Try all blends before subscribing.',
        description='A one-time purchase starter kit including one packet of each blend so customers can sample before committing.',
        ingredients=['Menstrual Blend', 'Follicular Blend', 'Ovulatory Blend', 'Luteal Blend'],
    ),
}


def get_cart() -> Dict[str, int]:
    cart = session.get('cart')
    if not isinstance(cart, dict):
        cart = {}
        session['cart'] = cart
    return cart


def cart_details() -> tuple[list[dict], float]:
    items = []
    total = 0.0
    cart = get_cart()
    for product_id_str, qty in cart.items():
        try:
            product_id = int(product_id_str)
            quantity = int(qty)
        except (TypeError, ValueError):
            continue
        product = PRODUCTS.get(product_id)
        if not product or quantity <= 0:
            continue
        subtotal = product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
    return items, round(total, 2)


@app.context_processor
def inject_cart_count() -> dict:
    count = sum(int(v) for v in get_cart().values())
    return {'cart_count': count}


@app.route('/')
def home():
    featured = [PRODUCTS[i] for i in (1, 2, 3, 4)]
    return render_template('index.html', featured=featured)


@app.route('/products')
def products():
    shop_products = [PRODUCTS[i] for i in (5, 6, 7)]
    return render_template('products.html', products=shop_products)


@app.route('/products/<int:product_id>')
def product_detail(product_id: int):
    product = PRODUCTS.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    return render_template('product_detail.html', product=product)


@app.post('/add-to-cart/<int:product_id>')
def add_to_cart(product_id: int):
    product = PRODUCTS.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))

    quantity = request.form.get('quantity', '1')
    try:
        quantity_int = max(1, int(quantity))
    except ValueError:
        quantity_int = 1

    cart = get_cart()
    current_qty = int(cart.get(str(product_id), 0))
    cart[str(product_id)] = current_qty + quantity_int
    session['cart'] = cart
    flash(f'Added {product.name} to cart.', 'success')
    return redirect(request.referrer or url_for('products'))


@app.route('/cart')
def cart():
    items, total = cart_details()
    return render_template('cart.html', items=items, total=total)


@app.post('/update-cart')
def update_cart():
    cart = get_cart()
    for product_id_str in list(cart.keys()):
        field_name = f'qty_{product_id_str}'
        value = request.form.get(field_name, '0')
        try:
            qty = int(value)
        except ValueError:
            qty = 0
        if qty <= 0:
            cart.pop(product_id_str, None)
        else:
            cart[product_id_str] = qty
    session['cart'] = cart
    flash('Cart updated.', 'success')
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_details()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('products'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        if not all([name, email, address]):
            flash('Please fill in all checkout fields.', 'error')
            return render_template('checkout.html', items=items, total=total)

        session['last_order'] = {
            'name': name,
            'email': email,
            'address': address,
            'total': total,
            'item_count': sum(item['quantity'] for item in items),
        }
        session['cart'] = {}
        return redirect(url_for('thank_you'))

    return render_template('checkout.html', items=items, total=total)


@app.route('/thank-you')
def thank_you():
    order = session.get('last_order')
    if not order:
        return redirect(url_for('home'))
    return render_template('thank_you.html', order=order)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thanks! Your message has been received. This prototype does not send emails yet.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=False, port=5001)
