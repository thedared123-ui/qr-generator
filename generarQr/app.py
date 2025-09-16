from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Página principal (menú)
@app.route("/")
def index():
    return render_template("index.html")  # menú con links a qr clásico y con logo


# --- QR clásico ---
@app.route("/qr", methods=["GET", "POST"])
def qr_classic():
    qr_img = None
    url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5,
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_img = base64.b64encode(buffer.getvalue()).decode("ascii")

    return render_template("qr.html", qr_img=qr_img, url=url)


# --- QR con logo ---
@app.route("/logo", methods=["GET", "POST"])
def qr_with_logo():
    qr_img = None
    url = None
    if request.method == "POST":
        url = request.form.get("url")
        file = request.files.get("logo")

        if url:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5,
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )
            qr.add_data(url)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

            if file and file.filename != "":
                try:
                    logo = Image.open(file.stream)
                    qr_width, qr_height = img_qr.size
                    logo_size = qr_width // 4
                    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

                    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                    img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
                except Exception as e:
                    print("Error cargando logo:", e)

            buffer = BytesIO()
            img_qr.save(buffer, format="PNG")
            qr_img = base64.b64encode(buffer.getvalue()).decode("ascii")

    return render_template("logo.html", qr_img=qr_img, url=url)


if __name__ == "__main__":
    app.run(debug=True)
