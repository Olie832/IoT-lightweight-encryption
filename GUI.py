import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ascon import ascon_encrypt  # Assuming the encryption function is defined in encryption.py
import os
def encrypt_credentials_and_submit_form():
    username = username_entry.get()
    password = password_entry.get()

    # Encrypt the password
    nonce_hex, encrypted_password_hex = encrypt_password(password)

    # Open browser and submit the form
    open_browser_and_submit_form(username, encrypted_password_hex, nonce_hex)


def encrypt_password(password):
    # Fixed key value
    key = bytes.fromhex("39cd26d44bfb1e28a4906e9789d0e7aa")
    # Generate a new random nonce
    nonce = os.urandom(16)  # Assuming nonce size is 16 bytes

    # Encrypt the password
    encrypted_password = ascon_encrypt(key, nonce, b"", password.encode())
    
    # Return both nonce and encrypted password in hex format
    return nonce.hex(), encrypted_password.hex()
def open_browser_and_submit_form(username, encrypted_password_hex, nonce_hex):
    # Open Microsoft Edge browser
    browser = webdriver.Chrome()
    browser.get('http://192.168.0.221:8000')  # URL of the login page

    try:
        # Wait for the username field to be present
        username_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        # Fill in the username field
        username_field.send_keys(username)

        # Wait for the password field to be present
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        # Fill in the password field with the encrypted password
        password_field.send_keys(Keys.CONTROL + "a")
        password_field.send_keys(encrypted_password_hex)

        # Add a hidden field for nonce
        nonce_field = browser.execute_script(
            'var input = document.createElement("input"); input.type = "hidden"; input.name = "nonce"; input.value = arguments[0]; document.forms[0].appendChild(input);', 
            nonce_hex
        )

        # Submit the form
        password_field.submit()

        # Wait for an element that indicates successful login
        success_element = WebDriverWait(browser, 300).until(
            EC.presence_of_element_located((By.ID, "success_message"))
        )
        # If the element is found, the login was successful
        print("Login successful!")
    except:
        # If the element is not found, the login failed
        print("Login failed! Please close this window and try again :)")


# Create the main window
root = tk.Tk()
root.title("Login App")

# Create widgets
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")
login_button = tk.Button(root, text="Login", command=encrypt_credentials_and_submit_form)
result_label = tk.Label(root, text="")

# Place widgets on the grid
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry.grid(row=0, column=1, padx=10, pady=5)
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry.grid(row=1, column=1, padx=10, pady=5)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Run the application
root.mainloop()
