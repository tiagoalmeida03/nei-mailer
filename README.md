Python Email Automation GUI
A simple desktop application built with Python and Tkinter that allows you to send mass personalized emails. It merges a list of contacts from a CSV file with a text/HTML template and sends them via any SMTP server (including Gmail).

📸 Screenshot
(You should take a screenshot of your app and save it as screenshot.png in your repository for this image to display)

✨ Features
Easy-to-Use GUI: All options are on one screen.

SMTP Configuration: Works with any SMTP provider (Host, Port, User, Pass).

Email Customization: Set Subject, "From" Name, Reply-To, CC, and BCC.

CSV Variable Merging: Reads a CSV file and personalizes each email (e.g., replaces $NAME with the name from the CSV).

HTML & Plain Text: Converts your plain text template into an HTML email (with line breaks) and includes a plain text fallback.

Image Signature: Embeds a .png or .jpg signature directly into the email body.

Multiple Attachments: Add one or more file attachments to every email.

Send Throttling: Set a custom delay (in seconds) between emails to avoid spam filters.

Safe & Asynchronous: Sending is done in a separate thread so the app never freezes.

Real-time Controls: Start, stop, and clear the log at any time.

Cross-Platform: The script and the final app work on Windows, macOS, and Linux.

🗂️ File Requirements
To use the app, you need to prepare three files:

1. Variable Table (.csv)

This is your list of recipients and personalized data.

Format: Must be a CSV file using a semicolon (;) as the delimiter.

Required Column: You must have a column named EMAIL.

Variables: Any other columns (e.g., NAME, PRODUCT, INVOICE_ID) will be available as variables in your template.

Example (contacts.csv):

Fragmento do código
EMAIL;NAME;PRODUCT
alice@example.com;Alice Smith;The Blue Widget
bob@example.com;Bob Johnson;The Red Widget
2. Body Template (.txt)

This is the text of your email.

Format: A simple .txt file.

Variables: Use $VARIABLE_NAME to insert data from your CSV. The variable name must match the column header in your CSV exactly (e.g., $NAME, $PRODUCT).

Signature: Include the special variable ${SIGNATURE} exactly where you want your signature image to appear.

Example (template.txt):

Plaintext
Hi $NAME,

Thank you for your recent purchase of $PRODUCT. We appreciate your business.

Please let us know if you have any questions.

Best,

${SIGNATURE}
3. Signature File (.png or .jpg)

Your company or personal signature as an image file. This will be embedded (not attached) at the ${SIGNATURE} location.

🚀 How to Use the App
Run the application (either the .exe, .app, or from the Python script).

SMTP Configuration:

Host: smtp.gmail.com (for Gmail) or your provider's host.

Port: 587 (for TLS)

Username: Your full email address (you@gmail.com).

Password: Your email password.

⚠️ Important Gmail/Google Note: If you use Gmail with 2-Factor Authentication, you must generate an "App Password" and use that here. Your regular password will not work. Learn how to create an App Password here.

Email Details:

Subject: The subject line for your email.

From: The name you want recipients to see (e.g., "The Support Team").

Reply-To: (Optional) If you want replies to go to a different address.

CC / BCC: (Optional) Add comma-separated emails to CC or BCC on every message.

Files and Attachments:

Click the buttons to select your .txt Body Template, .csv Variable Table, and .png/.jpg Signature File.

Click the + button to add one or more file attachments (like a PDF).

Start Sending:

Click "▶ Start".

Watch the log window for progress.

Click "■ Stop" to safely stop the process after the current email is finished.

📦 How to Create the App (For Developers)
You can package this script into a standalone executable (.exe, .app, or binary) so it can be run on any computer without installing Python.

We will use PyInstaller for this.

1. Preparation

First, install PyInstaller in your terminal:

Bash
pip install pyinstaller
2. Building the Executable

The most important rule is: You must build the app on the target operating system.

To make the Windows .exe, run the command on Windows.

To make the macOS .app, run the command on macOS.

To make the Linux executable, run the command on Linux.

Save the script as email_app.py and run the correct command from your terminal in the same directory.

🖥️ For Windows

Bash
pyinstaller --onefile --windowed --name="Email Automator" email_app.py
Optional (Add an Icon): If you have an .ico file:

Bash
pyinstaller --onefile --windowed --name="Email Automator" --icon="path/to/your/icon.ico" email_app.py
🍎 For macOS

Bash
pyinstaller --onefile --windowed --name="Email Automator" email_app.py
Optional (Add an Icon): If you have an .icns file:

Bash
pyinstaller --onefile --windowed --name="Email Automator" --icon="path/to/your/icon.icns" email_app.py
🐧 For Linux

Bash
pyinstaller --onefile --windowed --name="Email Automator" email_app.py
3. Get Your App

After the command finishes, look inside the new dist/ folder. Your standalone application (Email Automator.exe, Email Automator.app, or Email Automator) will be in there!

Note for macOS Users: When you try to run the .app on another Mac, you may get a security warning. To fix this, the user must right-click the app and select "Open" from the menu.

🐍 How to Run from Source
This script uses only Python's built-in libraries. No external packages are required.

Make sure you have Python 3 installed.

Clone this repository.

Run the script from your terminal:

Bash
python email_app.py
⚖️ License
This project is licensed under the MIT License.
