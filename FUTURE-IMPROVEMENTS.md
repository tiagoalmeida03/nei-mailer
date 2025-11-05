# Future Improvements for nei-mailer

This document outlines the planned features, enhancements, and long-term goals for the `nei-mailer` project.

## 1. Rich Text Editor (WYSIWYG)

The current email composer is plain-text only. A high-priority goal is to implement a "What You See Is What You Get" (WYSIWYG) rich text editor to allow users to format their emails.

Key features for the editor will include:

### Basic Formatting
* **Bold** (`Ctrl+B`)
* *Italic* (`Ctrl+I`)
* <u>Underline</u> (`Ctrl+U`)
* ~~Strikethrough~~

### Text Styling
* Font size selection
* Font color and background color pickers

### Structure
* Bulleted lists
* Numbered lists
* Blockquotes (for replying)
* Headings (H1, H2, H3)

### Links
* Ability to insert, edit, and remove hyperlinks.

### Alignment
* Left, center, and right text alignment.

### Other
* Insert horizontal rule
* Clear formatting button

---

## 2. UI/UX Enhancements

To improve the overall user experience and make the application more intuitive and modern, a general UI/UX overhaul is planned.

* **Responsive Design:** Ensure the application is fully functional and visually appealing on all screen sizes, from mobile phones to widescreen desktops.
* **Modern Aesthetics:** Update the color palette, typography, button styles, and spacing to create a cleaner, more professional look.
* **Improved Navigation:** Redesign the sidebar/navigation menu to be more intuitive, clearly separating Inbox, Drafts, Sent, Spam, and user-created folders.
* **Feedback Mechanisms:**
    * Implement non-intrusive "toast" notifications for actions like "Email Sent," "Saved to Drafts," or "Error."
    * Add loading spinners/skeletons for when emails are being fetched or sent.
* **Drag-and-Drop:**
    * Allow users to drag and drop files directly into the compose window to add attachments.
    * (Future) Allow dragging emails into folders.
* **Accessibility (a11y):**
    * Improve color contrast to meet WCAG standards.
    * Ensure all interactive elements are keyboard-navigable.
    * Add proper ARIA labels and roles where needed.

---

## 3. Other Core Features

Beyond the editor and UI, the following features are critical for a competitive mail client:

* **Advanced Search:** Implement a robust search bar that can filter by sender, recipient, subject, and body content.
* **Email Signatures:** Allow users to create and manage multiple email signatures that can be automatically appended to new emails or replies.
* **Contact Management:** A simple address book to save, manage, and auto-complete contacts.
* **Folders/Labels:** A system for users to create custom folders or apply labels to organize their inbox.
* **Keyboard Shortcuts:** Implement common mail shortcuts (e.g., `R` to reply, `C` to compose, `Ctrl+Enter` to send).
