#!/usr/bin/env python3
"""
iCloud Email Cleanup Script
Deletes emails dated before January 1, 2025 from specified folders

Requirements:
- Python 3.6+
- iCloud app-specific password (not your regular iCloud password)

How to generate an app-specific password:
1. Go to appleid.apple.com
2. Sign in with your Apple ID
3. In the Security section, click "Generate Password" under App-Specific Passwords
4. Name it something like "Email Cleanup Script"
5. Copy the generated password (format: xxxx-xxxx-xxxx-xxxx)
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import sys
import getpass

# Configuration
IMAP_SERVER = "imap.mail.me.com"
IMAP_PORT = 993
EMAIL_ADDRESS = "rileygcolley@icloud.com"
CUTOFF_DATE = datetime(2025, 1, 1)

# Folders to clean (iCloud uses different folder names)
FOLDERS_TO_CLEAN = [
    "INBOX",
    "Junk",
    "Deleted Messages"  # This is iCloud's trash folder
]

def connect_to_icloud(email_address, password):
    """Connect to iCloud IMAP server"""
    print(f"Connecting to {IMAP_SERVER}...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_address, password)
        print("✓ Successfully connected to iCloud Mail")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"✗ Login failed: {e}")
        print("\nMake sure you're using an app-specific password, not your regular iCloud password!")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Connection error: {e}")
        sys.exit(1)

def list_folders(mail):
    """List all available folders (for debugging)"""
    status, folders = mail.list()
    if status == 'OK':
        print("\nAvailable folders:")
        for folder in folders:
            print(f"  {folder.decode()}")

def delete_old_emails(mail, folder_name, cutoff_date, dry_run=True):
    """Delete emails older than cutoff_date from specified folder"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing folder: {folder_name}")

    try:
        # Select the folder
        status, messages = mail.select(f'"{folder_name}"')
        if status != 'OK':
            print(f"✗ Could not select folder '{folder_name}'")
            return 0

        total_messages = int(messages[0].decode())
        print(f"  Total messages in folder: {total_messages}")

        # Search for messages before cutoff date
        # IMAP date format: DD-Mon-YYYY
        date_string = cutoff_date.strftime("%d-%b-%Y")
        status, message_ids = mail.search(None, f'BEFORE {date_string}')

        if status != 'OK':
            print(f"✗ Search failed in folder '{folder_name}'")
            return 0

        message_id_list = message_ids[0].split()
        count = len(message_id_list)

        print(f"  Found {count} emails before {cutoff_date.strftime('%Y-%m-%d')}")

        if count == 0:
            return 0

        if dry_run:
            print(f"  [DRY RUN] Would delete {count} emails")
            return count

        # Delete emails in batches
        batch_size = 1000
        deleted = 0

        for i in range(0, len(message_id_list), batch_size):
            batch = message_id_list[i:i + batch_size]
            batch_str = b','.join(batch).decode()

            # Mark for deletion
            mail.store(batch_str, '+FLAGS', '\\Deleted')
            deleted += len(batch)

            print(f"  Marked {deleted}/{count} emails for deletion...", end='\r')

        # Permanently delete marked emails
        mail.expunge()
        print(f"\n  ✓ Deleted {deleted} emails from {folder_name}")

        return deleted

    except Exception as e:
        print(f"✗ Error processing folder '{folder_name}': {e}")
        return 0

def main():
    print("=" * 60)
    print("iCloud Email Cleanup Script")
    print("=" * 60)
    print(f"Email: {EMAIL_ADDRESS}")
    print(f"Deleting emails before: {CUTOFF_DATE.strftime('%Y-%m-%d')}")
    print(f"Folders: {', '.join(FOLDERS_TO_CLEAN)}")
    print("=" * 60)

    # Get app-specific password
    print("\nEnter your iCloud app-specific password:")
    print("(If you don't have one, visit: https://appleid.apple.com)")
    password = getpass.getpass("Password: ")

    if not password:
        print("✗ No password provided")
        sys.exit(1)

    # Connect to iCloud
    mail = connect_to_icloud(EMAIL_ADDRESS, password)

    # Optional: List all folders to verify folder names
    # Uncomment the next line if you want to see all available folders
    # list_folders(mail)

    # First, do a dry run
    print("\n" + "=" * 60)
    print("STEP 1: DRY RUN (No emails will be deleted)")
    print("=" * 60)

    total_to_delete = 0
    for folder in FOLDERS_TO_CLEAN:
        count = delete_old_emails(mail, folder, CUTOFF_DATE, dry_run=True)
        total_to_delete += count

    print("\n" + "=" * 60)
    print(f"DRY RUN COMPLETE: Found {total_to_delete} emails to delete")
    print("=" * 60)

    if total_to_delete == 0:
        print("\nNo emails to delete. Exiting.")
        mail.logout()
        return

    # Ask for confirmation
    print("\n⚠️  WARNING: This will PERMANENTLY delete these emails!")
    print("This action CANNOT be undone.")
    response = input("\nType 'DELETE' to proceed or anything else to cancel: ")

    if response.strip().upper() != 'DELETE':
        print("\n✓ Cancelled. No emails were deleted.")
        mail.logout()
        return

    # Actually delete emails
    print("\n" + "=" * 60)
    print("STEP 2: DELETING EMAILS")
    print("=" * 60)

    total_deleted = 0
    for folder in FOLDERS_TO_CLEAN:
        count = delete_old_emails(mail, folder, CUTOFF_DATE, dry_run=False)
        total_deleted += count

    print("\n" + "=" * 60)
    print(f"✓ COMPLETE: Deleted {total_deleted} emails total")
    print("=" * 60)

    # Logout
    mail.logout()
    print("\n✓ Disconnected from iCloud Mail")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user")
        sys.exit(0)
