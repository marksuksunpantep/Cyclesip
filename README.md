# Cycle Sync Smoothies - Basic E-commerce Prototype

This is a simple Flask-based prototype for a cycle-based smoothie brand.

## Features
- Home page and product catalog
- Individual product detail pages
- Cart with quantity updates
- Mock checkout flow
- About and contact pages

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open the local Flask URL shown in your terminal.

## Notes
- Cart data is stored in the Flask session.
- Checkout is a mock flow only; there is no payment gateway.
- Product data is stored in-memory in `app.py` for simplicity.
