# 🔍 PatternFinder (Pfind)

**PatternFinder (Pfind)** is a lightweight, multi-threaded URL scanning tool that checks URLs against custom regex patterns (stored in JSON format). It validates URLs, matches them against patterns, saves organized outputs per pattern, and generates a complete JSON report.

---

## 🚀 Features

- ✅ Scans and validates URLs from a file
- 📂 Loads reusable regex patterns from `~/.gf/` (in JSON format)
- 🔎 Identifies matches per pattern
- 🧠 Saves matched URLs into organized `.txt` files (per pattern)
- 🗃️ Outputs a detailed `JSON` scan report
- ⚡ Multi-threaded for faster scanning
- 🎨 Colored terminal output using `colorama`

---

## 📁 Directory Structure

```text
.
├── pfind.py                    # Main script
├── pattern_matches/           # (Auto-created) Stores matched URLs by pattern
├── pattern_scan_results_*.json # JSON reports from scans
└── ~/.gf/                     # Folder containing your pattern JSON files
```

---

## 🛠️ Requirements

- Python 3.7+
- Install dependencies:
```bash
pip install colorama
```

---

## 📦 Pattern Format
All pattern files must be stored in ~/.gf/ and follow this format:

```json
{
  "patterns": [
    "admin\\.php",
    "login\\?user=.*",
    "wp-json.*"
  ]
}
```
Each file should be named like admin_panels.json, wordpress.json, etc.

---

## 📑 Usage
1. Prepare your input file:
A plain text file with one URL per line.

```text
https://example.com/login?user=admin
http://site.org/wp-json/
https://test.com/admin.php
```
2. Run the script:
```bash
python3 pfind.py urls.txt
```
3. Output:
Matched URLs saved under `pattern_matches/<pattern_name>.txt`

Full scan report: `pattern_scan_results_<timestamp>.json`

Console summary with colorized output

---

## 📊 Output Example
JSON Report Excerpt:

```json
{
  "metadata": {
    "scan_time": "2025-06-04T13:25:01.123",
    "total_urls": 20,
    "valid_urls": 18,
    "patterns_loaded": 5
  },
  "summary": {
    "total_matches": 9,
    "patterns_matched": {
      "login": 3,
      "admin": 2
    }
  }
}
```
---

## 🧠 How It Works
 - Loads regex patterns from JSON files in `~/.gf/`
 - Validates URLs (structure, scheme)
 - Uses multi-threading (`ThreadPoolExecutor`) to scan faster
 - Matches URLs to all loaded patterns
 - Saves results in structured `.txt` and `.json` files

---

## 🔒 Disclaimer
This tool is intended for educational and legitimate security testing purposes only. Unauthorized scanning of systems you don’t own is illegal.

---

## 🧑‍💻 Author
Built with ❤️ by `Bishal Bhandari`
Feel free to contribute or fork!

Let me know if you want me to include example pattern files (`.json`), CLI flags, or Docker usage instructions in the README.
