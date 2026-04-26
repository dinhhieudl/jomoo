#!/usr/bin/env python3
"""Convert .fid images to .jpg at 80% quality, then update README references."""

import os
from pathlib import Path
from PIL import Image
import re

PRODUCTS_DIR = Path("/root/.openclaw/workspace/jomoo-products/products")
QUALITY = 80
converted = 0
failed = 0
total_size_before = 0
total_size_after = 0

def convert_fid_to_jpg(fid_path):
    global converted, failed, total_size_before, total_size_after
    jpg_path = fid_path.with_suffix(".jpg")
    
    try:
        size_before = fid_path.stat().st_size
        total_size_before += size_before
        
        with Image.open(fid_path) as img:
            # Convert to RGB if needed (e.g. RGBA, P mode)
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            
            img.save(jpg_path, "JPEG", quality=QUALITY, optimize=True)
        
        size_after = jpg_path.stat().st_size
        total_size_after += size_after
        
        # Remove original .fid file
        fid_path.unlink()
        converted += 1
        
    except Exception as e:
        print(f"  FAIL: {fid_path.name} - {e}")
        failed += 1


def update_readme_refs(readme_path):
    """Update image references in README from .fid to .jpg"""
    if not readme_path.exists():
        return
    
    content = readme_path.read_text(encoding="utf-8")
    # Replace .fid with .jpg in image references
    updated = content.replace(".fid)", ".jpg)")
    if updated != content:
        readme_path.write_text(updated, encoding="utf-8")


def main():
    print(f"Converting .fid → .jpg (quality={QUALITY}%)")
    print(f"Directory: {PRODUCTS_DIR}\n")
    
    # Find all .fid files
    fid_files = sorted(PRODUCTS_DIR.rglob("*.fid"))
    print(f"Found {len(fid_files)} .fid files\n")
    
    # Convert all
    for i, fid in enumerate(fid_files):
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(fid_files)}")
        convert_fid_to_jpg(fid)
    
    print(f"\nConversion done:")
    print(f"  Converted: {converted}")
    print(f"  Failed: {failed}")
    print(f"  Size before: {total_size_before / 1024 / 1024:.1f} MB")
    print(f"  Size after:  {total_size_after / 1024 / 1024:.1f} MB")
    print(f"  Saved: {(total_size_before - total_size_after) / 1024 / 1024:.1f} MB ({(1 - total_size_after/total_size_before)*100:.0f}% reduction)")
    
    # Update all README files
    print("\nUpdating README references...")
    for readme in PRODUCTS_DIR.rglob("README.md"):
        update_readme_refs(readme)
    
    # Update product_data.json files
    print("Updating JSON references...")
    for json_file in PRODUCTS_DIR.rglob("product_data.json"):
        content = json_file.read_text(encoding="utf-8")
        updated = content.replace('.fid"', '.jpg"').replace(".fid'", ".jpg'")
        if updated != content:
            json_file.write_text(updated, encoding="utf-8")
    
    print("\nAll done!")


if __name__ == "__main__":
    main()
