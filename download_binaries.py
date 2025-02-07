import requests
import os
import platform
from pathlib import Path

RELEASE_URL = "https://api.github.com/repos/curtisalexander/readstat-rs/releases/latest"
BINARY_NAMES = {
    "readstat-x86_64-pc-windows-msvc.exe": "readstat-windows-x86_64.exe",
    "readstat-x86_64-apple-darwin": "readstat-macos-x86_64",
    "readstat-aarch64-apple-darwin": "readstat-macos-aarch64",
    "readstat-x86_64-unknown-linux-gnu": "readstat-linux-x86_64"
}

def download_binaries():
    response = requests.get(RELEASE_URL)
    release_data = response.json()

    bin_dir = Path("readstat_dist/bin")
    bin_dir.mkdir(parents=True, exist_ok=True)

    for asset in release_data["assets"]:
        original_name = asset["name"]
        if original_name in BINARY_NAMES:
            new_name = BINARY_NAMES[original_name]
            download_url = asset["browser_download_url"]

            print(f"Downloading {original_name} as {new_name}...")
            response = requests.get(download_url)

            output_path = bin_dir / new_name
            output_path.write_bytes(response.content)

            # Make binary executable on Unix-like systems
            if not new_name.endswith('.exe'):
                os.chmod(output_path, 0o755)

if __name__ == "__main__":
    download_binaries()
