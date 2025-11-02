# Python Email Automation GUI

A simple desktop application built with Python and Tkinter that allows you to send mass personalized emails. It merges a list of contacts from a CSV file with a text/HTML template and sends them via any SMTP server (including Gmail).

## 📸 Screenshot

*(You should take a screenshot of your app and save it as `screenshot.png` in your repository for this image to display)*

![App Screenshot](screenshot.png)

## ✨ Features

* **Easy-to-Use GUI:** All options are on one screen.
* **SMTP Configuration:** Works with any SMTP provider (Host, Port, User, Pass).
* **Email Customization:** Set Subject, "From" Name, Reply-To, CC, and BCC.
* **CSV Variable Merging:** Reads a CSV file and personalizes each email (e.g., replaces `$NAME` with the name from the CSV).
* **HTML & Plain Text:** Converts your plain text template into an HTML email (with line breaks) and includes a plain text fallback.
* **Image Signature:** Embeds a `.png` or `.jpg` signature directly into the email body.
* **Multiple Attachments:** Add one or more file attachments to every email.
* **Send Throttling:** Set a custom delay (in seconds) between emails to avoid spam filters.
* **Safe & Asynchronous:** Sending is done in a separate thread so the app never freezes.
* **Real-time Controls:** Start, stop, and clear the log at any time.
* **Cross-Platform:** The script and the final app work on Windows, macOS, and Linux.

## 🗂️ File Requirements

To use the app, you need to prepare three files:

### 1. Variable Table (`.csv`)

This is your list of recipients and personalized data.

* **Format:** Must be a CSV file using a **semicolon (`;`)** as the delimiter.
* **Required Column:** You **must** have a column named `EMAIL`.
* **Variables:** Any other columns (e.g., `NAME`, `PRODUCT`, `INVOICE_ID`) will be available as variables in your template.

**Example (`contacts.csv`):**

```csv
EMAIL;NAME;PRODUCT
alice@example.com;Alice Smith;The Blue Widget
bob@example.com;Bob Johnson;The Red Widget
