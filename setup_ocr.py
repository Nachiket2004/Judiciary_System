#!/usr/bin/env python3
"""
Setup script for OCR dependencies
"""
import os
import sys
import platform
import subprocess

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✅ Tesseract is already installed:")
        print(result.stdout.split('\n')[0])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_tesseract():
    """Provide installation instructions for Tesseract"""
    system = platform.system().lower()
    
    print("❌ Tesseract OCR is not installed on your system.")
    print("\n📋 Installation Instructions:")
    
    if system == "windows":
        print("Windows:")
        print("1. Download Tesseract installer from:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Run the installer and follow the setup wizard")
        print("3. Add Tesseract to your PATH or set TESSERACT_CMD in .env")
        print("   Example: TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        
    elif system == "darwin":  # macOS
        print("macOS:")
        print("1. Install Homebrew if not already installed:")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Install Tesseract:")
        print("   brew install tesseract")
        
    elif system == "linux":
        print("Linux (Ubuntu/Debian):")
        print("   sudo apt-get update")
        print("   sudo apt-get install tesseract-ocr")
        print("\nLinux (CentOS/RHEL/Fedora):")
        print("   sudo yum install tesseract")
        print("   # or")
        print("   sudo dnf install tesseract")
        
    else:
        print(f"Unsupported system: {system}")
        print("Please install Tesseract OCR manually for your system.")
    
    print("\n🔄 After installation, run this script again to verify.")

def test_ocr():
    """Test OCR functionality"""
    try:
        import pytesseract
        from PIL import Image
        import tempfile
        import numpy as np
        
        print("\n🧪 Testing OCR functionality...")
        
        # Create a simple test image with text
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a white image
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((10, 30), "TEST OCR TEXT", fill='black', font=font)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)
            
            # Test OCR
            text = pytesseract.image_to_string(img)
            
            if "TEST" in text.upper():
                print("✅ OCR test successful!")
                print(f"   Extracted text: {text.strip()}")
            else:
                print("⚠️  OCR test completed but text extraction may be inaccurate")
                print(f"   Extracted text: {text.strip()}")
            
            # Clean up
            os.unlink(tmp.name)
            
    except ImportError as e:
        print(f"❌ Python OCR libraries not installed: {e}")
        print("   Run: pip install pytesseract Pillow")
    except Exception as e:
        print(f"❌ OCR test failed: {e}")

def main():
    print("🔍 AI Judiciary Platform - OCR Setup")
    print("=" * 40)
    
    # Check if Tesseract is installed
    if check_tesseract():
        test_ocr()
        print("\n✅ OCR setup is complete!")
        print("   You can now use the lawyer verification system.")
    else:
        install_tesseract()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())