"""
Antigravity History Exporter & Synchronizer
Exports all conversation history, transcripts, and artifacts from Antigravity IDE
into a human-readable and structured archive in this project directory.
"""

import os
import sys
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

# Paths
HOME_DIR = Path.home()
BRAIN_DIR = HOME_DIR / ".gemini" / "antigravity-ide" / "brain"
WORKSPACE_DIR = Path(__file__).resolve().parent
DEST_DIR = WORKSPACE_DIR / "antigravity_history"

def clean_user_request(text: str) -> str:
    """Extract clean text from <USER_REQUEST> tags."""
    if not text:
        return ""
    match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def parse_transcript(transcript_path: Path):
    """Parse transcript.jsonl into user-friendly conversation steps."""
    if not transcript_path.exists():
        return []
    
    steps = []
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except Exception:
                continue

            step_type = data.get("type", "")
            source = data.get("source", "")
            content = data.get("content", "")
            tool_calls = data.get("tool_calls", [])

            if step_type == "USER_INPUT" and source == "USER_EXPLICIT":
                user_msg = clean_user_request(content)
                if user_msg:
                    steps.append({"type": "user", "content": user_msg})
            
            elif step_type == "PLANNER_RESPONSE" and source == "MODEL":
                if content and content.strip():
                    steps.append({"type": "assistant", "content": content.strip()})
                if tool_calls:
                    for tc in tool_calls:
                        tool_name = tc.get("name") or tc.get("ToolName", "")
                        summary = tc.get("args", {}).get("toolSummary") or tc.get("args", {}).get("toolAction") or tool_name
                        steps.append({"type": "tool", "name": tool_name, "summary": summary, "args": tc.get("args", {})})
            
            elif step_type == "RUN_COMMAND" and source == "MODEL":
                cmd = data.get("args", {}).get("CommandLine", "")
                if cmd:
                    steps.append({"type": "command", "content": cmd})

    return steps

def process_conversations():
    if not BRAIN_DIR.exists():
        print(f"Error: Brain directory not found at {BRAIN_DIR}")
        return

    DEST_DIR.mkdir(exist_ok=True)

    conversations = []
    dir_entries = [d for d in BRAIN_DIR.iterdir() if d.is_dir() and d.name != "tempmediaStorage"]

    print(f"Found {len(dir_entries)} conversation folders. Processing...")

    for conv_dir in dir_entries:
        conv_id = conv_dir.name
        mod_time = datetime.fromtimestamp(conv_dir.stat().st_mtime)
        date_str = mod_time.strftime("%Y-%m-%d_%H-%M-%S")
        date_display = mod_time.strftime("%Y-%m-%d %H:%M:%S")

        # Find transcript
        logs_dir = conv_dir / ".system_generated" / "logs"
        transcript_file = logs_dir / "transcript.jsonl"
        if not transcript_file.exists():
            transcript_file = logs_dir / "transcript_full.jsonl"

        steps = []
        if transcript_file.exists():
            steps = parse_transcript(transcript_file)

        # Get first user query for title
        first_query = "Unknown Topic"
        for s in steps:
            if s["type"] == "user":
                first_query = s["content"].split("\n")[0][:80]
                break

        # Target conversation directory in project
        target_conv_dir = DEST_DIR / f"{date_str}_{conv_id[:8]}"
        target_conv_dir.mkdir(exist_ok=True)

        # Copy artifacts (.md files, diagrams, scratch)
        artifacts_copied = []
        for item in conv_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_file():
                dest_file = target_conv_dir / item.name
                if dest_file.exists() and dest_file.stat().st_size == item.stat().st_size:
                    artifacts_copied.append(item.name)
                    continue
                try:
                    shutil.copy2(item, dest_file)
                    artifacts_copied.append(item.name)
                except OSError as err:
                    # Ignore if disk space full on media files
                    pass
            elif item.is_dir() and item.name == "scratch":
                dest_scratch = target_conv_dir / "scratch"
                try:
                    shutil.copytree(item, dest_scratch, dirs_exist_ok=True)
                    artifacts_copied.append("scratch/")
                except OSError:
                    pass

        # Generate Conversation Markdown
        md_path = target_conv_dir / "conversation.md"
        with open(md_path, "w", encoding="utf-8") as md:
            md.write(f"# Conversation: {first_query}\n\n")
            md.write(f"- **ID:** `{conv_id}`\n")
            md.write(f"- **Date:** {date_display}\n")
            if artifacts_copied:
                md.write(f"- **Artifacts:** {', '.join(artifacts_copied)}\n")
            md.write("\n---\n\n")

            if not steps:
                md.write("*No recorded transcript steps found.*\n")

            for step in steps:
                stype = step["type"]
                if stype == "user":
                    md.write(f"### 👤 User\n\n{step['content']}\n\n")
                elif stype == "assistant":
                    md.write(f"### 🤖 Antigravity\n\n{step['content']}\n\n")
                elif stype == "tool":
                    name = step.get("name", "Tool")
                    summary = step.get("summary", "")
                    md.write(f"> ⚙️ **Action ({name}):** {summary}\n\n")
                elif stype == "command":
                    md.write(f"```powershell\n# Executed Command:\n{step['content']}\n```\n\n")

        # Save raw transcripts as backup too
        raw_logs_dir = target_conv_dir / "raw_logs"
        raw_logs_dir.mkdir(exist_ok=True)
        if transcript_file.exists():
            shutil.copy2(transcript_file, raw_logs_dir / transcript_file.name)

        conversations.append({
            "id": conv_id,
            "date": date_display,
            "date_sort": mod_time,
            "title": first_query,
            "folder": f"{date_str}_{conv_id[:8]}",
            "messages_count": len(steps)
        })

    # Sort descending by date
    conversations.sort(key=lambda x: x["date_sort"], reverse=True)

    # Write Master INDEX / README
    readme_path = DEST_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as rm:
        rm.write("# 📚 Antigravity History Archive\n\n")
        rm.write(f"Last synchronized: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n\n")
        rm.write("This folder contains all conversation transcripts, activities, commands, and artifacts executed by Antigravity.\n\n")
        rm.write("## 📋 Conversation Index\n\n")
        rm.write("| Date & Time | Topic / First Query | Messages | Link |\n")
        rm.write("| :--- | :--- | :--- | :--- |\n")
        for c in conversations:
            folder_link = f"[{c['folder']}](./{c['folder']}/conversation.md)"
            title_clean = c['title'].replace("|", "-").replace("\n", " ")
            rm.write(f"| {c['date']} | {title_clean} | {c['messages_count']} | {folder_link} |\n")

    print(f"\n[OK] Successfully synchronized {len(conversations)} conversations to:\n{DEST_DIR}")

if __name__ == "__main__":
    process_conversations()
