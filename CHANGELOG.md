# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]

### Added

* **Dynamic CSV Recipients:** The application now automatically scans for and reads `CC` and `BCC` columns from the input `.csv` file.
* **Per-Row Customization:** Allows for unique CC and BCC recipients to be specified for each individual email (row) in the CSV.
* **Multiple Recipient Support:** You can now add multiple email addresses to a single `CC` or `BCC` cell by separating them with a comma (`,`).
* **Smart Combining:** Recipients found in the CSV file are automatically *added* to any "global" CC or BCC recipients already entered in the app's GUI.

## [1.0.0]

### Added

* Initial release
* SMTP configuration support
* CSV variable substitution
* Image signature embedding
* Multiple attachments
* CC/BCC support
* Thread-safe operation
* Real-time logging
