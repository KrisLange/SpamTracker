import click
import imaplib
import email
from tabulate import tabulate
from email.utils import parseaddr
from collections import Counter
from datetime import datetime, timedelta

@click.command()
@click.option('--server', prompt='IMAP Server', help='IMAP server address')
@click.option('--port', prompt='IMAP Port', help='IMAP server port')
@click.option('--username', prompt='Username', help='Your email username')
@click.option('--password', prompt=True, hide_input=True, help='Your email password')
@click.option('--batch-size', default=100, help='Batch size for fetching emails')
def count_emails_by_domain(server, port, username, password, batch_size):
    click.echo(f"{port}")
    # Connect to IMAP server
    try:
        mail = imaplib.IMAP4_SSL(server, port=port)
        mail.login(username, password)
    except imaplib.IMAP4.error as e:
        click.echo(f"Failed to connect: {e}")
        return

    click.echo("Logged in!")
    # Select the inbox
    mail.select("inbox")

    # Calculate the date two months ago
    two_months_ago = (datetime.now() - timedelta(days=60)).strftime("%d-%b-%Y")

    # Search for emails from the last two months
    result, data = mail.search(None, f'(SINCE "{two_months_ago}")')

    if result == 'OK':
        email_domains = []
        message_numbers = data[0].split()

        # Fetch emails in batches
        for i in range(0, len(message_numbers), batch_size):
            batch = message_numbers[i:i+batch_size]
            str_batch = [str(int(x)) for x in batch]
            click.echo(f"fetching message [{i},{i+batch_size})")

            result, emails_data = mail.fetch(str(','.join(str_batch)), '(RFC822)')
            if result == 'OK':
                for email_data in emails_data:
                    if isinstance(email_data, tuple):
                        raw_email = email.message_from_bytes(email_data[1])
                        sender = parseaddr(raw_email['From'])[1]
                        domain = sender.split('@')[-1]
                        email_domains.append(domain)
                        click.echo(f"Email from {domain}")

        domain_counts = Counter(email_domains)

        # Sort domains by count in decreasing order
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)

        # Format the results as a table
        table_data = [(domain, count) for domain, count in sorted_domains]
        headers = ['Email Domain', 'Number of Emails']
        table = tabulate(table_data, headers=headers, tablefmt='grid')

        # Output the table
        click.echo(table)
    else:
        click.echo("Failed to search for emails.")

    mail.logout()

if __name__ == '__main__':
    count_emails_by_domain()
