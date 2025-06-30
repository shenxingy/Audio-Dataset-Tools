import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio(input_path, output_dir, min_silence_len=500, silence_thresh_offset=16, keep_silence=200):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 加载音频文件
    audio = AudioSegment.from_file(input_path)
    silence_thresh = audio.dBFS - silence_thresh_offset

    print(f"Audio dBFS: {audio.dBFS:.2f}, Using silence threshold: {silence_thresh:.2f} dB")

    # 切割音频
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )

    print(f"Found {len(chunks)} chunks.")

    # 导出每个音频片段
    for i, chunk in enumerate(chunks):
        out_path = os.path.join(output_dir, f"chunk_{i:03d}.wav")
        chunk.export(out_path, format="wav")
        print(f"Saved: {out_path}")

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
        keep_silence=args.keep_silence
    )
