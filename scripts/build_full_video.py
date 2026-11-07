import os
import json
import subprocess
import imageio_ffmpeg
import sys

def build_video():
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs("demo_video/clips", exist_ok=True)
    
    with open("demo_video/scenes_meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    concat_list_path = "demo_video/concat_list.txt"
    clip_paths = []

    print("[1/3] Encoding individual 1080p scene clips...")
    for sc in meta["scenes"]:
        sc_id = sc["id"]
        slide_img = f"demo_video/slides/slide_{sc_id:02d}.png"
        audio_mp3 = f"demo_video/audio/scene_{sc_id}.mp3"
        clip_mp4 = f"demo_video/clips/clip_{sc_id:02d}.mp4"
        duration = sc["final_duration"]

        print(f"      Rendering Clip {sc_id:02d}: {sc['title']} (Duration: {duration:.2f}s)...")
        
        cmd = [
            ffmpeg_exe, "-y",
            "-loop", "1",
            "-framerate", "30",
            "-i", slide_img,
            "-i", audio_mp3,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-shortest",
            "-t", str(duration),
            clip_mp4
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR] Failed to render clip {sc_id}:\n", res.stderr)
            sys.exit(1)
        clip_paths.append(clip_mp4)

    # Write concat demuxer file
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in clip_paths:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")

    print("[2/3] Concatenating scenes into unified master track...")
    raw_master = "demo_video/raw_master_1080p.mp4"
    cmd_concat = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        raw_master
    ]
    res_concat = subprocess.run(cmd_concat, capture_output=True, text=True)
    if res_concat.returncode != 0:
        print("[ERROR] Concat failed:\n", res_concat.stderr)
        sys.exit(1)

    print("[3/3] Applying 1080p subtitle overlay & finalizing MP4...")
    final_output = "demo_video/WHID_Guard_5Min_Demo_1080p.mp4"
    
    # Path for libass filter: forward slashes, escaping colon
    ass_path = os.path.abspath("demo_video/subtitles.ass").replace("\\", "/")
    # in FFmpeg filter graph on Windows, C: must be escaped as C\\:
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    cmd_burn = [
        ffmpeg_exe, "-y",
        "-i", raw_master,
        "-vf", f"ass='{ass_filter_path}'",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "copy",
        "-movflags", "+faststart",
        final_output
    ]
    res_burn = subprocess.run(cmd_burn, capture_output=True, text=True)
    if res_burn.returncode != 0:
        print("[WARN] Libass filter burning encountered warning/fallback, attempting srt filter fallback...")
        srt_path = os.path.abspath("demo_video/subtitles.srt").replace("\\", "/")
        if ":" in srt_path:
            drive, rest = srt_path.split(":", 1)
            srt_filter_path = f"{drive}\\:{rest}"
        else:
            srt_filter_path = srt_path
        cmd_fallback = [
            ffmpeg_exe, "-y",
            "-i", raw_master,
            "-vf", f"subtitles='{srt_filter_path}'",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-c:a", "copy",
            "-movflags", "+faststart",
            final_output
        ]
        res_burn = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if res_burn.returncode != 0:
            print("[ERROR] Subtitle burning failed:\n", res_burn.stderr)
            sys.exit(1)

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n========================================================")
    print(f"[SUCCESS] Master 1080p Demo Video Generated Successfully!")
    print(f"Output File: {final_output}")
    print(f"File Size:   {file_size_mb:.2f} MB")
    print(f"Duration:    {meta['total_duration']:.2f} seconds ({meta['total_duration']/60:.2f} minutes)")
    print(f"Resolution:  1920x1080 (Full HD, 30 fps)")
    print(f"Audio Track: AAC Stereo 48 kHz (192 kbps)")
    print(f"Subtitles:   Burned-in High-Contrast 1080p + Standalone demo_video/subtitles.srt")
    print(f"========================================================\n")

if __name__ == "__main__":
    build_video()
