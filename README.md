# Audio Dataset Tools

A collection of utilities for processing and preparing audio datasets.

## Tools

### `split-by-silence.py`

Splits a single audio file into multiple chunks by detecting silent gaps. Useful for segmenting long recordings (lectures, podcasts, field recordings) into individual utterances or clips for dataset creation.

**How it works:** Computes the average loudness of the file (dBFS), then treats any region that falls more than `--silence_thresh_offset` dB below that average as silence. Regions of silence longer than `--min_silence_len` ms become split points.

## Setup

**Requirements:** Python 3.8+, and `ffmpeg` installed on your system (used by pydub under the hood).

Install ffmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python split-by-silence.py \
  --input  path/to/audio.mp3 \
  --out_dir path/to/output/
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` / `-i` | *(required)* | Path to the input audio file (mp3, wav, flac, etc.) |
| `--out_dir` / `-o` | *(required)* | Directory where split chunks are saved |
| `--min_silence_len` | `250` | Minimum silence duration to treat as a split point (ms) |
| `--silence_thresh_offset` | `16.0` | How many dB below average loudness counts as silence |
| `--keep_silence` | `200` | Silence padding kept at each chunk boundary (ms) |

### Tuning tips

- If you get **too many chunks** (over-splitting): increase `--min_silence_len` or decrease `--silence_thresh_offset`.
- If you get **too few chunks** (under-splitting): decrease `--min_silence_len` or increase `--silence_thresh_offset`.
- Chunks are exported as 16-bit WAV files named `chunk_000.wav`, `chunk_001.wav`, etc.

### Example

```bash
# Split a podcast with generous silence detection
python split-by-silence.py -i podcast.mp3 -o chunks/ \
  --min_silence_len 500 --silence_thresh_offset 14

# Split a field recording with tight silence detection
python split-by-silence.py -i field.wav -o chunks/ \
  --min_silence_len 150 --silence_thresh_offset 20
```

## License

MIT
