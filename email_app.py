import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import smtplib
import ssl
import csv
import os
import time
import threading
import ssl
import certifi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from string import Template
from queue import Queue
from email.utils import formataddr

# --- Core Application Class ---

class EmailApp(tk.Tk):
    """
    Main application class for the email automation tool.
    """
    
    def __init__(self):
        super().__init__()
        
        # --- App Setup ---
        self.title("Email Automation System")
        self.geometry("800x800")
        
        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # --- State Variables ---
        self.sending_thread = None
        self.stop_event = threading.Event()
        self.log_queue = Queue()

        # --- File Path Storage ---
        self.template_file_path = tk.StringVar()
        self.variable_file_path = tk.StringVar()
        self.signature_file_path = tk.StringVar()

        # --- Build UI ---
        self.create_widgets()
        
        # Start queue monitor
        self.after(100, self.check_log_queue)

    def create_widgets(self):
        """Creates and lays out all the GUI widgets."""
        
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SMTP Configuration ---
        smtp_frame = ttk.LabelFrame(main_frame, text="SMTP Configuration", padding="10")
        smtp_frame.pack(fill=tk.X, expand=True)
        smtp_frame.columnconfigure(1, weight=1)
        smtp_frame.columnconfigure(3, weight=1)

        # Left Column
        ttk.Label(smtp_frame, text="SMTP HOST:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.smtp_host = ttk.Entry(smtp_frame)
        self.smtp_host.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        self.smtp_host.insert(0, "smtp.gmail.com")

        ttk.Label(smtp_frame, text="SMTP USERNAME:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.smtp_user = ttk.Entry(smtp_frame)
        self.smtp_user.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        ttk.Label(smtp_frame, text="SMTP DELAY (s):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.smtp_delay = ttk.Spinbox(smtp_frame, from_=0, to=300, increment=1)
        self.smtp_delay.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.smtp_delay.set(5) # Default 5 seconds

        # Right Column
        ttk.Label(smtp_frame, text="SMTP PORT:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.smtp_port = ttk.Entry(smtp_frame, width=10)
        self.smtp_port.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.smtp_port.insert(0, "587")

        ttk.Label(smtp_frame, text="SMTP PASSWORD:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.smtp_pass = ttk.Entry(smtp_frame, show="*")
        self.smtp_pass.grid(row=1, column=3, sticky="we", padx=5, pady=5)

        # --- Email Details ---
        email_frame = ttk.LabelFrame(main_frame, text="Email Details", padding="10")
        email_frame.pack(fill=tk.X, expand=True, pady=10)
        email_frame.columnconfigure(1, weight=1)

        ttk.Label(email_frame, text="SUBJECT:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.email_subject = ttk.Entry(email_frame)
        self.email_subject.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        ttk.Label(email_frame, text="FROM:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.email_from_name = ttk.Entry(email_frame)
        self.email_from_name.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        ttk.Label(email_frame, text="REPLY-TO:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.email_reply_to = ttk.Entry(email_frame)
        self.email_reply_to.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        ttk.Label(email_frame, text="CC:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.email_cc = ttk.Entry(email_frame)
        self.email_cc.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        ttk.Label(email_frame, text="BCC:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.email_bcc = ttk.Entry(email_frame)
        self.email_bcc.grid(row=4, column=1, sticky="we", padx=5, pady=5)

        # --- File Selection ---
        files_frame = ttk.LabelFrame(main_frame, text="Files and Attachments", padding="10")
        files_frame.pack(fill=tk.X, expand=True, pady=10)
        files_frame.columnconfigure(1, weight=1)

        # Body Template
        ttk.Button(files_frame, text="Select Body Template File (.txt)", command=self.select_template_file).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.template_label = ttk.Label(files_frame, textvariable=self.template_file_path, relief="sunken", padding=(5,2))
        self.template_label.grid(row=0, column=1, sticky="we", padx=5, pady=5)

        # Variable Table
        ttk.Button(files_frame, text="Select Variable Table File (.csv)", command=self.select_csv_file).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.variable_label = ttk.Label(files_frame, textvariable=self.variable_file_path, relief="sunken", padding=(5,2))
        self.variable_label.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Signature File
        ttk.Button(files_frame, text="Select Signature File (.png/.jpg)", command=self.select_signature_file).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.signature_label = ttk.Label(files_frame, textvariable=self.signature_file_path, relief="sunken", padding=(5,2))
        self.signature_label.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        # Attachment UI
        attachment_ui_frame = ttk.Frame(files_frame)
        attachment_ui_frame.grid(row=3, column=0, columnspan=2, sticky="we", padx=5, pady=5)
        attachment_ui_frame.columnconfigure(1, weight=1)

        ttk.Label(attachment_ui_frame, text="Attachments:").grid(row=0, column=0, sticky="nw", pady=5)

        # Listbox with Scrollbar
        listbox_frame = ttk.Frame(attachment_ui_frame)
        listbox_frame.grid(row=0, column=1, sticky="we", padx=5)
        listbox_frame.columnconfigure(0, weight=1)
        
        att_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.attachment_listbox = tk.Listbox(listbox_frame, height=4, selectmode=tk.SINGLE, yscrollcommand=att_scrollbar.set)
        att_scrollbar.config(command=self.attachment_listbox.yview)
        
        att_scrollbar.grid(row=0, column=1, sticky="ns")
        self.attachment_listbox.grid(row=0, column=0, sticky="we")

        # +/- Buttons
        attachment_button_frame = ttk.Frame(attachment_ui_frame)
        attachment_button_frame.grid(row=0, column=2, sticky="ns", pady=5)

        self.add_attachment_button = ttk.Button(attachment_button_frame, text="+", width=3, command=self.add_attachment)
        self.add_attachment_button.pack(side=tk.TOP, pady=(0, 2))
        
        self.remove_attachment_button = ttk.Button(attachment_button_frame, text="-", width=3, command=self.remove_attachment)
        self.remove_attachment_button.pack(side=tk.TOP, pady=2)


        # --- Controls and Log ---
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        
        # Controls
        control_bar = ttk.Frame(log_frame)
        control_bar.grid(row=0, column=0, sticky="w")
        
        self.start_button = ttk.Button(control_bar, text="▶ Start", command=self.start_sending_thread)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_bar, text="■ Stop", command=self.stop_sending, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(control_bar, text="🗑 Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Log Output
        self.log_text = tk.Text(log_frame, height=15, state=tk.DISABLED, wrap=tk.WORD, borderwidth=1, relief="solid")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=1, column=0, sticky="nsew", pady=5)
        scrollbar.grid(row=1, column=1, sticky="ns")

    # --- File/Directory Dialog Functions ---

    def select_template_file(self):
        path = filedialog.askopenfilename(title="Select Template File", filetypes=[("Text Files", "*.txt")])
        if path:
            self.template_file_path.set(path)

    def select_csv_file(self):
        path = filedialog.askopenfilename(title="Select Variable Table", filetypes=[("CSV Files", "*.csv")])
        if path:
            self.variable_file_path.set(path)
            
    def select_signature_file(self):
        path = filedialog.askopenfilename(title="Select Signature Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.signature_file_path.set(path)

    # --- Attachment Functions ---
    def add_attachment(self):
        """Opens dialog to select one or more attachments and adds them to the list."""
        paths = filedialog.askopenfilenames(title="Select Attachment(s)")
        if paths:
            current_attachments = self.attachment_listbox.get(0, tk.END)
            for path in paths:
                if path not in current_attachments:
                    self.attachment_listbox.insert(tk.END, path)

    def remove_attachment(self):
        """Removes the selected attachment from the list."""
        try:
            selected_indices = self.attachment_listbox.curselection()
            if not selected_indices:
                raise IndexError
            # Remove from bottom to top to avoid index shifting
            for index in reversed(selected_indices):
                self.attachment_listbox.delete(index)
        except IndexError:
            messagebox.showwarning("No Selection", "Please select an attachment to remove.")

    # --- Logging Functions ---

    def log(self, message):
        """Puts a message into the thread-safe queue to be logged."""
        self.log_queue.put(message)

    def check_log_queue(self):
        """Checks the log queue and updates the GUI text box."""
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.see(tk.END)
        self.after(100, self.check_log_queue) # Poll every 100ms

    def clear_log(self):
        """Clears the log text box."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    # --- Core Email Sending Logic ---

    def start_sending_thread(self):
        """Starts the email sending process in a new thread."""
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.clear_log()
        self.log("Starting email process...")

        # Create and start the thread
        self.sending_thread = threading.Thread(
            target=self.send_mail_logic,
            daemon=True
        )
        self.sending_thread.start()

    def stop_sending(self):
        """Signals the sending thread to stop."""
        self.log("Stopping... Please wait for the current email to finish.")
        self.stop_event.set()
        self.stop_button.config(state=tk.DISABLED)

    def sending_cleanup(self, final_message):
        """Resets the UI after sending is complete or stopped."""
        self.log(final_message)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def send_mail_logic(self):
        """
        The main logic for sending emails. This runs in a separate thread.
        """
        try:
            # 1. Get all data from GUI
            host = self.smtp_host.get()
            port_str = self.smtp_port.get()
            user_email = self.smtp_user.get() # This is the "from" email
            password = self.smtp_pass.get()
            delay_str = self.smtp_delay.get()
            
            subject = self.email_subject.get()
            from_display_name = self.email_from_name.get() # This is the "from" name
            reply_to_addr = self.email_reply_to.get() or user_email
            
            # Get GLOBAL CC/BCC lists from GUI
            cc_list = [email.strip() for email in self.email_cc.get().split(',') if email.strip()]
            bcc_list = [email.strip() for email in self.email_bcc.get().split(',') if email.strip()]
            
            template_path = self.template_file_path.get()
            csv_path = self.variable_file_path.get()
            sig_path = self.signature_file_path.get()
            
            # Get attachments from listbox
            attachment_files = self.attachment_listbox.get(0, tk.END) 

            # 2. Validation
            if not all([host, port_str, user_email, password, from_display_name, template_path, csv_path, sig_path]):
                raise ValueError("Missing required fields: Host, Port, User, Pass, From, Template, CSV, or Signature.")
            
            try:
                port = int(port_str)
            except ValueError:
                raise ValueError("Port must be a number.")
                
            try:
                delay = int(delay_str)
            except ValueError:
                raise ValueError("Delay must be a number.")

            # 3. Read Template
            self.log(f"Reading template from: {template_path}")
            try:
                # First, try to read as UTF-8
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, log it and retry with latin-1 (which handles cp1252)
                self.log("UTF-8 decoding failed for template. Retrying with 'latin-1'...")
                with open(template_path, 'r', encoding='latin-1') as f:
                    template_content = f.read()
            
            # Convert text newlines to HTML line breaks
            template_content = template_content.replace('\n', '<br>')
            
            # 4. Prepare Signature
            self.log(f"Reading signature from: {sig_path}")
            with open(sig_path, 'rb') as f:
                signature_data = f.read()
            
            # Replace placeholder with HTML img tag, setting max-width
            template_content = template_content.replace(
                "${SIGNATURE}", 
                f'<img src="cid:signature_image" style="max-width: 400px; height: auto;">'
            )
            
            email_template = Template(template_content)

            # 5. Get Attachments (Already done from listbox)
            self.log(f"Found {len(attachment_files)} attachment(s) from list.")
            
            # 6. Read CSV
            self.log(f"Reading variable table: {csv_path}")
            try:
                # First, try 'utf-8-sig' (handles BOM from Excel)
                with open(csv_path, 'r', encoding='utf-8-sig') as f: 
                    reader = list(csv.DictReader(f, delimiter=';'))
            except UnicodeDecodeError:
                # If UTF-8 fails, log it and retry with latin-1
                self.log("UTF-8-SIG decoding failed for CSV. Retrying with 'latin-1'...")
                with open(csv_path, 'r', encoding='latin-1') as f: 
                    reader = list(csv.DictReader(f, delimiter=';'))
            
            if not reader:
                raise ValueError("CSV file is empty or formatted incorrectly.")
            
            # Get header names, converting to uppercase for case-insensitive matching
            headers = [h.upper() for h in reader[0].keys()]
            if 'EMAIL' not in headers:
                raise ValueError("CSV file must contain an 'EMAIL' column.")
            
            # Find the exact (case-sensitive) column names from the first row
            # This allows users to have 'email' or 'Email' instead of just 'EMAIL'
            email_col = next(h for h in reader[0].keys() if h.upper() == 'EMAIL')
            cc_col = next((h for h in reader[0].keys() if h.upper() == 'CC'), None)
            bcc_col = next((h for h in reader[0].keys() if h.upper() == 'BCC'), None)
            
            if cc_col:
                self.log(f"Found 'CC' column in CSV: {cc_col}")
            if bcc_col:
                self.log(f"Found 'BCC' column in CSV: {bcc_col}")
            
            self.log(f"Found {len(reader)} recipients in CSV.")

            # 7. Connect to SMTP Server
            self.log(f"Connecting to {host}:{port}...")
            context = ssl.create_default_context(cafile=certifi.where())
            with smtplib.SMTP(host, port) as server:
                server.starttls(context=context)
                server.login(user_email, password)
                self.log("Successfully logged in.")

                # 8. Loop and Send
                for i, row in enumerate(reader, 1):
                    if self.stop_event.is_set():
                        self.log("Stop signal received. Terminating process.")
                        break
                    
                    recipient_email = row.get(email_col, '').strip()
                    if not recipient_email:
                        self.log(f"Skipping row {i}: No email address found in '{email_col}' column.")
                        continue
                        
                    self.log(f"--- Processing email {i}/{len(reader)} to {recipient_email} ---")
                    
                    try:
                        # Create the email
                        msg = MIMEMultipart('related')
                        msg['Subject'] = subject
                        msg['From'] = formataddr((from_display_name, user_email))
                        msg['To'] = recipient_email
                        msg['Reply-To'] = reply_to_addr
                        
                        # --- MODIFICATION: Handle dynamic CC/BCC from CSV ---
            
                        # Start with global lists (defined before the loop)
                        current_cc_list = list(cc_list) 
                        current_bcc_list = list(bcc_list)
                        
                        # Check for a 'CC' column in the CSV and add emails
                        if cc_col and row.get(cc_col, '').strip():
                            csv_cc_emails = [email.strip() for email in row[cc_col].split(',') if email.strip()]
                            if csv_cc_emails:
                                self.log(f"Adding CSV CCs: {', '.join(csv_cc_emails)}")
                                current_cc_list.extend(csv_cc_emails)
                        
                        # Check for a 'BCC' column in the CSV and add emails
                        if bcc_col and row.get(bcc_col, '').strip():
                            csv_bcc_emails = [email.strip() for email in row[bcc_col].split(',') if email.strip()]
                            if csv_bcc_emails:
                                self.log(f"Adding CSV BCCs: {', '.join(csv_bcc_emails)}")
                                current_bcc_list.extend(csv_bcc_emails)
                        
                        # De-duplicate and set headers
                        if current_cc_list:
                            unique_cc = sorted(list(set(current_cc_list)))
                            msg['Cc'] = ", ".join(unique_cc)
                        if current_bcc_list:
                            unique_bcc = sorted(list(set(current_bcc_list)))
                            msg['Bcc'] = ", ".join(unique_bcc)
                        
                        # Create the final recipient list for sendmail (must be de-duplicated)
                        all_recipients = list(set([recipient_email] + current_cc_list + current_bcc_list))
                        
                        # --- END MODIFICATION ---

                        # Personalize and attach body
                        safe_row = {k: row.get(k, f'${{{k}}}') for k in row}
                        body_html = email_template.substitute(safe_row)
                        
                        # Create 'alternative' part for HTML and plain text
                        alt_part = MIMEMultipart('alternative')
                        
                        # Must match the string in the template replacement above
                        plain_text = body_html.replace('<br>', '\n').replace(f'<img src="cid:signature_image" style="max-width: 400px; height: auto;">', '')
                        
                        alt_part.attach(MIMEText(plain_text, 'plain', 'utf-8'))
                        alt_part.attach(MIMEText(body_html, 'html', 'utf-8'))
                        
                        msg.attach(alt_part)
                        
                        # Embed signature
                        sig_image = MIMEImage(signature_data, name=os.path.basename(sig_path))
                        sig_image.add_header('Content-ID', '<signature_image>')
                        sig_image.add_header('Content-Disposition', 'inline', filename=os.path.basename(sig_path))
                        msg.attach(sig_image)

                        # Add attachments
                        for filepath in attachment_files:
                            filename = os.path.basename(filepath)
                            with open(filepath, 'rb') as f_attach:
                                # Add name=filename to constructor
                                part = MIMEBase('application', 'octet-stream', name=filename)
                                part.set_payload(f_attach.read())
                            
                            encoders.encode_base64(part)
                            
                            # Use keyword argument for filename for better MIME compatibility
                            part.add_header('Content-Disposition', 'attachment', filename=filename)
                            
                            msg.attach(part)
                        
                        # Send the email
                        # Use the raw user_email as the "from" address for sendmail
                        server.sendmail(user_email, all_recipients, msg.as_string())
                        self.log(f"Successfully sent email to {recipient_email}")

                    except Exception as e:
                        self.log(f"ERROR sending to {recipient_email}: {e}")
                    
                    if self.stop_event.is_set():
                        self.log("Stop signal received. Terminating process.")
                        break
                    
                    if i < len(reader) and not self.stop_event.is_set():
                        self.log(f"Waiting for {delay} second(s) delay...")
                        time.sleep(delay)

                self.log("--- Email sending loop finished. ---")
            
            # 9. Finished
            self.after(0, self.sending_cleanup, "Process completed successfully.")

        except Exception as e:
            # Handle setup errors (file not found, login fail, etc.)
            self.log(f"FATAL ERROR: {e}")
            self.after(0, self.sending_cleanup, "Process failed. Check logs.")

# --- Run the Application ---

if __name__ == "__main__":
    app = EmailApp()
    
    # Simple check for required GUI elements
    try:
        app.mainloop()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        print("This script requires a graphical environment to run.")