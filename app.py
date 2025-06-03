#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from web_ui import TranslationWebUI


def main():
    parser = argparse.ArgumentParser(description="PLaMo-2 Translation Web UI")
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public shareable link"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the server on (default: 7860)"
    )
    
    args = parser.parse_args()
    
    print("Starting PLaMo-2 Translation Web UI...")
    print(f"Server will run on port {args.port}")
    
    if args.share:
        print("Note: Public sharing enabled")
    
    app = TranslationWebUI()
    app.launch(share=args.share, server_port=args.port)


if __name__ == "__main__":
    main()