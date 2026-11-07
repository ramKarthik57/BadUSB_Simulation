import asyncio
import edge_tts
import os
import subprocess
import imageio_ffmpeg
import json

VOICE = "en-US-ChristopherNeural"
RATE = "+6%" # Clear, confident presentation tempo (~145 WPM)

SCENES = [
    {
        "id": 1,
        "title": "Introduction & Architecture Overview",
        "target_seconds": 35,
        "script": (
            "Hello everyone, and welcome to the live demonstration of our cybersecurity project: "
            "WHID-Guard, an ESP32-S3 Phone-Controlled USB HID Keyboard and Mouse platform with "
            "BadUSB Simulation and a Defensive Keystroke Firewall. Developed by Ram Karthik G and "
            "Harini V from the Department of Cybersecurity at Amrita Vishwa Vidyapeetham, Chennai. "
            "In this video, we will show you the physical hardware setup, live automated keystroke injection, "
            "wireless smartphone remote control, and our real-time behavioral host firewall actively defending "
            "against the attack."
        )
    },
    {
        "id": 2,
        "title": "Live Demo 1: Auto-Run Notepad Injection",
        "target_seconds": 40,
        "script": (
            "Let's begin with the live hardware demonstration. On the left, you see our Windows laptop desktop. "
            "When the ESP32-S3 is plugged in, its native USB-OTG controller on GPIO 19 and 20 enumerates instantly "
            "as a standard USB HID composite device without requiring any third-party drivers. Watch the screen closely: "
            "after a bounded 3.5-second stabilization wait, the ESP32 triggers Scenario 1. It automatically opens the "
            "Windows Run dialog, types notepad, and launches the editor. Notice how the microcontroller types our security "
            "awareness advisory character-by-character at high speed without anyone touching the laptop keyboard."
        )
    },
    {
        "id": 3,
        "title": "Live Demo 2: Phone UI & Physical Button Advancement",
        "target_seconds": 40,
        "script": (
            "Now look at the right pane, where our real smartphone controller is connected to the ESP32-S3 over Wi-Fi. "
            "The phone browser loads our dark-mode Single-Page Application served directly from the microcontroller's flash memory. "
            "In the Settings tab, we enter the security PIN and authenticate against the REST API. The top telemetry immediately "
            "confirms our session token. Next, watch what happens when I press the physical GPIO 0 BOOT button on the ESP32 board: "
            "the hardware edge-detector advances circularly through our payload sequences, cycling from Scenario 1 to 2, 3, and 4 "
            "with a 50-millisecond debounce filter."
        )
    },
    {
        "id": 4,
        "title": "Live Demo 3: Remote Scenario Execution & Emergency Stop",
        "target_seconds": 40,
        "script": (
            "From the phone's Scenarios tab, we can also launch any attack directly. Watch as I tap Scenario 4 on the phone. "
            "On the laptop, the Run dialog opens instantly, launches the Command Prompt, and runs netsh wlan show profiles, "
            "non-destructively enumerating all saved wireless networks. Next, I trigger Scenario 3: simulated ransomware. "
            "But watch this safety feature: while it is typing, I immediately tap the red Emergency Stop button on the phone! "
            "The firmware's non-blocking loop halts typing within 10 milliseconds and calls releaseAll on both keyboard and "
            "mouse buses, leaving zero keys stuck."
        )
    },
    {
        "id": 5,
        "title": "Live Demo 4: Wireless Keyboard & Multi-Touch Trackpad Mouse",
        "target_seconds": 40,
        "script": (
            "Beyond security payloads, the platform converts the smartphone into a complete driverless input peripheral. "
            "In the Keyboard tab, we have a full 6-row desktop keyboard with persistent hardware modifier latches, system shortcut macros, "
            "and a live text transmitter. On the laptop, I open a text file and type directly from the phone. Switching to the Mouse tab "
            "gives us a 60-hertz virtual trackpad. Moving a finger across the phone screen smoothly translates into 8-bit cursor movement "
            "on the laptop, supporting tap-to-click, drag-lock, and precision nudging."
        )
    },
    {
        "id": 6,
        "title": "Live Demo 5: Adversarial Evasion & Cadence Jitter",
        "target_seconds": 40,
        "script": (
            "Standard BadUSB tools type with robotic consistency, making them easy to catch with naive speed thresholds. "
            "In this demonstration, we test our firmware's Adversarial Stealth Mode. On the phone, I toggle the Adversarial Evasion switch. "
            "Notice how the typing cadence transforms: the firmware replaces rigid 10-millisecond delays with randomized stochastic jitter, "
            "and inserts cognitive pauses of 150 to 300 milliseconds after spaces and punctuation. This emulates authentic human thinking "
            "pauses, designed to stress-test host defensive classifiers."
        )
    },
    {
        "id": 7,
        "title": "Live Demo 6: WHID-Guard Host Defense in Action",
        "target_seconds": 45,
        "script": (
            "Now, let's observe our defensive solution: WHID-Guard. On the laptop, we launch our Python Keystroke Firewall. "
            "Look at the live telemetry card: using the Windows Raw Input API, it immediately attributes the active device handle to the "
            "ESP32-S3 with Vendor ID 303A. I click Toggle to arm the firewall. Now, I trigger a BadUSB payload from the phone. "
            "Watch the firewall: within just 8 characters—less than 85 milliseconds—the keystroke dynamics engine detects the near-zero "
            "variance, trips the anomaly threshold, and locks down the device! As you can see, zero characters reach Notepad. "
            "And most importantly, when I type on the laptop's built-in keyboard, it types perfectly! Only the malicious hardware handle "
            "is quarantined."
        )
    },
    {
        "id": 8,
        "title": "Quantitative Empirical Benchmark Evaluation",
        "target_seconds": 25,
        "script": (
            "We benchmarked WHID-Guard across 1,500 keystrokes. In human baseline testing, the system achieved a 0.0 percent False Positive Rate "
            "across 500 consecutive keystrokes. Against unconstrained BadUSB injection, it achieved a 98.6 percent True Positive Rate, "
            "quarantining the attack within 8 characters or 85 milliseconds. Against adversarial evasion, it flagged 25.2 percent of suspicious events."
        )
    },
    {
        "id": 9,
        "title": "Conclusion, IEEE Publication & Open-Source Release",
        "target_seconds": 15,
        "script": (
            "In conclusion, WHID-Guard successfully demonstrates the threat of hardware implants while introducing a practical, "
            "per-device behavioral defense. Our complete IEEE research paper and open-source codebase are available on GitHub. "
            "Thank you for your time and evaluation."
        )
    }
]

def get_audio_duration(file_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-i", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0

async def synthesize_all():
    os.makedirs("demo_video/audio_live", exist_ok=True)
    all_subtitles = []
    global_time = 0.0
    summary = []

    for item in SCENES:
        scene_id = item["id"]
        raw_mp3 = f"demo_video/audio_live/raw_scene_{scene_id}.mp3"
        print(f"[INFO] Synthesizing Live Demo Scene {scene_id}: {item['title']}...")
        
        c = edge_tts.Communicate(item["script"], VOICE, rate=RATE)
        sentences = []
        with open(raw_mp3, "wb") as f:
            async for chunk in c.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    start_sec = chunk["offset"] / 10_000_000.0
                    dur_sec = chunk["duration"] / 10_000_000.0
                    sentences.append({
                        "start": start_sec,
                        "end": start_sec + dur_sec,
                        "text": chunk["text"]
                    })
        
        raw_dur = get_audio_duration(raw_mp3)
        target_dur = round(raw_dur + 1.2, 1) # Natural pause before next scene
        pad_dur = 1.2
        
        final_mp3 = f"demo_video/audio_live/scene_{scene_id}.mp3"
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe, "-y", "-i", raw_mp3,
            "-af", f"apad=pad_dur={pad_dur:.2f}",
            "-t", f"{target_dur:.2f}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            final_mp3
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        final_dur = get_audio_duration(final_mp3)
        
        for s in sentences:
            all_subtitles.append({
                "scene_id": scene_id,
                "start": global_time + s["start"],
                "end": global_time + min(s["end"], raw_dur + 0.3),
                "text": s["text"]
            })
            
        summary.append({
            "id": scene_id,
            "title": item["title"],
            "raw_duration": raw_dur,
            "final_duration": final_dur,
            "start_time": global_time,
            "end_time": global_time + final_dur
        })
        global_time += final_dur
        print(f"       Scene {scene_id}: Raw={raw_dur:.2f}s -> Final={final_dur:.2f}s (Global: {global_time:.2f}s)")

    # Save subtitles to SRT format
    srt_path = "demo_video/subtitles_live.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, sub in enumerate(all_subtitles, 1):
            def fmt_time(secs):
                hrs = int(secs // 3600)
                mins = int((secs % 3600) // 60)
                scs = int(secs % 60)
                ms = int((secs - int(secs)) * 1000)
                return f"{hrs:02d}:{mins:02d}:{scs:02d},{ms:03d}"
            
            f.write(f"{idx}\n")
            f.write(f"{fmt_time(sub['start'])} --> {fmt_time(sub['end'])}\n")
            f.write(f"{sub['text']}\n\n")

    # Save summary metadata
    with open("demo_video/scenes_live_meta.json", "w", encoding="utf-8") as f:
        json.dump({"total_duration": global_time, "scenes": summary, "subtitles": all_subtitles}, f, indent=2)

    print(f"\n[SUCCESS] Total Audio Duration: {global_time:.2f} seconds ({global_time/60:.2f} minutes)")
    print(f"[SUCCESS] Subtitles saved to: {srt_path}")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
