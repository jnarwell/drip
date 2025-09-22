#!/usr/bin/env python3
"""
Check if GitHub Pages has the latest deployment
"""

import requests
import re
import sys
from datetime import datetime

def check_deployment():
    """Check if the deployed site matches local build"""
    
    # URLs to check
    urls = [
        "https://jnarwell.github.io/drip/",
        "https://jnarwell.github.io/drip/system/levels/"
    ]
    
    print("Checking GitHub Pages deployment status...\n")
    
    for url in urls:
        print(f"Checking: {url}")
        
        try:
            # Get the page content
            response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            content = response.text
            
            # Extract build version if present
            build_match = re.search(r'Build: v(\d+)', content)
            if build_match:
                build_version = build_match.group(1)
                build_time = datetime.fromtimestamp(int(build_version))
                print(f"  ✓ Build version: {build_version} ({build_time})")
            else:
                print("  ⚠ No build version found")
            
            # Extract costs
            cost_match = re.findall(r'~\$([0-9,]+)', content)
            if cost_match:
                print(f"  ✓ Found costs: {', '.join(cost_match[:4])}")
                
                # Check if they're the expected automated values
                expected = ["13,988", "21,681", "38,187", "79,732"]
                if cost_match[:4] == expected:
                    print("  ✅ Costs match automated values!")
                else:
                    print(f"  ❌ Costs don't match expected: {expected}")
            
            # Extract last updated time
            updated_match = re.search(r'Last updated: ([\d-]+ [\d:]+)', content)
            if updated_match:
                print(f"  ✓ Last updated: {updated_match.group(1)}")
                
        except Exception as e:
            print(f"  ❌ Error checking {url}: {e}")
        
        print()

if __name__ == "__main__":
    check_deployment()