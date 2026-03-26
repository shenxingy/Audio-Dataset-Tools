import os
import sys
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence


def split_audio(input_path, output_dir, min_silence_len=500, silence_thresh_offset=16, keep_silence=200):
    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        print(f"Error: could not load audio file '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)

    silence_thresh = audio.dBFS - silence_thresh_offset
    print(f"Audio dBFS: {audio.dBFS:.2f}, Using silence threshold: {silence_thresh:.2f} dB")

    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
    )

    if not chunks:
        print("Warning: no chunks found. Try lowering --silence_thresh_offset or --min_silence_len.")
        return

    print(f"Found {len(chunks)} chunks.")

    for i, chunk in enumerate(chunks):
        out_path = os.path.join(output_dir, f"chunk_{i:03d}.wav")
        try:
            chunk.export(out_path, format="wav")
            print(f"Saved: {out_path}")
        except Exception as e:
            print(f"Error: could not save chunk {i} to '{out_path}': {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split audio file by silence.")
    parser.add_argument("--input", "-i", required=True, help="Path to input audio file")
    parser.add_argument("--out_dir", "-o", required=True, help="Output directory")
    parser.add_argument("--min_silence_len", type=int, default=250, help="Minimum length of silence (ms)")
    parser.add_argument("--silence_thresh_offset", type=float, default=16.0, help="How much below dBFS is considered silence")
    parser.add_argument("--keep_silence", type=int, default=200, help="How much silence to retain at edges (ms)")
    args = parser.parse_args()

    split_audio(
        input_path=args.input,
        output_dir=args.out_dir,
        min_silence_len=args.min_silence_len,
        silence_thresh_offset=args.silence_thresh_offset,
        keep_silence=args.keep_silence,
    )
