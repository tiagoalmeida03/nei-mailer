# Email Automation System

A Python-based desktop application for sending personalized bulk emails with attachments, signatures, and variable substitution from CSV data.

## Features

- **SMTP Configuration**: Support for any SMTP server (Gmail, Outlook, custom servers)
- **Personalized Emails**: Use template variables to personalize each email
- **HTML Email Support**: Send rich HTML emails with embedded images
- **Signature Embedding**: Automatically embed image signatures in emails
- **Multiple Attachments**: Add multiple files to be sent with each email
- **CC/BCC Support**: Send copies to multiple recipients
- **Delay Control**: Set custom delays between emails to avoid rate limiting
- **Thread-Safe Operation**: Non-blocking UI with background email sending
- **Real-time Logging**: Monitor the sending process with detailed logs
- **Stop/Resume Control**: Ability to stop the sending process at any time

## Requirements

### Python Version
- Python 3.6 or higher

### Dependencies
All dependencies are part of Python's standard library:
- `tkinter` - GUI framework
- `smtplib` - SMTP protocol client
- `ssl` - SSL/TLS support
- `csv` - CSV file handling
- `email` - Email message construction
- `threading` - Multi-threading support

## Installation

1. **Clone or download** the script to your local machine

2. **Ensure Python is installed**:
   ```bash
   python --version
   ```

3. **No additional packages needed** - all dependencies are built-in

4. **Run the application**:
   ```bash
   python email_automation.py
   ```

## Setup and Configuration

### 1. SMTP Configuration

Configure your email server settings:

| Field | Description | Example |
|-------|-------------|---------|
| **SMTP HOST** | Your email provider's SMTP server | `smtp.gmail.com` |
| **SMTP PORT** | Port number (usually 587 for TLS) | `587` |
| **SMTP USERNAME** | Your email address | `your-email@gmail.com` |
| **SMTP PASSWORD** | App password or account password | `your-app-password` |
| **SMTP DELAY** | Delay between emails in seconds | `5` |

#### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate an App Password: [Google Account Settings](https://myaccount.google.com/apppasswords)
3. Use the 16-character app password in the SMTP PASSWORD field

#### Outlook Setup
- **Host**: `smtp-mail.outlook.com` or `smtp.office365.com`
- **Port**: `587`
- Use your regular Outlook password

### 2. Email Details

| Field | Description | Required |
|-------|-------------|----------|
| **SUBJECT** | Email subject line | Yes |
| **FROM** | Display name for sender | Yes |
| **REPLY-TO** | Reply-to email address | Optional |
| **CC** | Carbon copy recipients (comma-separated) | Optional |
| **BCC** | Blind carbon copy recipients (comma-separated) | Optional |

### 3. File Setup

#### Body Template File (.txt)
Create a plain text file with HTML formatting and variable placeholders:

```html
Hello ${NAME},

Thank you for your interest in ${PRODUCT}. We are excited to work with you!

Your account ID is: ${ACCOUNT_ID}

Best regards,
${SIGNATURE}
```

**Variable Format**: Use `${VARIABLE_NAME}` for substitution

#### Variable Table File (.csv)
Create a CSV file with semicolon (`;`) delimiters:

```csv
EMAIL;NAME;PRODUCT;ACCOUNT_ID
john@example.com;John Smith;Premium Plan;ACC-001
jane@example.com;Jane Doe;Basic Plan;ACC-002
```

**Requirements**:
- Must contain an `EMAIL` column
- Use semicolon (`;`) as delimiter
- First row is header with column names
- UTF-8 encoding recommended

#### Signature File (.png/.jpg)
- Image file containing your email signature
- Recommended max width: 400px
- Supported formats: PNG, JPG, JPEG
- Will be embedded inline in the email

### 4. Attachments

- Click **"+"** button to add files
- Click **"-"** button to remove selected file
- Multiple attachments supported
- Files are sent with every email

## Usage

1. **Configure SMTP Settings**
   - Enter your email server details
   - Set an appropriate delay (recommended: 5-10 seconds for Gmail)

2. **Fill Email Details**
   - Add subject, from name, and optional CC/BCC

3. **Select Required Files**
   - Body template (.txt)
   - Variable table (.csv)
   - Signature image (.png/.jpg)

4. **Add Attachments** (optional)
   - Click "+" to add files
   - Click "-" to remove files

5. **Start Sending**
   - Click **"▶ Start"** button
   - Monitor progress in the log window
   - Click **"■ Stop"** to halt the process if needed

6. **Review Logs**
   - Check for successful sends and errors
   - Use **"🗑 Clear Log"** to clear the log window

## Template Variables

### Using Variables in Templates

Variables in your template file are replaced with values from the CSV file:

**Template**:
```
Dear ${FIRST_NAME} ${LAST_NAME},

Your order #${ORDER_ID} has been confirmed.
```

**CSV**:
```csv
EMAIL;FIRST_NAME;LAST_NAME;ORDER_ID
customer@example.com;John;Doe;12345
```

**Result**:
```
Dear John Doe,

Your order #12345 has been confirmed.
```

### Special Variable: SIGNATURE

The `${SIGNATURE}` placeholder in your template is automatically replaced with your embedded signature image.

## Troubleshooting

### Common Issues

#### Authentication Failed
- **Gmail**: Use App Password, not regular password
- **Outlook**: Enable less secure apps or use app password
- Verify username and password are correct

#### Connection Timeout
- Check SMTP host and port
- Verify firewall/antivirus isn't blocking
- Try port 465 (SSL) instead of 587 (TLS)

#### CSV Not Loading
- Ensure semicolon (`;`) is used as delimiter
- Check file encoding (UTF-8 recommended)
- Verify `EMAIL` column exists in header

#### Images Not Displaying
- Ensure signature file path is correct
- Use supported formats (PNG, JPG, JPEG)
- Check image file isn't corrupted

#### Rate Limiting / Blocked
- Increase delay between emails
- Gmail limit: ~500 emails/day for personal accounts
- Consider using dedicated SMTP service for bulk sending

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Missing required fields" | Empty configuration fields | Fill all required SMTP and file fields |
| "Port must be a number" | Invalid port format | Enter numeric port (e.g., 587) |
| "CSV file is empty" | CSV file has no data | Add data rows to CSV file |
| "Must contain EMAIL column" | EMAIL column missing | Add EMAIL column to CSV header |
| "Authentication failed" | Wrong credentials | Verify username/password, use app password |

## Security Best Practices

1. **Never commit passwords** to version control
2. **Use App Passwords** instead of account passwords
3. **Limit CSV file access** - contains recipient data
4. **Test with small batches** before full sends
5. **Review all recipients** in CSV before sending
6. **Keep logs** for audit purposes
7. **Use encrypted connections** (TLS/SSL)

## Rate Limiting Guidelines

| Provider | Daily Limit | Recommended Delay |
|----------|-------------|-------------------|
| Gmail (Free) | ~500 emails | 5-10 seconds |
| Gmail (Workspace) | ~2,000 emails | 3-5 seconds |
| Outlook (Free) | ~300 emails | 10-15 seconds |
| Custom SMTP | Varies | Check provider docs |

## Advanced Configuration

### HTML Email Formatting

Your template supports HTML tags:

```html
<h1>Welcome ${NAME}!</h1>
<p>Thank you for joining <strong>${COMPANY}</strong>.</p>
<ul>
  <li>Benefit 1</li>
  <li>Benefit 2</li>
</ul>

${SIGNATURE}
```

### Multiple CC/BCC Recipients

Separate multiple recipients with commas:
```
CC: manager@company.com, admin@company.com
BCC: archive@company.com, backup@company.com
```

## Limitations

- **Single-file application**: No external configuration files
- **No draft mode**: Emails are sent immediately
- **No scheduling**: Must be run manually
- **No analytics**: No open/click tracking
- **Memory storage**: No persistent history beyond current session

## License

This is free and unencumbered software released into the public domain.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the log window
3. Verify all file formats and requirements
4. Test with a small sample before bulk sending

## Changelog

### Version 1.0
- Initial release
- SMTP configuration support
- CSV variable substitution
- Image signature embedding
- Multiple attachments
- CC/BCC support
- Thread-safe operation
- Real-time logging

---

**⚠️ Important**: Always test with a small batch of test emails before sending to your full recipient list. Review all configurations and test thoroughly to avoid sending errors to your entire mailing list.
