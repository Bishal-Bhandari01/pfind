# PFind - Parameter Finding Tool

A tool for discovering and validating URL parameters using waybackurls and gf-patterns.

## Requirements

- Python 3.x
- Go (for installing waybackurls and gf)
- Git

## Installation

1. **Install Required Python Packages**
```bash
pip install -r requirements.txt
```

2. **Install Go Tools**
```bash
# Install waybackurls
GO111MODULE=on go install github.com/tomnomnom/waybackurls@latest

# Install gf
GO111MODULE=on go install github.com/tomnomnom/gf@latest
```

3. **Setup gf-patterns**
```bash
# Create gf directory
mkdir -p ~/.gf

# Clone gf-patterns repository
git clone https://github.com/1ndianl33t/Gf-Patterns
mv Gf-Patterns/*.json ~/.gf/

# Additional patterns (optional)
git clone https://github.com/tomnomnom/gf
mv gf/examples/*.json ~/.gf/
```

4. **Add Go binary path to your shell**
```bash
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

## Usage

Basic usage:
```bash
python pfind.py -d example.com -t 10
```

Options:
- `-d, --domain`: Target domain
- `-t, --threads`: Number of threads (default: 10)
- `-o, --output`: Output file path

## Features

- Fetches URLs using waybackurls
- Analyzes URLs using gf-patterns
- Validates working parameters
- Saves results by pattern type
- Multi-threaded processing

## Output Structure

```
results/
├── xss.txt
├── sqli.txt
├── ssrf.txt
└── summary.json
```

## Common gf-patterns

- `xss`: Cross-site scripting parameters
- `sqli`: SQL injection parameters
- `ssrf`: Server-side request forgery parameters
- `rce`: Remote code execution parameters
- `redirect`: Open redirect parameters
- `lfi`: Local file inclusion parameters

## Example Commands

```bash
# Basic scan
python pfind.py -d example.com

# Scan with 20 threads and save output
python pfind.py -d example.com -t 20 -o results.txt

# Process existing URL list
cat urls.txt | python pfind.py
```

## Note

Make sure to respect the target website's terms of service and rate limits when using this tool.

## License

MIT License