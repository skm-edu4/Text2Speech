# tts_engine.py - Core TTS Engine (Edge-TTS with Async, Voices, and Batching)

import os
import re
import yaml
import logging
import asyncio
import edge_tts
from pathlib import Path

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
        if not self.logging.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logging.addHandler(console_handler)

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _create_safe_filename(self, text, max_words=5):
        """Generates a filesystem-safe filename using the first few words."""
        words = text.split()[:max_words]
        raw_name = "_".join(words)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', raw_name)
        if not safe_name:
            safe_name = "audio_clip"
        return f"{safe_name}.mp3"

    async def get_available_voices(self, language="en"):
        """Fetches available voices from Edge-TTS with a reliable fallback."""
        self.logging.info("Fetching available voices...")

        # Reliable fallback list of high-quality Edge-TTS voices
        fallback_voices = [
            {"name": "en-US-AriaNeural", "gender": "Female", "locale": "en-US"},
            {"name": "en-US-GuyNeural", "gender": "Male", "locale": "en-US"},
            {"name": "en-US-JennyNeural", "gender": "Female", "locale": "en-US"},
            {"name": "en-GB-SoniaNeural", "gender": "Female", "locale": "en-GB"},
            {"name": "en-GB-RyanNeural", "gender": "Male", "locale": "en-GB"},
            {"name": "en-AU-NatashaNeural", "gender": "Female", "locale": "en-AU"},
            {"name": "en-CA-ClaraNeural", "gender": "Female", "locale": "en-CA"},
            {"name": "en-IN-NeerjaNeural", "gender": "Female", "locale": "en-IN"},
        ]

        try:
            voices = await edge_tts.list_voices()
            filtered_voices = [
                {"name": v['ShortName'], "gender": v['Gender'], "locale": v['Locale']}
                for v in voices if v['Locale'].startswith(language)
            ]
            if not filtered_voices:
                self.logging.warning("No voices found via API, using fallback list.")
                return fallback_voices
            return filtered_voices
        except Exception as e:
            self.logging.warning(f"Failed to fetch voices from API ({e}). Using fallback list.")
            return fallback_voices

    async def generate_speech(self, text, voice="en-US-AriaNeural", output_filename=None):
        """Synthesize single text to speech."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        output_dir = self.config['output']['directory']
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        if output_filename is None:
            output_filename = self._create_safe_filename(text)
        output_path = os.path.join(output_dir, output_filename)

        preview = text[:40] + '...' if len(text) > 40 else text
        self.logging.info(f"Synthesizing: '{preview}' -> {output_filename} (Voice: {voice})")

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

        file_size = os.path.getsize(output_path) / 1024
        self.logging.info(f"✓ Saved: {output_filename} ({file_size:.1f} KB)")
        return output_path

    async def generate_batch(self, text_block, voice="en-US-AriaNeural"):
        """Processes multiple lines of text into separate, auto-named audio files."""
        lines = [line.strip() for line in text_block.split('\n') if line.strip()]
        self.logging.info(f"Starting batch processing for {len(lines)} lines...")

        generated_files = []
        for i, line in enumerate(lines, 1):
            try:
                # Each line gets its own auto-generated filename
                path = await self.generate_speech(line, voice)
                generated_files.append(os.path.basename(path))
            except Exception as e:
                self.logging.error(f"Failed on line {i}: {e}")

        return generated_files
