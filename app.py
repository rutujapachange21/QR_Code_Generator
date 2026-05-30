import io
import base64
import qrcode
from flask import Flask, render_template, request

app = Flask(__name__)

# Home route for local testing and Vercel deployment
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect the data submitted by the user from the form
        title = request.form.get('title')
        description = request.form.get('description')
        social_link = request.form.get('social_link')

        # Configure the QR code design parameters
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Embed the social link, or default to the user's name/title if no link is provided
        qr_data = social_link if social_link else f"Portfolio of {title}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Generate a Dark Purple (#180029) QR code to match the Jewel Monarch Sunrise theme
        img = qr.make_image(fill_color="#180029", back_color="white")

        # Convert the image directly in memory to avoid file-saving errors on Vercel Serverless
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        qr_code_uri = f"data:image/png;base64,{qr_base64}"

        # Pass all collected data and the generated QR image back to the template to activate 'Landing Profile Mode'
        return render_template(
            'index.html',
            title=title,
            description=description,
            social_link=social_link,
            qr_code=qr_code_uri
        )

    # If it is a GET request (initial page load), render the empty dashboard screen
    return render_template('index.html')

# For local testing (when running on your own PC)
if __name__ == '__main__':
    app.run(debug=True)
