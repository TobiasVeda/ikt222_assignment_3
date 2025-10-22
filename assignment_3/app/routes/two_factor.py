from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.db import get_db
from app.services import db_helper
import pyotp
import qrcode
import io
import base64

bp = Blueprint("two_factor", __name__)


# Enable 2FA - Generate QR Code
@bp.route("/enable-2fa", methods=["GET", "POST"])
def enable_2fa():
    """Generate and display QR code for 2FA setup"""

    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("password.login"))

    db = get_db()
    user = db_helper.get_user_form_id(db, session["user_id"])

    if request.method == "POST":
        # User confirmed they scanned the QR code
        verification_code = request.form.get("verification_code")
        totp_secret = session.get("temp_totp_secret")

        if not totp_secret or not verification_code:
            return render_template("enable_2fa.html",
                                   error="Please scan the QR code and enter the verification code")

        # Verify the code before enabling 2FA
        totp = pyotp.TOTP(totp_secret)
        if totp.verify(verification_code):
            # Save the secret to database
            db_helper.enable_2fa_for_user(db, session["user_id"], totp_secret)
            session.pop("temp_totp_secret", None)
            return redirect(url_for("main.dashboard"))
        else:
            return render_template("enable_2fa.html",
                                   error="Invalid verification code. Please try again.")

    # Generate a new TOTP secret
    totp_secret = pyotp.random_base32()
    session["temp_totp_secret"] = totp_secret

    # Create TOTP URI for QR code
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
        name=user["username"],
        issuer_name="Your App Name"
    )

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64 for HTML display
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    qr_code_base64 = base64.b64encode(buf.getvalue()).decode()

    return render_template("enable_2fa.html",
                           qr_code=qr_code_base64,
                           secret=totp_secret,
                           username=user["username"])


# Verify 2FA Code during login
@bp.route("/verify-2fa", methods=["GET", "POST"])
def verify_2fa():
    """Verify the 2FA code entered by user during login"""

    # Check if user needs 2FA verification
    if "pending_2fa_user_id" not in session:
        return redirect(url_for("password.login"))

    if request.method == "POST":
        verification_code = request.form.get("verification_code")
        user_id = session.get("pending_2fa_user_id")

        if not verification_code:
            return render_template("verify_2fa.html",
                                   error="Please enter a verification code")

        # Get user's TOTP secret from database
        db = get_db()
        user = db_helper.get_user_form_id(db, user_id)

        if not user or not user["totp_secret"]:
            session.pop("pending_2fa_user_id", None)
            return redirect(url_for("password.login"))

        # Verify the TOTP code
        totp = pyotp.TOTP(user["totp_secret"])
        if totp.verify(verification_code, valid_window=1):  # valid_window allows ±30 seconds
            # 2FA verification successful
            session["user_id"] = user_id
            session.pop("pending_2fa_user_id", None)
            return redirect(url_for("main.dashboard"))
        else:
            return render_template("verify_2fa.html",
                                   error="Invalid verification code. Please try again.")

    return render_template("verify_2fa.html")


# Disable 2FA
@bp.route("/disable-2fa", methods=["POST"])
def disable_2fa():
    """Disable 2FA for the current user"""

    if "user_id" not in session:
        return redirect(url_for("password.login"))

    db = get_db()
    db_helper.disable_2fa_for_user(db, session["user_id"])

    return redirect(url_for("main.dashboard"))