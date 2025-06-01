# Slotify Backup CLI

A simple command-line tool to **export and import database backups** for the [Slotify](https://slotify.pythonanywhere.com) app using its token-protected API.

Developed by **[Indrajit Ghosh](https://indrajitghosh.onrender.com/)**, this script is useful for scheduled backups and restoration.

---

## 🌟 Features

- ✅ Export Slotify database as a ZIP file using the `/api/export` endpoint
- ✅ Import a ZIP file to the Slotify database via `/api/import` (Currently disabled)
- ✅ Supports custom API base URL, token file path, and output directory
- ✅ Automatically timestamps export files
- ✅ Suitable for automated backups using cron

---

## 🔧 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
````

---

## 🔐 Authentication

This tool uses a Bearer token for authentication.
Save your API token in a file named `.slotify_api_token` in the project root or use `--token-file` to specify a custom file.

Example token file:

```
abc123...your_token_here...
```

---

## 🚀 Usage

### Export Data

```bash
python main.py export
```

With options:

```bash
python main.py export \
    --base-url https://slotify.pythonanywhere.com
    --output-dir ./backups \ # (Optional)
    --token-file ~/.my_token \ # (Optional)
    
```

### Import Data

```bash
python main.py import --zip-file ~/Downloads/slotify_export.zip
```

With options:

```bash
python main.py import \
    --base-url https://slotify.pythonanywhere.com
    --zip-file ~/Downloads/slotify_export.zip \
    --token-file .slotify_api_token # (Optional)
```

---

## 📅 Cron Job for Daily Backup

To automatically export every day at 2:00 AM, run:

```bash
crontab -e
```

Add this line (adjust path as needed):

```bash
# Everyday at 11 AM
0 11 * * * cd /path/to/SlotifyBackups && /path/to/SlotifyBackups/env/bin/python /path/to/SlotifyBackups/main.py export --base-url https://slotify.pythonanywhere.com >> /path/to/SlotifyBackups/cron.log 2>&1
```

> Ensure your `.slotify_api_token` exists in the same directory or provide `--token-file`.

---

## 📁 Project Structure

```
SlotifyBackups/
├── main.py                  # Main CLI script
├── .slotify_api_token       # Token file (ignored by Git)
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignores token and backups
├── README.md                # This file
```

---

## 🙋 Author

**Indrajit Ghosh**
PhD Scholar, ISI Bangalore
[Website](https://indrajitghosh.onrender.com/) • [GitHub](https://github.com/indrajit912)
