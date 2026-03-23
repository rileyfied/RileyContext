#!/usr/bin/env python3
"""
RileyFile File Router
Automatically organizes files in RileyShare based on content and type

Files saved to RileyShare get:
1. Analyzed for content type and keywords
2. Auto-tagged with relevant #hashtags
3. Routed to appropriate subfolder or project

Notes from RileyNotes app should save directly to RileyNotes folder.
"""

import json
import os
import shutil
import re
from datetime import datetime
from pathlib import Path

# RileyContext base paths (local canonical root)
RILEYDOMAIN = Path.home() / 'dev' / 'RileyContext'
RILEYSHARE = RILEYDOMAIN / 'RileyShare'
RILEYNOTES = RILEYDOMAIN / 'RileyNotes'
RILEYPROJECTS = RILEYDOMAIN / 'RileyProjects'

# Project keyword mappings
PROJECT_KEYWORDS = {
    'ARMOR APP': ['armor', 'fighter verses', 'scripture', 'memorization', 'bible', 'verse'],
    'DASHBOARD APP': ['dashboard', 'productivity', 'command center', 'projects'],
    'YOUTUBE CHANNEL': ['youtube', 'video', 'content', 'ai tools', 'tutorial', 'channel'],
    'CFA TRAINING': ['cfa', 'chick-fil-a', 'restaurant', 'training', 'operations', 'leadership', 'chickfila'],
    'RILEY API': ['api', 'endpoint', 'backend', 'server'],
}

# File type categories
FILE_CATEGORIES = {
    'code': ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json', '.sh'],
    'document': ['.md', '.txt', '.rtf', '.doc', '.docx', '.pdf'],
    'image': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'],
    'data': ['.csv', '.xlsx', '.xls', '.json', '.xml'],
    'archive': ['.zip', '.tar', '.gz', '.rar'],
}

def extract_hashtags(text):
    """Extract existing hashtags from text content"""
    return re.findall(r'#[\w\-]+', text.lower())

def infer_tags_from_content(filename, content=None):
    """Infer hashtags from filename and content"""
    tags = set()
    name_lower = filename.lower()

    # Check for project keywords in filename
    for project, keywords in PROJECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                tags.add(f"#{keyword.replace(' ', '')}")

    # Add content-based tags if content provided
    if content:
        content_lower = content.lower()

        # AI-related
        if any(term in content_lower for term in ['chatgpt', 'claude', 'gemini', 'ai', 'llm', 'gpt']):
            tags.add('#ai')

        # Design-related
        if any(term in content_lower for term in ['design', 'figma', 'canva', 'ui', 'ux']):
            tags.add('#design')

        # Music-related
        if any(term in content_lower for term in ['piano', 'chord', 'music', 'harmony', 'scale']):
            tags.add('#music')

        # Video-related
        if any(term in content_lower for term in ['youtube', 'video', 'thumbnail', 'editing']):
            tags.add('#video')

        # Extract existing hashtags from content
        existing_tags = extract_hashtags(content)
        tags.update(existing_tags)

    return list(tags)

def get_file_category(filepath):
    """Determine file category based on extension"""
    ext = filepath.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'other'

def find_matching_project(filename, content=None):
    """Find which project a file belongs to based on keywords"""
    name_lower = filename.lower()
    text_to_search = name_lower + (content.lower() if content else '')

    for project, keywords in PROJECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_to_search:
                return project
    return None

def should_route_to_notes(filepath, content=None):
    """Determine if file should go to RileyNotes"""
    # Files with hashtags in content
    if content and extract_hashtags(content):
        return True

    # Short text files (likely quick notes)
    if filepath.suffix in ['.txt', '.md'] and content:
        word_count = len(content.split())
        if word_count < 200:  # Short notes
            return True

    return False

def read_text_file(filepath):
    """Safely read text content from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def route_file(filepath):
    """
    Route a single file to its appropriate destination
    Returns: (destination_path, tags, action_taken)
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return None, [], 'File not found'

    # Skip if already in a project folder or RileyNotes
    if RILEYPROJECTS in filepath.parents or RILEYNOTES in filepath.parents:
        return filepath, [], 'Already in correct location'

    # Read content for text files
    content = None
    if get_file_category(filepath) in ['document', 'code']:
        content = read_text_file(filepath)

    # Infer tags
    tags = infer_tags_from_content(filepath.name, content)

    # Decision tree
    destination = None
    action = 'No action'

    # Check if it should go to a specific project
    matching_project = find_matching_project(filepath.name, content)
    if matching_project:
        destination = RILEYPROJECTS / matching_project / filepath.name
        action = f'Routed to project: {matching_project}'

    # Check if it should go to RileyNotes
    elif should_route_to_notes(filepath, content):
        # Create timestamped filename for notes
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
        note_name = f"{timestamp}_{filepath.stem}.md"
        destination = RILEYNOTES / note_name
        action = 'Routed to RileyNotes'

    # Otherwise stays in RileyShare (no move needed)
    else:
        destination = filepath
        action = 'Kept in RileyShare'

    return destination, tags, action

def process_new_files_in_share():
    """Process all files in RileyShare root (not in captures)"""
    results = []

    for item in RILEYSHARE.iterdir():
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue

        destination, tags, action = route_file(item)

        # Only move if destination differs
        if destination and destination != item:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(destination))

        results.append({
            'file': item.name,
            'destination': str(destination) if destination else None,
            'tags': tags,
            'action': action
        })

    return results

def main():
    """Run the file router on RileyShare"""
    print(f"RileyFile File Router")
    print(f"Processing files in: {RILEYSHARE}")
    print("-" * 50)

    results = process_new_files_in_share()

    for result in results:
        print(f"\n{result['file']}")
        print(f"  Action: {result['action']}")
        if result['tags']:
            print(f"  Tags: {' '.join(result['tags'])}")

    print(f"\n{'=' * 50}")
    print(f"Processed {len(results)} files")

if __name__ == '__main__':
    main()
