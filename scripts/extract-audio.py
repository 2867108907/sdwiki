#!/usr/bin/env python3
# Extract text from audio/video files using OpenAI Whisper
# Usage: ./scripts/extract-audio.py input.mp3 output.txt
#        ./scripts/extract-audio.py input.mp4 output.txt (ffmpeg required)

import argparse
import os
import shutil
import subprocess
import sys


def install_package(package):
    """Install a Python package using pip"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please install it manually.")
        return False


def check_dependencies():
    """Check if required dependencies are installed, install if missing"""
    try:
        import whisper
        print("✓ openai-whisper is already installed")
        return whisper
    except ImportError:
        print("openai-whisper not found. Attempting to install...")
        if install_package("openai-whisper"):
            print("✓ openai-whisper installed successfully")
            # Try importing again after installation
            import whisper
            return whisper
        else:
            sys.exit(1)


def check_ffmpeg():
    """Check if ffmpeg is available, attempt to install if missing"""
    if shutil.which('ffmpeg'):
        print("✓ ffmpeg is already installed")
        return True

    print("ffmpeg not found, required for processing video files")

    # Detect package manager
    if shutil.which('brew'):
        # macOS with Homebrew
        print("Detected Homebrew, attempting to install ffmpeg...")
        try:
            subprocess.check_call(['brew', 'install', 'ffmpeg'])
            print("✓ ffmpeg installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install ffmpeg via Homebrew")
    elif shutil.which('apt'):
        # Ubuntu/Debian
        print("Detected apt, attempting to install ffmpeg...")
        try:
            subprocess.check_call(['sudo', 'apt', 'install', '-y', 'ffmpeg'])
            print("✓ ffmpeg installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install ffmpeg via apt")
    elif shutil.which('apt-get'):
        # Debian alternative
        print("Detected apt-get, attempting to install ffmpeg...")
        try:
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'])
            print("✓ ffmpeg installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install ffmpeg via apt-get")

    print("\nAutomatic installation failed. Please install ffmpeg manually:")
    print("  macOS: brew install ffmpeg")
    print("  Ubuntu/Debian: sudo apt install ffmpeg")
    print("  Other: See https://ffmpeg.org/download.html")
    sys.exit(1)


def extract_audio_from_video(video_path, audio_path):
    """Extract audio track from video file"""
    cmd = ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'copy', audio_path]
    print(f"Extracting audio: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error extracting audio: {result.stderr}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from audio/video using Whisper'
    )
    parser.add_argument('input', help='Input audio/video file (.mp3, .wav, .mp4, .mov, etc.)')
    parser.add_argument('output', help='Output text file')
    parser.add_argument('--model', default='base', help='Whisper model size (tiny/base/small/medium/large)')
    parser.add_argument('--language', default=None, help='Language code (e.g. zh, en, ja)')
    args = parser.parse_args()

    # Check input exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found")
        sys.exit(1)

    # Create output directory if needed
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Handle video files - extract audio first
    input_file = args.input
    temp_audio = None
    ext = os.path.splitext(args.input)[1].lower()

    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']:
        # Video file - extract audio
        check_ffmpeg()
        temp_audio = os.path.join(out_dir, os.path.splitext(os.path.basename(args.output))[0] + '.aac')
        extract_audio_from_video(args.input, temp_audio)
        input_file = temp_audio

    # Check and import whisper (installs if missing)
    whisper = check_dependencies()

    # Load model and transcribe
    print(f"Loading Whisper model: {args.model}")
    model = whisper.load_model(args.model)

    print(f"Transcribing: {input_file}")
    result = model.transcribe(input_file, language=args.language, verbose=False)

    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        for segment in result['segments']:
            f.write(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text'].strip()}\n")

    # Cleanup temp audio
    if temp_audio and os.path.exists(temp_audio):
        os.remove(temp_audio)

    lines = len(result['segments'])
    print(f"\n✓ Extracted text to {args.output}")
    print(f"Segments: {lines}, Total words: {sum(len(s['text'].split()) for s in result['segments'])}")


if __name__ == '__main__':
    main()
