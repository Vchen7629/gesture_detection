#!/usr/bin/env python3
"""Helper script to compile Qt resources and run labelImg."""

import os
import subprocess
import sys
from pathlib import Path

def main():
    # Get the project root and labelImg directory
    project_root = Path(__file__).parent
    labelimg_dir = project_root / "labelImg"
    resources_file = labelimg_dir / "libs" / "resources.py"
    qrc_file = labelimg_dir / "resources.qrc"

    # Check if resources.py exists, if not compile it
    if not resources_file.exists():
        print("Compiling Qt resources...")
        try:
            subprocess.run(
                ["pyrcc5", "-o", str(resources_file), str(qrc_file)],
                cwd=labelimg_dir,
                check=True
            )
            print("Resources compiled successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling resources: {e}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: pyrcc5 not found. Make sure PyQt5 is installed.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Resources already compiled, skipping compilation.")

    # Run labelImg with any command-line arguments
    print("Starting labelImg...")
    labelimg_script = labelimg_dir / "labelImg.py"

    # Change to labelImg directory and run the script
    os.chdir(labelimg_dir)

    # Import and run labelImg (this way it runs in the same process with uv's environment)
    sys.path.insert(0, str(labelimg_dir))

    # Pass any additional arguments
    sys.argv = [str(labelimg_script)] + sys.argv[1:]

    # Execute the labelImg script
    with open(labelimg_script) as f:
        code = compile(f.read(), labelimg_script, 'exec')
        exec(code, {'__name__': '__main__', '__file__': str(labelimg_script)})

if __name__ == "__main__":
    main()