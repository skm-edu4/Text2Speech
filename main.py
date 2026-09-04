#!/usr/bin/env python3
# main.py - Main Entry Point for TTS Application

import os
import sys
import argparse
import asyncio
import json
from pathlib import Path

def check_dependencies():
    missing_packages = []
    try: import yaml
    except ImportError: missing_packages.append("pyyaml")
    try: import edge_tts
    except ImportError: missing_packages.append("edge-tts")

    if missing_packages:
        print("✗ Missing required packages:")
        for pkg in missing_packages: print(f"  - {pkg}")
        print(f"\nInstall with: pip install {' '.join(missing_packages)}")
        sys.exit(1)

def interactive_mode(engine):
    print("\n" + "="*60)
    print("  TTS Engine - Interactive Mode")
    print("="*60)
    print("Commands: 'settings' (show config), 'quit' (exit)")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("Enter text (or 'quit'): ").strip()
            if not user_input: continue
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋"); break
            if user_input.lower() == 'settings':
                print("\n--- Configuration ---\n" + json.dumps(engine.config, indent=2) + "\n")
                continue

            output_file = asyncio.run(engine.generate_speech(user_input))
            print(f"✓ Audio saved: {output_file}\n")
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋"); break
        except Exception as e:
            print(f"✗ Error: {e}\n")

def batch_mode(engine, input_file, voice):
    if not os.path.exists(input_file):
        print(f"✗ Input file not found: {input_file}"); sys.exit(1)

    print(f"\nProcessing: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"Found {len(lines)} line(s) to synthesize.\n")
    for i, line in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}] {line}")
        try:
            output_file = asyncio.run(engine.generate_speech(line, voice=voice))
            print(f"      → {output_file}\n")
        except Exception as e:
            print(f"      ✗ Error: {e}\n")

def main():
    check_dependencies()
    parser = argparse.ArgumentParser(description="Text-to-Speech using Edge-TTS")
    parser.add_argument('-t', '--text', type=str, help='Text to synthesize')
    parser.add_argument('-f', '--file', type=str, help='Input file for batch mode')
    parser.add_argument('-v', '--voice', type=str, default='en-US-AriaNeural', help='Voice to use (e.g., en-US-GuyNeural)')
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help='Config file path')
    parser.add_argument('-o', '--output', type=str, help='Output filename')

    args = parser.parse_args()

    if args.text and args.file:
        print("✗ Cannot use both -t and -f options together"); sys.exit(1)
    if not os.path.exists(args.config):
        print(f"✗ Config file not found: {args.config}"); sys.exit(1)

    print("\n" + "="*60)
    print("  Text-to-Speech Engine (Edge-TTS)")
    print("="*60)

    try:
        from tts_engine import TTSEngine
        engine = TTSEngine(config_path=args.config)

        if args.text:
            output_file = asyncio.run(engine.generate_speech(args.text, args.voice, args.output))
            print(f"\n✓ Audio saved: {output_file}")
        elif args.file:
            batch_mode(engine, args.file, args.voice)
        else:
            interactive_mode(engine)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
