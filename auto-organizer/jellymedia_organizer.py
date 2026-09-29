#!/usr/bin/env python
import os
import time
import subprocess

ROOT = "/storage/emulated/0/JellyMedia"
CHECK_EVERY = 30
STABLE_FOR = 120

video_ext = (".mkv", ".mp4", ".avi", ".mov", ".webm")
seen = {}

def is_root_video(path):
    return (
        os.path.isfile(path)
        and path.lower().endswith(video_ext)
        and os.path.dirname(path.rstrip("/")) == ROOT
    )

def organize():
    try:
        result = subprocess.run(
            ["jellymedia", "organize"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=300
        )
        output = result.stdout.strip()
        if output:
            print(output, flush=True)
    except Exception as e:
        print("Organizer error:", e, flush=True)

print("JellyMedia Auto Organizer started", flush=True)
print("Watching:", ROOT, flush=True)

while True:
    try:
        now = time.time()

        for name in os.listdir(ROOT):
            path = os.path.join(ROOT, name)

            if not is_root_video(path):
                continue

            try:
                size = os.path.getsize(path)
                mtime = os.path.getmtime(path)
            except OSError:
                continue

            old = seen.get(path)

            if old is None:
                seen[path] = {
                    "size": size,
                    "mtime": mtime,
                    "stable_since": now
                }
                print("Detected:", name, flush=True)
                continue

            if old["size"] != size or old["mtime"] != mtime:
                old["size"] = size
                old["mtime"] = mtime
                old["stable_since"] = now
                continue

            if now - old["stable_since"] >= STABLE_FOR:
                print("Stable file, organizing:", name, flush=True)
                organize()
                seen.pop(path, None)

        # Remove entries for files that disappeared/moved
        for path in list(seen):
            if not os.path.exists(path):
                seen.pop(path, None)

    except Exception as e:
        print("Watcher error:", e, flush=True)

    time.sleep(CHECK_EVERY)
