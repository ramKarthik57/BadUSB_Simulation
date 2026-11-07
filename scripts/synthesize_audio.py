import asyncio
import edge_tts
import os
import subprocess
import imageio_ffmpeg
import json

VOICE = "en-US-ChristopherNeural"
RATE = "+8%" # Professional, confident presentation pace (~145 WPM)

SCENES = [
    {
        "id": 1,
        "title": "Introduction & Problem Statement",
        "target_seconds": 35,
        "script": (
            "Hello everyone, and welcome to our demonstration of WHID-Guard: an ESP32-S3 "
            "Phone-Controlled USB HID Keyboard and Mouse platform with BadUSB Simulation and a "
            "Defensive Keystroke Firewall. Developed by Ram Karthik G and Harini V from the Department "
            "of Cybersecurity at Amrita Vishwa Vidyapeetham, Chennai. Modern operating systems "
            "implicitly trust Human Interface Devices, allowing unauthorized hardware implants to inject "
            "destructive payloads at microsecond bus speeds without host consent. WHID-Guard provides "
            "an interruptible hardware emulation suite paired with an intelligent, per-device behavioral defense."
        )
    },
    {
        "id": 2,
        "title": "Hardware Architecture & Dual-Port Topology",
        "target_seconds": 35,
        "script": (
            "The system is powered by the ESP32-S3 dual-core microcontroller running at 240 megahertz "
            "with native USB-OTG full-speed hardware directly on GPIO 19 and 20. Our custom dual-port "
            "topology cleanly isolates attack vectors from developer controls. The primary USB-OTG port "
            "connects to the target laptop, enumerating immediately as a standard driverless composite HID "
            "keyboard and multi-button mouse. Concurrently, the CP210x UART bridge on Port 1 provides "
            "isolated serial telemetry and firmware flashing on COM5, ensuring continuous laboratory monitoring "
            "without disrupting the target host's USB bus."
        )
    },
    {
        "id": 3,
        "title": "Deterministic Finite State Machine & Payloads",
        "target_seconds": 35,
        "script": (
            "Inside the firmware, an 8-state deterministic Finite State Machine governs scenario lifecycles. "
            "Upon initial connection, it enforces a bounded 3.5-second wait for host USB enumeration to stabilize, "
            "and then automatically executes Scenario 1: an educational Notepad security awareness notification. "
            "The platform includes four demonstration scenarios: Notepad awareness, institutional portal redirection, "
            "simulated PowerShell ransomware alerts, and Wi-Fi profile reconnaissance. Scenarios can also be advanced "
            "offline using the physical GPIO 0 BOOT button, which employs a 50-millisecond hardware debounce filter."
        )
    },
    {
        "id": 4,
        "title": "Mobile Web Controller & Remote Peripheral Suite",
        "target_seconds": 35,
        "script": (
            "Concurrently, the ESP32-S3 broadcasts a 2.4 gigahertz Wi-Fi network, hosting a responsive dark-mode "
            "Single-Page Application served entirely from PROGMEM flash memory. Users authenticate against our REST API "
            "using a secure PIN, which issues tokenized credentials. The interface features one-touch scenario execution "
            "with live status polling, a complete 6-row QWERTY keyboard with latched modifiers and system shortcuts, "
            "a 256-character bulk text transmitter, and a 60-hertz virtual trackpad mouse with relative motion clamping "
            "and precision drag-lock controls."
        )
    },
    {
        "id": 5,
        "title": "Adversarial Resilience & Human Cadence Emulation",
        "target_seconds": 35,
        "script": (
            "Standard BadUSB tools inject keystrokes at rigid 10-millisecond intervals, making them trivial to block "
            "with rudimentary speed limiters. To rigorously test defensive resilience, we implemented an adversarial "
            "stealth mode in the ESP32-S3 firmware. When toggled from the mobile interface, the controller replaces "
            "deterministic timing with stochastic jitter and automatically injects cognitive micro-pauses of 150 to "
            "300 milliseconds following whitespace and punctuation marks, mimicking the natural neuromuscular delays "
            "of human operators."
        )
    },
    {
        "id": 6,
        "title": "WHID-Guard Behavioral Keystroke Dynamics Engine",
        "target_seconds": 40,
        "script": (
            "To counter these sophisticated threats, we developed the WHID-Guard host defense engine. Rather than "
            "relying on simplistic rate limits, WHID-Guard computes behavioral keystroke dynamics over an online sliding "
            "window of ten events. It continuously calculates the mean Inter-Key Interval, standard deviation, coefficient "
            "of variation, and burst typing rate. While human typing exhibits natural cognitive variance with a coefficient "
            "of variation exceeding 0.30, unconstrained BadUSB injection demonstrates rigid consistency below 0.15, "
            "enabling precise algorithmic classification without false alarms."
        )
    },
    {
        "id": 7,
        "title": "Per-Device Hardware Attribution & Selective Isolation",
        "target_seconds": 40,
        "script": (
            "Traditional security tools install global keyboard hooks that lock out all typing indiscriminately. "
            "WHID-Guard solves this problem through per-device hardware attribution via the Windows Raw Input API. "
            "By registering for raw input message sinks and querying device names, our engine extracts the physical "
            "hardware device handle and USB Vendor and Product IDs. When an injection attack is detected, our low-level "
            "keyboard hook drops only the malicious hardware packets, keeping the user's legitimate laptop keyboard "
            "completely active and responsive."
        )
    },
    {
        "id": 8,
        "title": "Quantitative Empirical Evaluation & Benchmark Results",
        "target_seconds": 30,
        "script": (
            "We conducted an extensive empirical evaluation across a 1,500-keystroke benchmark corpus. On human baseline "
            "typing, WHID-Guard achieved a 0.0 percent False Positive Rate across 500 consecutive keystrokes. "
            "Against unconstrained BadUSB attacks, the system achieved a 98.6 percent True Positive Detection Rate, "
            "quarantining the offending implant within exactly 8 characters—less than 85 milliseconds of total execution time. "
            "Against stealth cadence emulation, it successfully flagged 25.2 percent of suspicious events."
        )
    },
    {
        "id": 9,
        "title": "Conclusion, IEEE Publication & Open-Source Release",
        "target_seconds": 15,
        "script": (
            "In conclusion, WHID-Guard bridges offensive hardware exploration and host-level defensive resilience. "
            "Our complete research manuscript and reproducible codebase are open-sourced on GitHub. Thank you for "
            "your evaluation of our project."
        )
    }
]

def get_audio_duration(file_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-i", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 00:00:32.45, start: ...
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0

async def synthesize_all():
    os.makedirs("demo_video/audio", exist_ok=True)
    all_subtitles = []
    global_time = 0.0
    summary = []

    for item in SCENES:
        scene_id = item["id"]
        raw_mp3 = f"demo_video/audio/raw_scene_{scene_id}.mp3"
        print(f"[INFO] Synthesizing Scene {scene_id}: {item['title']}...")
        
        c = edge_tts.Communicate(item["script"], VOICE, rate=RATE)
        sentences = []
        with open(raw_mp3, "wb") as f:
            async for chunk in c.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    # offset & duration in 100ns ticks
                    start_sec = chunk["offset"] / 10_000_000.0
                    dur_sec = chunk["duration"] / 10_000_000.0
                    sentences.append({
                        "start": start_sec,
                        "end": start_sec + dur_sec,
                        "text": chunk["text"]
                    })
        
        raw_dur = get_audio_duration(raw_mp3)
        target_dur = round(raw_dur + 1.0, 1)
        pad_dur = 1.0
        
        # Pad with silence at the end using ffmpeg apad filter
        final_mp3 = f"demo_video/audio/scene_{scene_id}.mp3"
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
        
        # Build global subtitles
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
    srt_path = "demo_video/subtitles.srt"
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
    with open("demo_video/scenes_meta.json", "w", encoding="utf-8") as f:
        json.dump({"total_duration": global_time, "scenes": summary, "subtitles": all_subtitles}, f, indent=2)

    print(f"\n[SUCCESS] Total Audio Duration: {global_time:.2f} seconds ({global_time/60:.2f} minutes)")
    print(f"[SUCCESS] Subtitles saved to: {srt_path}")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
