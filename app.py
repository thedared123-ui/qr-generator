from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_img = None
    url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            
            # Convertir a base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_img = base64.b64encode(buffer.getvalue()).decode("ascii")
            
    return render_template("index.html", qr_img=qr_img, url=url)

if __name__ == "__main__":
    app.run(debug=True)
