#!/usr/bin/env python3
"""
Batch generator helper - Generate voice demos in batches of 10
"""

import json
import subprocess
import sys

def load_industries():
    """Load industries from JSON file"""
    with open('industries.json', 'r') as f:
        return json.load(f)

def generate_batch(batch_number, batch_size=10):
    """Generate a specific batch of industries"""
    industries = load_industries()
    
    start_idx = (batch_number - 1) * batch_size
    end_idx = min(start_idx + batch_size, len(industries))
    
    if start_idx >= len(industries):
        print(f"❌ Batch {batch_number} is out of range. Total industries: {len(industries)}")
        return False
    
    batch_industries = industries[start_idx:end_idx]
    
    print(f"\n{'='*60}")
    print(f"BATCH {batch_number}: Industries {start_idx + 1} to {end_idx}")
    print(f"{'='*60}")
    for i, industry in enumerate(batch_industries, start=start_idx + 1):
        print(f"{i}. {industry}")
    print(f"{'='*60}\n")
    
    # Build command
    industries_str = ','.join(batch_industries)
    cmd = ['python3', 'generate_conversations.py', '--industries', industries_str]
    
    # Run generation
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 batch_generate.py <batch_number>")
        print("\nExamples:")
        print("  python3 batch_generate.py 1    # Generate batch 1 (industries 1-10)")
        print("  python3 batch_generate.py 2    # Generate batch 2 (industries 11-20)")
        print("  python3 batch_generate.py 9    # Generate batch 9 (industries 81-89)")
        print("\nTotal batches needed: 9 (89 industries / 10 per batch)")
        sys.exit(1)
    
    try:
        batch_number = int(sys.argv[1])
        if batch_number < 1:
            print("❌ Batch number must be 1 or greater")
            sys.exit(1)
        
        success = generate_batch(batch_number)
        
        if success:
            print(f"\n✅ Batch {batch_number} completed successfully!")
        else:
            print(f"\n❌ Batch {batch_number} failed")
            sys.exit(1)
            
    except ValueError:
        print("❌ Batch number must be an integer")
        sys.exit(1)

if __name__ == "__main__":
    main()
