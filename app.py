from flask import Flask, request, render_template
import qrcode
import io
import base64

# Note: We removed webbrowser, Timer, and os imports because cloud servers don't use them!

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_data = None
    user_url = ""

    if request.method == "POST":
        user_url = request.form.get("url")
        if user_url:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(user_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#333333", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            qr_code_data = f"data:image/png;base64,{img_base64}"

    return render_template("index.html", qr_code=qr_code_data, url=user_url)

# Vercel handles the server running, so we just need this basic block
if __name__ == "__main__":
    app.run()