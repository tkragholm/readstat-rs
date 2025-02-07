import os
import platform
import subprocess
import sys
from pathlib import Path

def get_binary_path():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "darwin":
        # Handle both Intel and Apple Silicon Macs
        if machine == "arm64":
            binary_name = "readstat-macos-aarch64"
        else:
            binary_name = "readstat-macos-x86_64"
    elif system == "windows":
        binary_name = "readstat-windows-x86_64.exe"
    elif system == "linux":
        binary_name = "readstat-linux-x86_64"
    else:
        raise RuntimeError(f"Unsupported platform: {system}-{machine}")

    binary_path = Path(__file__).parent / "bin" / binary_name
    if not binary_path.exists():
        raise RuntimeError(f"Binary not found: {binary_path}")

    return str(binary_path)

def main():
    try:
        binary = get_binary_path()
        result = subprocess.run([binary] + sys.argv[1:])
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
