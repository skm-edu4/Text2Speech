# tts_engine.py - Clean Core TTS Engine (Edge-TTS Only)

import os
import re
import yaml
import logging
import asyncio
import edge_tts
from pathlib import Path
from datetime import datetime

class TTSEngine:
    def __init__(self, config_path="config.yaml"):
        self._setup_logging(config_path)
        self.config = self._load_config(config_path)
        self.logging.info("✓ TTS Engine initialized and ready!")

    def _setup_logging(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        log_level = config.get('logging', {}).get('level', 'INFO').upper()
        self.logging = logging.getLogger('TTSEngine')
        self.logging.setLevel(getattr(logging, log_level, logging.INFO))
        self.logging.handlers = []
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logging.addHandler(console_handler)

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _create_safe_filename(self, text, max_words=5):
        """
        Generates a filesystem-safe filename using the first few words of the text.
        Example: "Hello world, I am speaking!" -> "Hello_world_I_am.mp3"
        """
        # 1. Split text into words and grab the first N words
        words = text.split()[:max_words]
        raw_name = "_".join(words)

        # 2. Remove any non-alphanumeric characters (keeps letters, numbers, and underscores)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', raw_name)

        # 3. Fallback if the text started with symbols (e.g., "!!! Hello")
        if not safe_name:
            safe_name = "audio_clip"

        # Edge-TTS natively outputs MP3, which is great for keeping file sizes low!
        return f"{safe_name}.mp3"

    def generate_speech(self, text, output_filename=None):
        """Synthesize text to speech using Edge-TTS and auto-name by first words."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        output_dir = self.config['output']['directory']
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Auto-generate filename from the text if one wasn't manually provided
        if output_filename is None:
            output_filename = self._create_safe_filename(text, max_words=5)

        output_path = os.path.join(output_dir, output_filename)

        # Log the action
        preview = text[:50] + '...' if len(text) > 50 else text
        self.logging.info(f"Synthesizing: '{preview}' -> {output_filename}")

        try:
            # Initialize Edge-TTS with a great default voice
            communicate = edge_tts.Communicate(text, "en-US-AriaNeural")

            # Save the audio file (Edge-TTS handles the async loop internally)
            asyncio.run(communicate.save(output_path))

            file_size = os.path.getsize(output_path) / 1024
            self.logging.info(f"✓ Audio saved: {output_path} ({file_size:.1f} KB)")

            return output_path

        except Exception as e:
            self.logging.error(f"✗ Synthesis failed: {e}")
            raise

if __name__ == "__main__":
    print("Testing TTS Engine...")
    engine = TTSEngine()
    engine.generate_speech("Hello! The debugging fix is working perfectly.")
