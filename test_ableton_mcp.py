#!/usr/bin/env python3
"""
AbletonMCP Test Suite
Tests all implemented features to ensure they work correctly.
"""

import socket
import json
import time
import sys
from typing import Dict, Any, List

class AbletonMCPTester:
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def send_command(self, cmd_type: str, params: Dict = None) -> Dict[str, Any]:
        """Send a command to Ableton and get the response"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.host, self.port))
            
            command = {'type': cmd_type, 'params': params or {}}
            s.sendall(json.dumps(command).encode('utf-8'))
            
            # Receive response
            response = b''
            while True:
                chunk = s.recv(8192)
                if not chunk:
                    break
                response += chunk
                try:
                    result = json.loads(response.decode('utf-8'))
                    break
                except json.JSONDecodeError:
                    continue
            
            s.close()
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def test(self, name: str, command: str, params: Dict = None, 
             check_func=None, cleanup_func=None) -> bool:
        """Run a single test"""
        print(f"  Testing {name}... ", end='', flush=True)
        
        try:
            result = self.send_command(command, params)
            
            if result.get('status') == 'error':
                print(f"❌ FAILED")
                print(f"    Error: {result.get('message', 'Unknown error')}")
                self.tests_failed += 1
                self.test_results.append({'name': name, 'status': 'failed', 'error': result.get('message')})
                return False
            
            # Run custom check function if provided
            if check_func and not check_func(result):
                print(f"❌ FAILED")
                print(f"    Check function failed")
                self.tests_failed += 1
                self.test_results.append({'name': name, 'status': 'failed', 'error': 'Check function failed'})
                return False
            
            print(f"✅ PASSED")
            self.tests_passed += 1
            self.test_results.append({'name': name, 'status': 'passed'})
            
            # Run cleanup if provided
            if cleanup_func:
                cleanup_func(result)
            
            return True
            
        except Exception as e:
            print(f"❌ FAILED")
            print(f"    Exception: {str(e)}")
            self.tests_failed += 1
            self.test_results.append({'name': name, 'status': 'failed', 'error': str(e)})
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        print("\n🎹 AbletonMCP Test Suite")
        print("=" * 60)
        
        # Check connection first
        print("\n📡 Testing Connection...")
        if not self.test("Connection", "get_session_info"):
            print("\n❌ Cannot connect to Ableton. Make sure:")
            print("   1. Ableton Live is running")
            print("   2. AbletonMCP Remote Script is loaded")
            print("   3. The script is listening on port 9877")
            return
        
        # Store initial state
        initial_info = self.send_command("get_session_info")
        initial_track_count = initial_info.get('result', {}).get('track_count', 0)
        
        # Test Session Info
        print("\n📊 Testing Session Info...")
        self.test("Get session info", "get_session_info",
                 check_func=lambda r: 'tempo' in r.get('result', {}))
        self.test("Get song position", "get_song_position",
                 check_func=lambda r: 'current_time' in r.get('result', {}))
        
        # Test Transport
        print("\n▶️  Testing Transport...")
        self.test("Start playback", "start_playback")
        time.sleep(0.5)
        self.test("Stop playback", "stop_playback")
        self.test("Set tempo", "set_tempo", {"tempo": 124.0})
        
        # Test Track Management (HIGH PRIORITY)
        print("\n🎚️  Testing Track Management...")
        
        # Create MIDI track
        midi_result = None
        def store_midi_track(r):
            nonlocal midi_result
            midi_result = r
        
        self.test("Create MIDI track", "create_midi_track", {"index": -1},
                 check_func=lambda r: 'index' in r.get('result', {}),
                 cleanup_func=store_midi_track)
        
        midi_track_idx = midi_result.get('result', {}).get('index', 0) if midi_result else 0
        
        # Create audio track
        audio_result = None
        def store_audio_track(r):
            nonlocal audio_result
            audio_result = r
        
        self.test("Create audio track", "create_audio_track", {"index": -1},
                 check_func=lambda r: 'index' in r.get('result', {}),
                 cleanup_func=store_audio_track)
        
        audio_track_idx = audio_result.get('result', {}).get('index', 0) if audio_result else 1
        
        self.test("Set track name", "set_track_name", 
                 {"track_index": midi_track_idx, "name": "Test Track"})
        
        self.test("Get track info", "get_track_info", {"track_index": midi_track_idx},
                 check_func=lambda r: 'name' in r.get('result', {}))
        
        self.test("Set track volume", "set_track_volume", 
                 {"track_index": midi_track_idx, "volume": 0.7})
        
        self.test("Set track pan", "set_track_pan",
                 {"track_index": midi_track_idx, "pan": -0.2})
        
        self.test("Set track mute", "set_track_mute",
                 {"track_index": midi_track_idx, "mute": True})
        
        self.test("Set track solo", "set_track_solo",
                 {"track_index": midi_track_idx, "solo": False})
        
        self.test("Set track arm", "set_track_arm",
                 {"track_index": midi_track_idx, "arm": True})
        
        self.test("Get track routing", "get_track_routing",
                 {"track_index": midi_track_idx},
                 check_func=lambda r: 'input_routing_type' in r.get('result', {}))
        
        # Test if we can duplicate the MIDI track
        dup_result = None
        def store_dup_track(r):
            nonlocal dup_result
            dup_result = r
        
        self.test("Duplicate track", "duplicate_track", {"track_index": midi_track_idx},
                 check_func=lambda r: 'new_index' in r.get('result', {}),
                 cleanup_func=store_dup_track)
        
        dup_track_idx = dup_result.get('result', {}).get('new_index', 0) if dup_result else 0
        
        # Test Clip Management (HIGH PRIORITY)
        print("\n🎵 Testing Clip Management...")
        
        # Create a clip
        self.test("Create clip", "create_clip",
                 {"track_index": midi_track_idx, "clip_index": 0, "length": 4.0},
                 check_func=lambda r: 'name' in r.get('result', {}))
        
        # Add notes to clip
        test_notes = [
            {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100, "mute": False},
            {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 100, "mute": False},
            {"pitch": 67, "start_time": 2.0, "duration": 0.5, "velocity": 100, "mute": False},
        ]
        
        self.test("Add notes to clip", "add_notes_to_clip",
                 {"track_index": midi_track_idx, "clip_index": 0, "notes": test_notes},
                 check_func=lambda r: r.get('result', {}).get('note_count', 0) == 3)
        
        self.test("Get clip notes", "get_clip_notes",
                 {"track_index": midi_track_idx, "clip_index": 0},
                 check_func=lambda r: r.get('result', {}).get('note_count', 0) == 3)
        
        self.test("Set clip name", "set_clip_name",
                 {"track_index": midi_track_idx, "clip_index": 0, "name": "Test Clip"})
        
        self.test("Set clip loop", "set_clip_loop",
                 {"track_index": midi_track_idx, "clip_index": 0, 
                  "loop_start": 0.0, "loop_end": 4.0, "looping": True},
                 check_func=lambda r: r.get('result', {}).get('looping') == True)
        
        # Duplicate clip to slot 1
        self.test("Duplicate clip", "duplicate_clip",
                 {"track_index": midi_track_idx, "clip_index": 0,
                  "target_track_index": midi_track_idx, "target_clip_index": 1},
                 check_func=lambda r: r.get('result', {}).get('duplicated') == True)
        
        # Remove some notes
        self.test("Remove notes from clip", "remove_notes_from_clip",
                 {"track_index": midi_track_idx, "clip_index": 0,
                  "start_time": 0.0, "end_time": 1.0, "pitch_start": 0, "pitch_end": 128})
        
        # Replace notes
        new_notes = [
            {"pitch": 72, "start_time": 0.0, "duration": 1.0, "velocity": 110, "mute": False}
        ]
        self.test("Replace notes in clip", "replace_notes_in_clip",
                 {"track_index": midi_track_idx, "clip_index": 0, "notes": new_notes})
        
        # Test clip playback
        self.test("Fire clip", "fire_clip",
                 {"track_index": midi_track_idx, "clip_index": 0})
        time.sleep(0.3)
        self.test("Stop clip", "stop_clip",
                 {"track_index": midi_track_idx, "clip_index": 0})
        
        # Delete clip from slot 1
        self.test("Delete clip", "delete_clip",
                 {"track_index": midi_track_idx, "clip_index": 1})
        
        # Test Device Control (HIGH PRIORITY)
        print("\n🎛️  Testing Device Control...")
        
        # We need to load a device first - use a basic built-in instrument
        # Try to load Wavetable, which should exist in most Ableton installations
        self.test("Load instrument", "load_browser_item",
                 {"track_index": midi_track_idx, 
                  "item_uri": "query:Synths#Wavetable"})
        
        time.sleep(0.5)  # Give device time to load
        
        # Get track info to find device
        track_info = self.send_command("get_track_info", {"track_index": midi_track_idx})
        devices = track_info.get('result', {}).get('devices', [])
        
        if devices:
            device_idx = devices[0]['index']
            
            self.test("Get device parameters", "get_device_parameters",
                     {"track_index": midi_track_idx, "device_index": device_idx},
                     check_func=lambda r: 'parameters' in r.get('result', {}))
            
            # Get first parameter
            params_result = self.send_command("get_device_parameters", 
                                             {"track_index": midi_track_idx, "device_index": device_idx})
            params = params_result.get('result', {}).get('parameters', [])
            
            if len(params) > 1:  # Skip Device On parameter
                param_idx = params[1]['index']
                param_val = params[1].get('value', 0.5)
                
                self.test("Set device parameter", "set_device_parameter",
                         {"track_index": midi_track_idx, "device_index": device_idx,
                          "parameter_index": param_idx, "value": param_val + 0.1})
            
            self.test("Set device enabled", "set_device_enabled",
                     {"track_index": midi_track_idx, "device_index": device_idx, "enabled": False})
            
            self.test("Set device enabled (re-enable)", "set_device_enabled",
                     {"track_index": midi_track_idx, "device_index": device_idx, "enabled": True})
            
            self.test("Delete device", "delete_device",
                     {"track_index": midi_track_idx, "device_index": device_idx})
        
        # Test Scene Management
        print("\n🎬 Testing Scene Management...")
        
        self.test("Get scenes", "get_scenes",
                 check_func=lambda r: 'scenes' in r.get('result', {}))
        
        # Create a scene
        scene_result = None
        def store_scene(r):
            nonlocal scene_result
            scene_result = r
        
        self.test("Create scene", "create_scene", {"scene_index": -1},
                 check_func=lambda r: 'index' in r.get('result', {}),
                 cleanup_func=store_scene)
        
        scene_idx = scene_result.get('result', {}).get('index', 0) if scene_result else 0
        
        self.test("Set scene name", "set_scene_name",
                 {"scene_index": scene_idx, "name": "Test Scene"})
        
        self.test("Fire scene", "fire_scene", {"scene_index": 0})
        time.sleep(0.3)
        self.test("Stop all clips", "stop_all_clips")
        
        self.test("Duplicate scene", "duplicate_scene", {"scene_index": scene_idx})
        
        self.test("Delete scene", "delete_scene", {"scene_index": scene_idx + 1})
        self.test("Delete scene", "delete_scene", {"scene_index": scene_idx})
        
        # Test Master Track
        print("\n🎚️  Testing Master Track...")
        
        self.test("Get master track info", "get_master_track_info",
                 check_func=lambda r: 'name' in r.get('result', {}))
        
        self.test("Set master volume", "set_master_volume", {"volume": 0.8})
        
        # Test Return Tracks
        print("\n🔄 Testing Return Tracks...")
        
        self.test("Get return tracks", "get_return_tracks",
                 check_func=lambda r: 'returns' in r.get('result', {}))
        
        # Test sends (if we have return tracks)
        return_tracks = self.send_command("get_return_tracks")
        if return_tracks.get('result', {}).get('return_count', 0) > 0:
            self.test("Set track send", "set_track_send",
                     {"track_index": midi_track_idx, "send_index": 0, "value": 0.5})
        
        # Test Browser
        print("\n🔍 Testing Browser...")
        
        self.test("Get browser tree", "get_browser_tree",
                 check_func=lambda r: 'categories' in r.get('result', {}))
        
        self.test("Get browser items at path", "get_browser_items_at_path",
                 {"path": "audio_effects"},
                 check_func=lambda r: 'items' in r.get('result', {}))
        
        # Test Undo/Redo
        print("\n↩️  Testing Undo/Redo...")
        
        self.test("Undo", "undo")
        self.test("Redo", "redo")
        
        # Cleanup - Delete test tracks
        print("\n🧹 Cleanup...")
        
        # Get current track count
        current_info = self.send_command("get_session_info")
        current_track_count = current_info.get('result', {}).get('track_count', 0)
        
        # Delete tracks we created (work backwards to maintain indices)
        tracks_to_delete = current_track_count - initial_track_count
        for i in range(tracks_to_delete):
            track_idx = current_track_count - 1 - i
            self.test(f"Delete test track {track_idx}", "delete_track", 
                     {"track_index": track_idx})
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📋 Test Summary")
        print("=" * 60)
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"📊 Total:  {self.tests_passed + self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n🎉 All tests passed! AbletonMCP is working perfectly!")
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed. Check output above for details.")
            print("\nFailed tests:")
            for result in self.test_results:
                if result['status'] == 'failed':
                    print(f"  - {result['name']}: {result.get('error', 'Unknown error')}")
        
        coverage = (self.tests_passed / (self.tests_passed + self.tests_failed) * 100) if (self.tests_passed + self.tests_failed) > 0 else 0
        print(f"\n📈 Test Coverage: {coverage:.1f}%")
        print("=" * 60)

def main():
    """Main test runner"""
    print("\n🎹 AbletonMCP Test Suite")
    print("Make sure Ableton Live is running with AbletonMCP Remote Script loaded!\n")
    
    # Give user a moment to read
    time.sleep(1)
    
    tester = AbletonMCPTester()
    tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if tester.tests_failed == 0 else 1)

if __name__ == "__main__":
    main()
