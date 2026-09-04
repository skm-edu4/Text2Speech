#!/usr/bin/env python3
# main.py - Main Entry Point for TTS Application (Edge-TTS)

import os
import sys
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    missing_packages = []

    try:
        import yaml
    except ImportError:
        missing_packages.append("pyyaml")

    try:
        import edge_tts
    except ImportError:
        missing_packages.append("edge-tts")

    if missing_packages:
        print("✗ Missing required packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing_packages)}")
        sys.exit(1)

def interactive_mode(engine):
    """Run in interactive mode."""
    print("\n" + "="*60)
    print("  TTS Engine - Interactive Mode (Edge-TTS)")
    print("="*60)
    print("Commands:")
    print("  - Type any text to synthesize")
    print("  - 'quit' or 'exit' - Exit the program")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("Enter text (or 'quit' to exit): ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break

            # Generate speech
            output_file = engine.generate_speech(user_input)
            print(f"✓ Audio saved: {output_file}\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"✗ Error: {e}\n")

def batch_mode(engine, input_file):
    """Process multiple lines from a file."""
    if not os.path.exists(input_file):
        print(f"✗ Input file not found: {input_file}")
        sys.exit(1)

    print(f"\nProcessing: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"Found {len(lines)} line(s) to synthesize.\n")

    for i, line in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}] {line}")
        try:
            output_file = engine.generate_speech(line)
            print(f"      → {output_file}\n")
        except Exception as e:
            print(f"      ✗ Error: {e}\n")

def main():
    """Main entry point."""
    # Check dependencies first
    check_dependencies()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="High-Quality Text-to-Speech using Edge-TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py -t "Hello World"          # Single text synthesis
  python main.py -f input.txt              # Batch mode from file
  python main.py -c custom_config.yaml     # Use custom config
        """
    )

    parser.add_argument(
        '-t', '--text',
        type=str,
        help='Text to synthesize (single line)'
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Input file with text lines (batch mode)'
    )

    parser.add_argument(
        '-c', '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output filename (default: auto-generated from text)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.text and args.file:
        print("✗ Cannot use both -t and -f options together")
        sys.exit(1)

    # Check if config exists
    if not os.path.exists(args.config):
        print(f"✗ Config file not found: {args.config}")
        print("\nPlease create a config.yaml file or specify a valid config.")
        sys.exit(1)

    print("\n" + "="*60)
    print("  High-Quality TTS Engine (Edge-TTS)")
    print("="*60)

    try:
        # Initialize the engine
        from tts_engine import TTSEngine
        engine = TTSEngine(config_path=args.config)

        # Single text mode
        if args.text:
            output_file = engine.generate_speech(args.text, args.output)
            print(f"\n✓ Audio saved: {output_file}")
            return

        # Batch file mode
        if args.file:
            batch_mode(engine, args.file)
            return

        # Default: Interactive mode
        interactive_mode(engine)

    except FileNotFoundError as e:
        print(f"\n📁 File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
