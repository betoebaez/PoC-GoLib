from setuptools import setup, find_packages
from pathlib import Path
import os
import platform
import subprocess
import shutil

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Version
VERSION = "1.0.0"


class BuildLibrary:
    """Helper class to build the Go shared library."""
    
    @staticmethod
    def build_library():
        """Build the Go shared library."""
        print("🏗️  Building LibCoreHey shared library...")
        
        # Check if Go is available
        if not shutil.which('go'):
            print("⚠️  Go compiler not found. Skipping library build.")
            print("💡 Note: This package requires Go to be installed, or use pre-built binaries.")
            return False
        
        # Check if lib.go exists
        if not Path('lib.go').exists():
            raise RuntimeError("lib.go source file not found.")
        
        # Create libcorehey directory if it doesn't exist
        lib_dir = Path('libcorehey')
        lib_dir.mkdir(exist_ok=True)
        
        # Build library based on platform
        system = platform.system()
        if system == "Darwin":  # macOS
            lib_file = lib_dir / "libcorehey.dylib"
            subprocess.run(
                ["go", "build", "-buildmode=c-shared", "-o", str(lib_file), "lib.go"],
                check=True
            )
            # Sign the library for macOS
            try:
                subprocess.run(["codesign", "-s", "-", str(lib_file)], 
                             check=False, capture_output=True)
            except:
                pass  # Signing is optional
        elif system == "Linux":
            lib_file = lib_dir / "libcorehey.so"
            subprocess.run(
                ["go", "build", "-buildmode=c-shared", "-o", str(lib_file), "lib.go"],
                check=True
            )
        elif system == "Windows":
            lib_file = lib_dir / "libcorehey.dll"
            subprocess.run(
                ["go", "build", "-buildmode=c-shared", "-o", str(lib_file), "lib.go"],
                check=True
            )
        else:
            raise RuntimeError(f"Unsupported platform: {system}")
        
        print(f"✅ Built {lib_file}")


# Check for existing pre-built binaries
import glob
existing_libs = []
for ext in ["libcorehey/*.dylib", "libcorehey/*.so", "libcorehey/*.dll"]:
    existing_libs.extend(glob.glob(ext))

if existing_libs:
    print(f"✅ Found pre-built binaries: {[lib.split('/')[-1] for lib in existing_libs]}")
    print("🎉 No Go compiler required - using pre-compiled binaries!")
else:
    # Check if we're in CI environment (GitHub Actions)
    in_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'
    
    if in_ci:
        print("⚠️  Running in CI - skipping build, expecting pre-built binaries")
    else:
        # Only try to build if no binaries exist and not in CI
        print("No pre-built binaries found, attempting to build library...")
        build_success = BuildLibrary.build_library()
        if not build_success:
            print("⚠️  Library build failed. Package will install but may not work until binaries are provided.")
            print("💡 Solutions:")
            print("   1. Install Go: apt install golang-go (Linux) or brew install go (macOS)")
            print("   2. Use pre-built binaries from GitHub releases")
            print("   3. Contact package maintainer for assistance")

# Detect architecture and platform
arch = platform.machine()
os_name = platform.system().lower()

# Map architecture and platform to binary names
binary_name = None
if os_name == "linux":
    if arch == "x86_64":
        binary_name = "libcorehey_amd64.so"
    elif arch == "aarch64":
        binary_name = "libcorehey_arm64.so"
elif os_name == "darwin":
    binary_name = "libcorehey.dylib"
elif os_name == "windows":
    binary_name = "libcorehey.dll"

if not binary_name:
    raise RuntimeError(f"Unsupported platform or architecture: {os_name} {arch}")

# Include the binary in package data
lib_files = [binary_name]

# Update package_data to include the architecture-specific binary
setup(
    name="LibCoreHey",
    version=VERSION,
    author="HeyBanco Team",
    author_email="dev@heybanco.com",
    description="Python wrapper for HeyBanco's core Go library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heybanco/LibCoreHey",  # Update this with your actual repo
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Go",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Communications",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No additional Python dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
        ],
    },
    package_data={
        "libcorehey": lib_files,
    },
    include_package_data=True,
    zip_safe=False,  # Required for shared libraries
    keywords="heybanco api whatsapp go python wrapper",
    project_urls={
        "Bug Reports": "https://github.com/heybanco/LibCoreHey/issues",
        "Source": "https://github.com/heybanco/LibCoreHey",
        "Documentation": "https://github.com/heybanco/LibCoreHey/blob/main/README.md",
    },
)