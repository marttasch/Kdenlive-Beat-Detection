# This script was adapted and extended from a gist by gepron1x: 
# https://gist.github.com/gepron1x/efb0c6b55b26d1cef91c9e831d727504
# It provides beat detection and timeline guide generation for Kdenlive.

import argparse
import librosa  # you need librosa to get this working
import datetime
import os
from tqdm import tqdm  # for progress bar
import logging

def parse_delta(s):
    date = datetime.datetime.strptime(s, "%H:%M:%S")
    return datetime.timedelta(hours=date.hour, minutes=date.minute, seconds=date.second)

def process_file(input_file, output_file, bpm, offset, tightness):
    """Process a single audio file to detect beats and write output."""
    try:
        print(f"Analyzing {input_file}...")
        y, sr = librosa.load(input_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, bpm=bpm, tightness=tightness)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        if output_file is None:
            output_file = f"{input_file}_beats.txt"

        print(f"{input_file} BPM: {tempo[0]:.2f}")
        print(f"Writing timeline guides to {output_file}...")
        with open(output_file, "wt") as f:
            for i, seconds in enumerate(beat_times):
                f.write(f"{str(datetime.timedelta(seconds=seconds) + offset)} {i}\n")
    except Exception as e:
        logging.error(f"Error processing file {input_file}: {e}")

def main():
    # === Setup Logging ===
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # === Parse Arguments ===
    parser = argparse.ArgumentParser(
        prog='Kdenlive beatfinder',
        description='Creates timeline guides matching the song beat')

    parser.add_argument('input_file', nargs='?', help="Input audio file (leave empty for batch mode)")
    parser.add_argument('--output_file', required=False, help="Output txt file for beat times (single mode only)")
    parser.add_argument("--bpm", type=float, default=None, help="Initial BPM guess [float, beats per minute]")
    parser.add_argument("--offset", default="0:00:0", help="Offset to add to the beat times [HH:MM:SS]")
    parser.add_argument("--tightness", type=float, default=100, help="Tightness of beat distribution around tempo")
    parser.add_argument("--mode", choices=['single', 'batch'], default='single', help="Processing mode: single file or batch processing")
    parser.add_argument("--output_dir", default=".", help="Directory to save output files in batch mode")

    args = parser.parse_args()
    offset = parse_delta(args.offset)

    # === Validate Arguments ===
    if args.mode == 'single':
        if not args.input_file:
            args.input_file = input("Enter the input file path: ")
        if not os.path.isfile(args.input_file):
            print(f"Error: File '{args.input_file}' not found.")
            return

    if args.mode == 'batch' and not os.path.isdir(args.output_dir):
        print(f"Error: Output directory '{args.output_dir}' does not exist.")
        return

    # === Single Mode ===
    if args.mode == 'single':
        process_file(args.input_file, args.output_file, args.bpm, offset, args.tightness)

    # === Batch Mode ===
    elif args.mode == 'batch':
        print("Batch mode activated. Processing all supported audio files in the current directory...")
        supported_extensions = ['.wav', '.mp3', '.flac']
        audio_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].lower() in supported_extensions]

        if not audio_files:
            print("No supported audio files found in the current directory.")
            return

        os.makedirs(args.output_dir, exist_ok=True)
        for audio_file in tqdm(audio_files, desc="Processing files", unit="file"):
            output_file = os.path.join(args.output_dir, f"{os.path.splitext(audio_file)[0]}_beats.txt")
            process_file(audio_file, output_file, args.bpm, offset, args.tightness)

        print(f"Batch processing completed. Processed {len(audio_files)} file(s). Outputs saved to '{args.output_dir}'.")

if __name__ == '__main__':
    main()
