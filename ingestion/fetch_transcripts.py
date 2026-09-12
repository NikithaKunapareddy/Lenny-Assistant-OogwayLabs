import os
import json
import base64
import urllib.request
import time

TARGET_EPISODES = [
    "elena-verna",
    "brian-balfour",
    "casey-winters",
    "shreyas-doshi",
    "sean-ellis",
    "adam-fishman",
    "gibson-biddle",
    "hila-qu",
    "fareed-mosavat",
    "dan-hockenmaier",
    "madhavan-ramanujam",
    "ada-chen-rekhi",
    "ravi-mehta",
    "elizabeth-stone",
    "scott-belsky"
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "raw_transcripts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_episode(slug):
    out_file = os.path.join(OUTPUT_DIR, f"{slug}.md")
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        print(f"[-] Episode '{slug}' already exists ({os.path.getsize(out_file)} bytes). Skipping.")
        return True

    api_url = f"https://api.github.com/repos/ChatPRD/lennys-podcast-transcripts/contents/episodes/{slug}/transcript.md"
    print(f"[+] Fetching '{slug}' from GitHub API...")
    req = urllib.request.Request(
        api_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[+] Saved '{slug}' ({len(content)} chars)")
            return True
    except Exception as e:
        print(f"[!] Failed to fetch '{slug}': {e}")
        return False

def main():
    print(f"=== Starting Transcript Fetch for {len(TARGET_EPISODES)} Iconic Lenny Episodes ===")
    success = 0
    for slug in TARGET_EPISODES:
        if fetch_episode(slug):
            success += 1
        time.sleep(0.5) # Gentle on GitHub rate limits
    print(f"=== Successfully retrieved {success}/{len(TARGET_EPISODES)} episodes ===")

if __name__ == "__main__":
    main()
