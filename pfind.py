#!/usr/bin/env python3

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Set, Any
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
from urllib.parse import urlparse, urljoin
import datetime

# Initialize colorama for colored output
init()

class PatternFinder:
    def __init__(self):
        self.patterns_dir = os.path.expanduser('~/.gf')
        self.patterns: Dict[str, List[str]] = {}
        self.load_patterns()
        self.results = {
            "metadata": {
                "scan_time": "",
                "total_urls": 0,
                "valid_urls": 0,
                "patterns_loaded": len(self.patterns)
            },
            "results": [],
            "summary": {
                "total_matches": 0,
                "patterns_matched": {}
            }
        }
        self.output_dir = "pattern_matches"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_patterns(self) -> None:
        """Load all JSON pattern files from ~/.gf directory"""
        if not os.path.exists(self.patterns_dir):
            print(f"Error: Patterns directory not found at {self.patterns_dir}")
            sys.exit(1)

        for pattern_file in Path(self.patterns_dir).glob('*.json'):
            try:
                with open(pattern_file) as f:
                    data = json.load(f)
                    pattern_name = pattern_file.stem
                    patterns = data.get('patterns', [])
                    self.patterns[pattern_name] = [
                        re.compile(p, re.IGNORECASE) 
                        for p in patterns
                    ]
                print(f"Loaded {len(patterns)} patterns from {pattern_name}")
            except Exception as e:
                print(f"Error loading {pattern_file}: {e}")

    def validate_url(self, url: str) -> Dict[str, Any]:
        """Validate URL structure and accessibility"""
        try:
            parsed = urlparse(url)
            validation = {
                "url": url,
                "is_valid": False,
                "scheme": parsed.scheme,
                "netloc": parsed.netloc,
                "path": parsed.path,
                "params": parsed.params,
                "query": parsed.query,
                "errors": []
            }
            
            # Basic URL structure validation
            if not parsed.scheme or not parsed.netloc:
                validation["errors"].append("Invalid URL structure")
                return validation
                
            if parsed.scheme not in ['http', 'https']:
                validation["errors"].append("Invalid scheme (must be http or https)")
                return validation
            
            validation["is_valid"] = True
            return validation
            
        except Exception as e:
            return {
                "url": url,
                "is_valid": False,
                "errors": [str(e)]
            }

    def scan_url(self, url: str) -> Dict[str, Any]:
        """Scan and validate a single URL"""
        validation = self.validate_url(url)
        matches: Dict[str, Set[str]] = {}
        
        if validation["is_valid"]:
            for pattern_name, pattern_list in self.patterns.items():
                for pattern in pattern_list:
                    if pattern.search(url):
                        if pattern_name not in matches:
                            matches[pattern_name] = set()
                        matches[pattern_name].add(url)
        
        return {
            "url": url,
            "validation": validation,
            "matches": {k: list(v) for k, v in matches.items()}
        }

    def save_pattern_matches(self, scan_results: List[Dict[str, Any]]) -> None:
        """Save URLs to their respective pattern files"""
        pattern_files: Dict[str, set] = {}

        # Collect URLs for each pattern
        for result in scan_results:
            if result["validation"]["is_valid"]:
                for pattern, matches in result["matches"].items():
                    if pattern not in pattern_files:
                        pattern_files[pattern] = set()
                    pattern_files[pattern].update(matches)

        # Save URLs to pattern-specific files
        for pattern, urls in pattern_files.items():
            output_file = os.path.join(self.output_dir, f"{pattern}.txt")
            with open(output_file, 'w') as f:
                for url in sorted(urls):
                    f.write(f"{url}\n")
            print(f"{Fore.GREEN}Saved {len(urls)} URLs to {output_file}{Style.RESET_ALL}")

    def scan_file(self, file_path: str) -> None:
        """Scan URLs from a file and generate reports"""
        try:
            with open(file_path) as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return

        self.results["metadata"]["scan_time"] = datetime.datetime.now().isoformat()
        self.results["metadata"]["total_urls"] = len(urls)

        # Use ThreadPoolExecutor for parallel scanning
        with ThreadPoolExecutor(max_workers=10) as executor:
            scan_results = list(executor.map(self.scan_url, urls))

        # Save pattern-specific matches
        self.save_pattern_matches(scan_results)

        # Process results for summary
        valid_urls = 0
        total_matches = 0
        pattern_matches = {}

        for result in scan_results:
            if result["validation"]["is_valid"]:
                valid_urls += 1
                for pattern, matches in result["matches"].items():
                    total_matches += len(matches)
                    pattern_matches[pattern] = pattern_matches.get(pattern, 0) + len(matches)

        # Update results
        self.results["results"] = scan_results
        self.results["metadata"]["valid_urls"] = valid_urls
        self.results["summary"]["total_matches"] = total_matches
        self.results["summary"]["patterns_matched"] = pattern_matches

        # Save JSON report
        output_file = f"pattern_scan_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Fore.GREEN}JSON results saved to: {output_file}{Style.RESET_ALL}")
        self.print_summary()

    def print_summary(self) -> None:
        """Print scan summary"""
        print(f"\n{Fore.CYAN}Scan Summary:{Style.RESET_ALL}")
        print(f"Total URLs: {self.results['metadata']['total_urls']}")
        print(f"Valid URLs: {self.results['metadata']['valid_urls']}")
        print(f"Total Matches: {self.results['summary']['total_matches']}")
        print("\nPattern Matches:")
        for pattern, count in self.results['summary']['patterns_matched'].items():
            print(f"  - {pattern}: {count}")

def main():
    if len(sys.argv) != 2:
        print("Usage: pfind.py <url_file>")
        sys.exit(1)

    finder = PatternFinder()
    finder.scan_file(sys.argv[1])

if __name__ == "__main__":
    main()