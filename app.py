from flask import Flask, request, render_template
from ascon import ascon_decrypt
import requests
import RPi.GPIO as GPIO


app = Flask(__name__)

KEY = bytes.fromhex("39cd26d44bfb1e28a4906e9789d0e7aa")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    form_data = request.form.to_dict()

    if 'password' in form_data and 'nonce' in form_data:
        encrypted_password_hex = form_data['password']
        nonce_hex = form_data['nonce']
        
        encrypted_password = bytes.fromhex(encrypted_password_hex)
        nonce = bytes.fromhex(nonce_hex)

        decrypted_password = ascon_decrypt(KEY, nonce, b"", encrypted_password)

        expected_password = "admin"
        if decrypted_password.decode() == expected_password:
            if 'username' in form_data and form_data['username'] == 'admin':
                return render_template('led.html')
            else:
                return "Invalid username. Please close this window and try again :)"
        else:
            return "Invalid password. Please close this window and try again :)"
    else:
        return "Password or nonce not found in form data"

@app.route('/led')
def led_control():
    return render_template('led.html')

@app.route('/led/on', methods=['POST'])
#def led_on():
    GPIO.output(led_pin, GPIO.HIGH)
    return 'LED turned on'

@app.route('/led/off', methods=['POST'])
#def led_off():
    GPIO.output(led_pin, GPIO.LOW)
    return 'LED turned off'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
