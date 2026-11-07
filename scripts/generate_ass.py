import json

def generate_ass():
    with open("demo_video/scenes_meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    ass_content = """[Script Info]
Title: WHID-Guard Demo Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,30,&H00FFFFFF,&H000000FF,&H000B0F19,&H80000000,-1,0,0,0,100,100,0,0,1,2.5,1,2,120,120,55,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def fmt_ass_time(secs):
        hrs = int(secs // 3600)
        mins = int((secs % 3600) // 60)
        scs = int(secs % 60)
        cs = int((secs - int(secs)) * 100) # centiseconds
        return f"{hrs:d}:{mins:02d}:{scs:02d}.{cs:02d}"

    for sub in meta["subtitles"]:
        t_start = fmt_ass_time(sub["start"])
        t_end = fmt_ass_time(sub["end"])
        text = sub["text"].strip().replace("\n", " ")
        ass_content += f"Dialogue: 0,{t_start},{t_end},Default,,0,0,0,,{text}\n"

    with open("demo_video/subtitles.ass", "w", encoding="utf-8") as f:
        f.write(ass_content)

    print("[SUCCESS] Generated demo_video/subtitles.ass")

if __name__ == "__main__":
    generate_ass()
