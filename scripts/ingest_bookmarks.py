#!/usr/bin/env python3
"""
Safari Bookmarks Ingestion Script for RileyFile
Parses Safari bookmarks export and converts to capture format
"""

import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self.current_folders = []
        self.current_bookmark = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            self.in_title = True
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            self.current_bookmark = {'url': href, 'title': '', 'folders': list(self.current_folders)}
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_title = False
        elif tag == 'a':
            if self.current_bookmark:
                self.bookmarks.append(self.current_bookmark)
                self.current_bookmark = None
            self.in_title = False
        elif tag == 'dl':
            if self.current_folders:
                self.current_folders.pop()

    def handle_data(self, data):
        if self.in_title:
            data = data.strip()
            if data:
                if self.current_bookmark:
                    self.current_bookmark['title'] = data
                else:
                    self.current_folders.append(data)

def infer_tags_from_bookmark(bookmark):
    """Infer hashtags based on URL and folder path"""
    tags = set()
    url = bookmark['url'].lower()
    title = bookmark['title'].lower()
    folders = [f.lower() for f in bookmark['folders']]

    # Project tags based on folders
    folder_to_tag = {
        'cfa': '#cfa',
        'piano': '#piano',
        'boombox': '#boombox',
        'graphic design': '#design',
        'house': '#house',
        'coursera': '#learning',
        'working apps': '#tools',
    }

    for folder in folders:
        for key, tag in folder_to_tag.items():
            if key in folder:
                tags.add(tag)

    # Domain-based tags
    if 'youtube' in url:
        tags.add('#video')
    if 'github' in url:
        tags.add('#code')
    if 'claude.ai' in url or 'chatgpt' in url or 'gemini' in url:
        tags.add('#ai')
    if 'reddit' in url:
        tags.add('#reddit')
    if 'medium' in url or 'substack' in url:
        tags.add('#article')
    if 'docs.google' in url or 'notion' in url:
        tags.add('#doc')

    # Content-based tags
    if 'piano' in title or 'chord' in title or 'music' in title:
        tags.add('#piano')
    if 'ai' in title or 'gpt' in title or 'claude' in title:
        tags.add('#ai')
    if 'resume' in title or 'job' in title or 'career' in title:
        tags.add('#career')
    if 'design' in title or 'figma' in title or 'canva' in title:
        tags.add('#design')

    return list(tags)

def convert_to_capture(bookmark):
    """Convert a bookmark to RileyFile capture format"""
    tags = infer_tags_from_bookmark(bookmark)
    folder_path = ' > '.join(bookmark['folders']) if bookmark['folders'] else 'Uncategorized'

    content = f"{bookmark['title']}\n{bookmark['url']}"
    if tags:
        content += f"\n\n{' '.join(tags)}"

    return {
        'id': f"bm_{hash(bookmark['url']) & 0xffffffff:08x}",
        'content': content,
        'tags': tags,
        'urls': [bookmark['url']],
        'created': datetime.now().isoformat(),
        'updated': datetime.now().isoformat(),
        'source': 'safari_bookmarks',
        'source_folder': folder_path,
        'original_title': bookmark['title']
    }

def main():
    # Paths - Updated for RileyFile structure
    bookmarks_path = Path.home() / 'dev' / 'RileyContext' / 'RileyProjects' / 'Safari Export 2026-01-22' / 'Bookmarks.html'
    output_path = Path.home() / 'dev' / 'RileyContext' / 'RileyShare' / 'captures' / 'safari_bookmarks.json'

    # Parse bookmarks
    with open(bookmarks_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = BookmarkParser()
    parser.feed(html_content)

    # Convert to captures
    captures = []
    for bookmark in parser.bookmarks:
        if bookmark['url'] and bookmark['title']:
            capture = convert_to_capture(bookmark)
            captures.append(capture)

    # Write output
    output = {
        'source': 'safari_bookmarks',
        'imported': datetime.now().isoformat(),
        'count': len(captures),
        'captures': captures
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Imported {len(captures)} bookmarks to RileyContext/RileyShare/captures")

if __name__ == '__main__':
    main()
