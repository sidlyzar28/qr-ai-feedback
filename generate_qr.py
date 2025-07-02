import qrcode

BASE_URL = "https://qr-ai-feedback.onrender.com"

def generate_qr(product_id):
    url = f"{BASE_URL}/feedback?product_id={product_id}"
    img = qrcode.make(url)
    img.save(f"static/qr_{product_id}.png")
    print(f"✅ QR generated for: {url}")

# Example usage:
generate_qr("p123")
