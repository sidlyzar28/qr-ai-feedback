import qrcode

def generate_qr(product_id):
    data = f"http://localhost:5000/feedback?product_id={product_id}"
    img = qrcode.make(data)
    img.save(f"static/qr_{product_id}.png")

generate_qr("p123")
