#!/usr/bin/env python3
"""
Arrangement Player for AbletonMCP

This script automatically fires scenes at specified bar positions
to create an arrangement while recording to Arrangement View.

Usage:
    python arrangement_player.py
"""

import socket
import json
import time
import sys

HOST = "localhost"
PORT = 9877

def send_command(cmd_type, params=None):
    """Send a command to Ableton and return the response"""
    s = socket.socket()
    s.settimeout(10)
    s.connect((HOST, PORT))
    s.sendall(json.dumps({'type': cmd_type, 'params': params or {}}).encode())
    chunks = []
    while True:
        try:
            chunk = s.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                result = json.loads(b''.join(chunks).decode())
                s.close()
                return result
            except json.JSONDecodeError:
                continue
        except socket.timeout:
            break
    s.close()
    return json.loads(b''.join(chunks).decode())


def get_position():
    """Get current song position"""
    result = send_command('get_song_position')
    return result.get('result', result)


def fire_scene(index):
    """Fire a scene"""
    result = send_command('fire_scene', {'scene_index': index})
    return result.get('result', result)


def start_playback():
    """Start playback"""
    return send_command('start_playback')


def stop_playback():
    """Stop playback"""
    return send_command('stop_playback')


def run_arrangement(arrangement):
    """
    Run an arrangement.
    
    arrangement: list of (bar_number, scene_index, name) tuples
    """
    print("\n🎵 ARRANGEMENT PLAYER")
    print("=" * 50)
    print("\nArrangement:")
    for bar, scene, name in arrangement:
        print(f"  Bar {bar:3d}: Scene {scene} - {name}")
    
    print("\n" + "=" * 50)
    input("\nPress ENTER to start (make sure Arrangement Recording is ON)...")
    
    # Sort by bar number
    arrangement = sorted(arrangement, key=lambda x: x[0])
    
    # Start playback
    print("\n▶️  Starting playback...")
    start_playback()
    time.sleep(0.5)
    
    # Fire first scene
    first_bar, first_scene, first_name = arrangement[0]
    print(f"\n🎬 Bar {first_bar}: Firing Scene {first_scene} - {first_name}")
    fire_scene(first_scene)
    
    # Track which scenes we've fired
    fired = {0}
    current_index = 1
    
    print("\n📍 Monitoring position...")
    
    try:
        while current_index < len(arrangement):
            pos = get_position()
            current_bar = pos.get('current_bar', 0)
            is_playing = pos.get('is_playing', False)
            
            if not is_playing:
                print("\n⏹️  Playback stopped. Exiting.")
                break
            
            # Check if we need to fire the next scene
            next_bar, next_scene, next_name = arrangement[current_index]
            
            if current_bar >= next_bar:
                print(f"\n🎬 Bar {current_bar}: Firing Scene {next_scene} - {next_name}")
                fire_scene(next_scene)
                current_index += 1
            
            # Show progress
            sys.stdout.write(f"\r   Bar: {current_bar}  ")
            sys.stdout.flush()
            
            time.sleep(0.1)  # Poll every 100ms
        
        print("\n\n✅ Arrangement complete!")
        print("   Stop recording in Ableton to save your arrangement.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user.")
        stop_playback()


# Define your arrangement here!
# Format: (bar_number, scene_index, section_name)

DETROIT_TECHNO_ARRANGEMENT = [
    (1,   4, "INTRO - Sparse"),
    (17,  0, "BUILD - Full drums"),
    (25,  1, "DROP 1 - Main groove"),
    (41,  2, "BREAKDOWN - Dubby"),
    (57,  3, "BUILD 2 - Rising"),
    (65,  1, "PEAK - Main groove"),
    (81,  2, "OUTRO - Breakdown"),
]


if __name__ == "__main__":
    print("\n🎹 AbletonMCP Arrangement Player")
    print("   Detroit Deep Techno Arrangement\n")
    
    try:
        # Test connection
        pos = get_position()
        print(f"✅ Connected to Ableton!")
        print(f"   Current position: Bar {pos.get('current_bar', '?')}")
        print(f"   Tempo: {pos.get('tempo', '?')} BPM")
        
        run_arrangement(DETROIT_TECHNO_ARRANGEMENT)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure Ableton is running with AbletonMCP control surface enabled.")
