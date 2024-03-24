# Count Emails by Domain

This script connects to an IMAP server, retrieves emails from the last two months, and displays the frequency of each email domain.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Kris/SpamTracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SpamTracker
   ```

3. Install the dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python src/email_frequencies.py --server imap.google.com --username foo@gmail.com
```

## Sample Output

Running the script might produce output similar to the following:

```
Email Domain    Number of Emails
--------------------------------
example.com     25
gmail.com       15
yahoo.com       10
```

## Author

Kris Lange
kris@krislange.com