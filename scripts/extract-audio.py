#!/usr/bin/env python3
# Extract text from audio/video files using OpenAI Whisper
# Usage: ./scripts/extract-audio.py input.mp3
#        ./scripts/extract-audio.py input.mp4 (ffmpeg required)

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def install_package(package):
    """Install a Python package using pip"""
    print(f"Installing {package}...", file=sys.stderr)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please install it manually.", file=sys.stderr)
        return False


def check_dependencies():
    """Check if required dependencies are installed, install if missing"""
    try:
        import whisper
        print("openai-whisper is already installed", file=sys.stderr)
        return whisper
    except ImportError:
        print("openai-whisper not found. Attempting to install...", file=sys.stderr)
        if install_package("openai-whisper"):
            print("openai-whisper installed successfully", file=sys.stderr)
            import whisper
            return whisper
        else:
            sys.exit(1)


def check_ffmpeg():
    """Check if ffmpeg is available, attempt to install if missing"""
    if shutil.which('ffmpeg'):
        print("ffmpeg is already installed", file=sys.stderr)
        return True

    print("ffmpeg not found, required for processing video files", file=sys.stderr)

    if shutil.which('brew'):
        print("Detected Homebrew, attempting to install ffmpeg...", file=sys.stderr)
        try:
            subprocess.check_call(['brew', 'install', 'ffmpeg'])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install ffmpeg via Homebrew", file=sys.stderr)
    elif shutil.which('apt') or shutil.which('apt-get'):
        manager = 'apt' if shutil.which('apt') else 'apt-get'
        print(f"Detected {manager}, attempting to install ffmpeg...", file=sys.stderr)
        try:
            subprocess.check_call(['sudo', manager, 'install', '-y', 'ffmpeg'])
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install ffmpeg via {manager}", file=sys.stderr)

    print("\nAutomatic installation failed. Please install ffmpeg manually:", file=sys.stderr)
    print("  macOS: brew install ffmpeg", file=sys.stderr)
    print("  Ubuntu/Debian: sudo apt install ffmpeg", file=sys.stderr)
    sys.exit(1)


def extract_audio_from_video(video_path, audio_path):
    """Extract audio track from video file"""
    cmd = ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'copy', audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error extracting audio: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from audio/video using Whisper'
    )
    parser.add_argument('input', help='Input audio/video file')
    parser.add_argument('--model', default='base', help='Whisper model size')
    parser.add_argument('--language', default=None, help='Language code (e.g. zh, en, ja)')
    args = parser.parse_args()

    # Check input exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found", file=sys.stderr)
        sys.exit(1)

    # Handle video files - extract audio first
    input_file = args.input
    temp_audio = None
    ext = os.path.splitext(args.input)[1].lower()

    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']:
        check_ffmpeg()
        temp_audio = tempfile.NamedTemporaryFile(suffix='.aac', delete=False).name
        extract_audio_from_video(args.input, temp_audio)
        input_file = temp_audio

    # Check and import whisper
    whisper = check_dependencies()

    # Load model and transcribe
    print(f"Loading Whisper model: {args.model}", file=sys.stderr)
    model = whisper.load_model(args.model)

    print(f"Transcribing: {input_file}", file=sys.stderr)
    result = model.transcribe(input_file, language=args.language, verbose=False)

    # Output to stdout
    for segment in result['segments']:
        print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text'].strip()}")

    # Cleanup temp audio
    if temp_audio and os.path.exists(temp_audio):
        os.remove(temp_audio)

    lines = len(result['segments'])
    words = sum(len(s['text'].split()) for s in result['segments'])
    print(f"\n--- Transcribed {lines} segments, {words} words from {args.input} ---", file=sys.stderr)


if __name__ == '__main__':
    main()
