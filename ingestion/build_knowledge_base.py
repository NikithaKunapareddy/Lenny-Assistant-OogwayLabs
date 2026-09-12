import os
import re
import json
import pickle
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS_DIR = os.path.join(SCRIPT_DIR, "raw_transcripts")
OUTPUT_JSON = os.path.join(SCRIPT_DIR, "..", "backend", "app", "rag", "lenny_knowledge_base.json")
OUTPUT_INDEX = os.path.join(SCRIPT_DIR, "..", "backend", "app", "rag", "tfidf_index.pkl")

os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

def parse_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except Exception as e:
                print(f"Error parsing YAML: {e}")
            body = parts[2]
    return meta, body

def clean_text(text):
    # Remove excessive blank lines and clean up whitespace
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_transcript(slug, meta, body, target_words=350, overlap_words=50):
    lines = body.split("\n")
    guest = meta.get("guest", slug.replace("-", " ").title())
    title = meta.get("title", f"Episode with {guest}")
    youtube_url = meta.get("youtube_url", "")
    keywords = meta.get("keywords", [])
    if isinstance(keywords, list):
        keywords_str = ", ".join(str(k) for k in keywords)
    else:
        keywords_str = str(keywords)

    dialogue_turns = []
    current_speaker = "Lenny Rachitsky"
    current_time = "00:00:00"
    current_text = []

    turn_pattern = re.compile(r'^([A-Za-z\s\.\'\-]+)\s*\(([0-9\:]+)\):\s*(.*)$')

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        m = turn_pattern.match(line_clean)
        if m:
            if current_text:
                dialogue_turns.append({
                    "speaker": current_speaker,
                    "timestamp": current_time,
                    "text": " ".join(current_text)
                })
                current_text = []
            current_speaker = m.group(1).strip()
            current_time = m.group(2).strip()
            if m.group(3).strip():
                current_text.append(m.group(3).strip())
        else:
            if not line_clean.startswith("#"):
                current_text.append(line_clean)

    if current_text:
        dialogue_turns.append({
            "speaker": current_speaker,
            "timestamp": current_time,
            "text": " ".join(current_text)
        })

    # If dialogue turn parsing yielded very few items, fall back to paragraph grouping
    if len(dialogue_turns) < 3:
        paragraphs = [p.strip() for p in body.split("\n\n") if len(p.strip()) > 30 and not p.strip().startswith("#")]
        dialogue_turns = [{"speaker": guest, "timestamp": "00:00:00", "text": p} for p in paragraphs]

    chunks = []
    chunk_index = 1
    i = 0
    while i < len(dialogue_turns):
        acc_turns = []
        word_count = 0
        start_time = dialogue_turns[i]["timestamp"]
        primary_speaker = dialogue_turns[i]["speaker"]
        j = i

        while j < len(dialogue_turns) and word_count < target_words:
            t = dialogue_turns[j]
            turn_str = f"{t['speaker']} ({t['timestamp']}): {t['text']}"
            acc_turns.append(turn_str)
            word_count += len(turn_str.split())
            j += 1

        chunk_text = "\n\n".join(acc_turns)
        chunk_id = f"{slug}-chunk-{chunk_index:03d}"

        chunks.append({
            "id": chunk_id,
            "episode_slug": slug,
            "guest": guest,
            "title": title,
            "youtube_url": youtube_url,
            "keywords": keywords_str,
            "timestamp": start_time,
            "primary_speaker": primary_speaker,
            "content": chunk_text,
            "word_count": word_count
        })
        chunk_index += 1

        # Advance with overlap
        # Calculate how many turns to step forward
        advance = max(1, j - i - 1)
        i += advance

    return chunks

def main():
    print("=== Building Lenny Knowledge Base from Transcripts ===")
    all_chunks = []
    files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".md")]
    print(f"Found {len(files)} transcript files.")

    for f in files:
        slug = f.replace(".md", "")
        file_path = os.path.join(TRANSCRIPTS_DIR, f)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
            raw = fp.read()
        meta, body = parse_frontmatter(raw)
        chunks = chunk_transcript(slug, meta, body)
        all_chunks.extend(chunks)
        print(f"[-] Processed '{slug}': generated {len(chunks)} chunks.")

    print(f"\nTotal Knowledge Base Chunks: {len(all_chunks)}")

    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
        json.dump(all_chunks, out, indent=2, ensure_ascii=False)
    print(f"[+] Saved chunk database to: {OUTPUT_JSON}")

    # Build TF-IDF search index
    print("[*] Vectorizing corpus with TF-IDF (unigram + bigram)...")
    corpus = [
        f"{c['guest']} {c['title']} {c['keywords']} {c['content']}"
        for c in all_chunks
    ]
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=25000,
        sublinear_tf=True
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    with open(OUTPUT_INDEX, "wb") as idx_file:
        pickle.dump({
            "vectorizer": vectorizer,
            "matrix": tfidf_matrix,
            "chunk_ids": [c["id"] for c in all_chunks]
        }, idx_file)
    print(f"[+] Saved TF-IDF retrieval index to: {OUTPUT_INDEX}")
    print("=== Knowledge Base Ingestion Complete ===")

if __name__ == "__main__":
    main()
