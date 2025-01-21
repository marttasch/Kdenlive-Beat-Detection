# Kdenlive Beat Detection

This script analyzes audio files, detects beats, and generates timeline guides for use in video editing software like Kdenlive. It supports both single-file and batch processing modes and is highly configurable to suit various audio analysis needs.

## Features

- **Single File Processing**: Process a single audio file to detect beats and generate a guide.
- **Batch Processing**: Automatically process all supported audio files in the current directory.
- **Output Customization**: Specify output files and directories for organizing results.
- **Interactive User Prompts**: Guides users when arguments are missing.
- **Progress Feedback**: Displays progress using a progress bar in batch mode.

## Requirements

This script requires Python and the following libraries:

- `librosa`
- `tqdm`

You can install the required libraries using:

```bash
pip install librosa tqdm
```

## Usage

Run the script with the following command:

```bash
python beatfinder.py [options]
```

### Arguments

- `input_file` (optional): Path to the audio file for single mode.
- `--output_file`: Path to the output file for single mode. Defaults to `<input_file>_beats.txt`.
- `--bpm`: Initial BPM guess (float, beats per minute). Optional.
- `--offset`: Offset to add to beat times (default: `0:00:0`). Format: `HH:MM:SS`.
- `--tightness`: Tightness of beat distribution around tempo (default: 100).
- `--mode`: Choose `single` (default) or `batch` mode.
- `--output_dir`: Directory to save output files in batch mode (default: current directory).

### Examples

#### Single File Mode

To process a single audio file:

```bash
python beatfinder.py example.wav --output_file example_beats.txt --bpm 120 --offset 0:00:05
```

#### Batch Mode

To process all audio files in the current directory:

```bash
python beatfinder.py --mode batch --output_dir ./output --bpm 120
```

This will create beat files in the `./output` directory.

## Supported File Formats

The script supports the following audio file formats:

- `.wav`
- `.mp3`
- `.flac`

## Output Format

The output is a plain text file with two columns:

1. **Timestamp**: The timestamp of the beat in `HH:MM:SS.sss` format.
2. **Index**: The sequential index of the beat.

Example:

```
0:00:01.500 0
0:00:03.000 1
0:00:04.500 2
```

## Using with Kdenlive

The generated text files can be used to import markers or guides for beats in Kdenlive. To do this:

1. Open the **Guides** view in Kdenlive (View -> Guides).
2. Select the audio file from the project content.
3. In the Guides view, choose **Import Marker from TXT File** and select the generated `.txt` file.

This will add beat markers to your audio, synchronized with the audio.

## Code Basis

This script is adapted from the gist: [https://gist.github.com/gepron1x/efb0c6b55b26d1cef91c9e831d727504](https://gist.github.com/gepron1x/efb0c6b55b26d1cef91c9e831d727504)

Feel free to reach out with questions or feedback!

