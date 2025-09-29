#!/usr/bin/env python3
"""
Slotify API Client Script

This script allows users to interact with Slotify's token-protected export and import API endpoints.

Author: Indrajit Ghosh
Created On: Jun 03, 2025

Features:
- Reads the API token from a file (default: .slotify_api_token)
- Downloads exported JSON file from the /api/v1/export endpoint
- Uploads JSON file to the /api/v1/import endpoint
- Deletes the temporary file after upload
- Supports custom token file, output directory, and base URL

Authentication:
This client uses a Bearer token for API authentication.
You must save your token in a file (default: .slotify_api_token), or use --token-file to specify a custom path.

Usage:
- python slotify_client.py export --base-url https://slotify.pythonanywhere.com
- python slotify_client.py import --base-url https://slotify.pythonanywhere.com --json-file ./backups/slotify_export_20250601_113656.json
"""

import argparse
import requests
import logging
from pathlib import Path
from datetime import datetime, timezone

# Logging setup
LOG_FILE = Path.cwd() / "slotify_backups.log"
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%b %d, %Y %I:%M:%S %p'
)

# Defaults
DEFAULT_BASE_URL = 'http://localhost:8080'
DEFAULT_TOKEN_PATH = Path.cwd() / '.slotify_api_token'
DEFAULT_DOWNLOAD_DIR = Path.cwd() / 'backups'

def load_token(token_path=DEFAULT_TOKEN_PATH):
    path = Path(token_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Token file not found: {path}")
    token = path.read_text().strip()
    if not token:
        raise ValueError("Token file is empty.")
    return token

def export_data(token, base_url, download_dir=DEFAULT_DOWNLOAD_DIR):
    logging.info("Initiating export...")
    headers = {'Authorization': f'Bearer {token}'}
    export_endpoint = f'{base_url.rstrip("/")}/api/v1/export?as_file=true'

    # Log and print the GET request
    logging.info(f"GET {export_endpoint}")
    print(f"GET {export_endpoint}")

    response = requests.get(export_endpoint, headers=headers)

    if response.status_code != 200:
        logging.error(f"Export failed: {response.status_code} - {response.text}")
        raise Exception(f"Export failed: {response.status_code} - {response.text}")

    download_dir = Path(download_dir).expanduser()
    download_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%b_%d_%Y_%I_%M_%S_%p').lower()
    filename = f'slotify_export_{timestamp}.json'
    file_path = download_dir / filename

    with open(file_path, 'wb') as f:
        f.write(response.content)

    logging.info(f"Exported data saved to: {file_path}")
    return file_path

def import_data(base_url, json_file_path):
    """
    This function imports data into Slotify from a specified JSON file.
    Args:
        base_url (str): The base URL of the Slotify API.
        json_file_path (str): The path to the JSON file to be imported.
    Returns:
        str: Success message from the API response.
    Raises:
        FileNotFoundError: If the specified JSON file does not exist.
        Exception: If the import request fails.
    
    Usage:
        import_data('http://localhost:8080', './backups/slotify_export_jan_01_2024_12_00_00_pm.json')
    
    Note: To use this function, ensure that the Slotify instance is running and accessible. And firt 
    ensure that the database is empty and initialized. For this do the following:
        1. Stop the Slotify server if it's running.
        2. Delete the existing database file (e.g., slotify.db).
        3. Now use the command: `flask db upgrade` to initialize a new database.
        4. Start the Slotify server again.
    After completing these steps, you can safely use the import_data function to import your data.
    """
    file_path = Path(json_file_path).expanduser()
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    logging.info(f"Initiating import with file: {file_path}")
    
    import_endpoint = f'{base_url.rstrip("/")}/api/v1/import'

    # Log and print the POST request
    logging.info(f"POST {import_endpoint}")
    print(f"POST {import_endpoint}")

    with open(file_path, 'rb') as f:
        files = {'file': (file_path.name, f, 'application/json')}
        response = requests.post(import_endpoint, files=files)

    if response.status_code != 200:
        logging.error(f"Import failed: {response.status_code} - {response.text}")
        print("\n[!] Import failed. Ensure the database is empty and initialized.\n")
        raise Exception(f"Import failed: {response.status_code} - {response.text}")

    logging.info("Import successful.")
    return response.json().get('message')

def main():
    parser = argparse.ArgumentParser(description="Slotify API client to export or import data.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data from Slotify')
    export_parser.add_argument('--base-url', required=True, help='Base URL of the Slotify API')
    export_parser.add_argument('--token-file', default=DEFAULT_TOKEN_PATH, help='Path to token file')
    export_parser.add_argument('--download-dir', default=DEFAULT_DOWNLOAD_DIR, help='Directory to save export')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import data into Slotify')
    import_parser.add_argument('--base-url', required=True, help='Base URL of the Slotify API')
    import_parser.add_argument('--token-file', default=DEFAULT_TOKEN_PATH, help='Path to token file')
    import_parser.add_argument('--json-file', required=True, help='Path to exported JSON file')

    args = parser.parse_args()
    token = load_token(args.token_file)

    if args.command == 'export':
        path = export_data(token, args.base_url, args.download_dir)
        print(f"\n[✔] Export successful. File saved to: {path}\n")
    elif args.command == 'import':
        message = import_data(args.base_url, args.json_file)
        print(f"\n[✔] Import successful: {message}\n")

if __name__ == '__main__':
    main()