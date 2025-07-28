#!/usr/bin/env python3
"""
Script to fix pandas_ta numpy import error.
This patches the problematic squeeze_pro.py file to use the correct numpy import.
"""

import os
import site
import glob

def find_pandas_ta_squeeze_pro():
    """Find the pandas_ta squeeze_pro.py file that needs patching."""
    # Get site-packages directory
    site_packages = site.getsitepackages()[0]
    squeeze_pro_path = os.path.join(site_packages, 'pandas_ta', 'momentum', 'squeeze_pro.py')
    
    if os.path.exists(squeeze_pro_path):
        return squeeze_pro_path
    
    # Try alternative locations
    for path in site.getsitepackages():
        squeeze_pro_path = os.path.join(path, 'pandas_ta', 'momentum', 'squeeze_pro.py')
        if os.path.exists(squeeze_pro_path):
            return squeeze_pro_path
    
    return None

def patch_squeeze_pro_file(file_path):
    """Patch the squeeze_pro.py file to fix the numpy import."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the problematic import exists
        if 'from numpy import NaN as npNaN' in content:
            print(f"Found problematic import in {file_path}")
            
            # Replace the problematic import
            new_content = content.replace(
                'from numpy import NaN as npNaN',
                'from numpy import nan as npNaN'
            )
            
            # Write the patched content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Successfully patched {file_path}")
            return True
        else:
            print(f"✅ No problematic import found in {file_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error patching {file_path}: {e}")
        return False

def main():
    """Main function to fix the pandas_ta import issue."""
    print("🔧 Fixing pandas_ta numpy import error...")
    print("=" * 50)
    
    # Find the problematic file
    squeeze_pro_path = find_pandas_ta_squeeze_pro()
    
    if squeeze_pro_path is None:
        print("❌ Could not find pandas_ta squeeze_pro.py file")
        print("Please make sure pandas_ta is installed correctly")
        return False
    
    print(f"📁 Found file: {squeeze_pro_path}")
    
    # Patch the file
    success = patch_squeeze_pro_file(squeeze_pro_path)
    
    if success:
        print("\n🎉 pandas_ta import issue has been fixed!")
        print("\n💡 You can now run: streamlit run alwrity.py")
        return True
    else:
        print("\n⚠️  Failed to fix the import issue")
        return False

if __name__ == "__main__":
    main() 