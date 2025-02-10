import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

import requests

RELEASE_URL = "https://api.github.com/repos/curtisalexander/readstat-rs/releases/latest"
BINARY_MAPPINGS = {
    "readstat-v0.13.0-aarch64-apple-darwin.tar.gz": "readstat-macos-aarch64",
    "readstat-v0.13.0-x86_64-apple-darwin.tar.gz": "readstat-macos-x86_64",
    "readstat-v0.13.0-x86_64-pc-windows-msvc.zip": "readstat-windows-x86_64.exe",
    "readstat-v0.13.0-x86_64-unknown-linux-gnu.tar.gz": "readstat-linux-x86_64",
}


def extract_binary(archive_path, extract_dir, is_windows=False):
    binary_name = "readstat.exe" if is_windows else "readstat"
    extracted_binary = None

    print(f"Extracting {archive_path}...")
    if archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:gz") as tar:
            # List all files in the archive
            print("Files in archive:", tar.getnames())
            for member in tar.getmembers():
                if member.name.endswith(binary_name):
                    # Extract only the binary file
                    member.name = os.path.basename(member.name)
                    # Add filter parameter
                    tar.extract(member, extract_dir, filter="data")
                    extracted_binary = Path(extract_dir) / binary_name
                    break

    elif archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            # List all files in the archive
            print("Files in archive:", zip_ref.namelist())
            for info in zip_ref.infolist():
                if info.filename.endswith(binary_name):
                    # Extract only the binary file
                    info.filename = os.path.basename(info.filename)
                    zip_ref.extract(info, extract_dir)
                    extracted_binary = Path(extract_dir) / binary_name
                    break

    if extracted_binary and extracted_binary.exists():
        print(f"Successfully extracted binary: {extracted_binary}")
        print(f"Binary size: {extracted_binary.stat().st_size}")
        return extracted_binary
    return None


def download_binaries():
    print(f"Current working directory: {os.getcwd()}")

    try:
        print(f"Fetching release data from: {RELEASE_URL}")
        response = requests.get(RELEASE_URL)
        response.raise_for_status()
        release_data = response.json()

        version_tag = release_data.get("tag_name", "v0.13.0")
        print(f"Latest release: {version_tag}")
        print(
            f"Available assets: {[asset['name'] for asset in release_data.get('assets', [])]}"
        )

        bin_dir = Path(__file__).parent / "readstat_rs" / "bin"
        print(f"Creating directory: {bin_dir}")
        bin_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            for original_name, new_name in BINARY_MAPPINGS.items():
                url = f"https://github.com/curtisalexander/readstat-rs/releases/download/{version_tag}/{original_name}"
                print(f"\nDownloading {original_name} as {new_name}...")
                print(f"Download URL: {url}")

                response = requests.get(url)
                response.raise_for_status()

                # Save archive
                archive_path = temp_path / original_name
                archive_path.write_bytes(response.content)
                print(f"Archive size: {len(response.content)} bytes")

                # Extract binary
                extract_dir = temp_path / "extract"
                extract_dir.mkdir(exist_ok=True)

                binary_path = extract_binary(
                    str(archive_path), str(extract_dir), new_name.endswith(".exe")
                )
                if binary_path:
                    # Copy to final location
                    output_path = bin_dir / new_name
                    shutil.copy2(binary_path, output_path)

                    # Make binary executable on Unix-like systems
                    if not new_name.endswith(".exe"):
                        try:
                            os.chmod(output_path, 0o755)
                            print(f"Set executable permissions for {new_name}")
                        except OSError as e:
                            print(f"Warning: Could not set executable permissions: {e}")

                    print(f"Successfully installed {new_name}")
                else:
                    print(f"Could not find binary in {original_name}")

        # List contents of bin directory
        print("\nContents of bin directory:")
        for file in bin_dir.iterdir():
            print(f"- {file.name} ({file.stat().st_size} bytes)")
            if not file.name.endswith(".exe"):
                print(f"  Permissions: {oct(file.stat().st_mode)[-3:]}")
                print(f"  File type: {os.popen(f'file "{file}"').read().strip()}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching from GitHub API: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    download_binaries()
