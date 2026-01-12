# AbletonMCP Feature Roadmap

This document tracks the implementation status and planned features for AbletonMCP to achieve maximum agentic control over Ableton Live.

## Current Coverage: ~40%

---

## ✅ Implemented Features

### Tracks
- ✅ Create MIDI tracks
- ✅ Set track name
- ✅ Set track volume
- ✅ Set track pan
- ✅ Mute/unmute tracks
- ✅ Solo/unsolo tracks
- ✅ Set track sends
- ✅ Get track info

### Clips & MIDI
- ✅ Create MIDI clips
- ✅ Add notes to clips
- ✅ Set clip name
- ✅ Fire/stop clips

### Devices & Effects
- ✅ Load instruments/effects on tracks
- ✅ Load effects on master track
- ✅ Load effects on return tracks
- ✅ Get device parameters (all knobs/values)
- ✅ Set device parameters (control any knob)
- ✅ Get return track info

### Transport & Playback
- ✅ Start/stop playback
- ✅ Set tempo
- ✅ Get song position (beats)
- ✅ Timed scene triggering (arrangement playback)

### Scenes
- ✅ Get scenes
- ✅ Fire scene
- ✅ Stop all clips
- ✅ Create scene
- ✅ Duplicate scene
- ✅ Delete scene
- ✅ Set scene name

### Browser
- ✅ Get browser tree (hierarchical)
- ✅ Get browser items at path
- ✅ Load instruments/effects by URI

### Session
- ✅ Get session info
- ✅ Get master track info
- ✅ Set master volume
- ✅ Capture MIDI
- ✅ Undo/redo

---

## 🔴 Missing Features

### HIGH PRIORITY - Core Mixing/Arranging (~40% coverage gain)

#### Track Management
- [ ] **Create audio tracks** - Essential for recording/importing audio
  - Implementation: Similar to `create_midi_track`, use different track type
- [ ] **Delete tracks** - Clean up, remove unwanted tracks
  - Implementation: `song.delete_track(track_index)`
- [ ] **Duplicate tracks** - Fast workflow for similar instruments
  - Implementation: `song.duplicate_track(track_index)`
- [ ] **Move/reorder tracks** - Organization
  - Implementation: Complex, may need to handle routing/sends

#### Clip Management
- [ ] **Get clip notes** - Read existing MIDI patterns for modification
  - Implementation: `clip.get_notes(start, end, pitch)` - returns note list
  - Critical for: Modifying existing patterns, analysis, transposition
- [ ] **Remove notes from clip** - Edit/fix patterns
  - Implementation: `clip.remove_notes(start, end, pitch)`
- [ ] **Replace notes in clip** - Full editing capability
  - Implementation: `clip.set_notes(notes_tuple)`
- [ ] **Delete clips** - Remove unwanted clips
  - Implementation: `clip_slot.delete_clip()`
- [ ] **Duplicate clips** - Quickly create variations
  - Implementation: `clip_slot.duplicate_clip_to(target_slot)`
- [ ] **Get clip length** - Query loop/clip properties
  - Implementation: `clip.length`, `clip.loop_start`, `clip.loop_end`
- [ ] **Set clip loop points** - Control loop behavior
  - Implementation: Set `clip.loop_start`, `clip.loop_end`, `clip.looping`

#### Device Control
- [ ] **Enable/disable devices** - Bypass effects for A/B comparison
  - Implementation: `device.is_active = True/False`
  - Critical for: Mixing workflow, CPU management
- [ ] **Delete devices** - Remove effects
  - Implementation: `track.delete_device(device_index)`
- [ ] **Reorder devices** - Change signal chain
  - Implementation: Complex, may need custom logic

#### Recording
- [ ] **Arm tracks for recording** - Enable MIDI/audio recording
  - Implementation: `track.arm = True/False`
- [ ] **Get/set track input routing** - Select input source
  - Implementation: `track.input_routing_type`, `track.input_routing_channel`
- [ ] **Get/set track output routing** - Route to external/other tracks
  - Implementation: `track.output_routing_type`, `track.output_routing_channel`

---

### MEDIUM PRIORITY - Workflow Enhancement (~20% coverage gain)

#### Visual Organization
- [ ] **Set track color** - Visual organization
  - Implementation: `track.color` (RGB value 0-127 per channel)
- [ ] **Set clip color** - Visual organization
  - Implementation: `clip.color` (RGB value)
- [ ] **Track grouping (create groups)** - Bus processing
  - Implementation: Create group track, move tracks into it

#### Session Settings
- [ ] **Get/set time signature** - Support non-4/4 music
  - Implementation: `song.signature_numerator`, `song.signature_denominator`
- [ ] **Metronome on/off** - Recording workflow
  - Implementation: `song.metronome = True/False`
- [ ] **Set quantization** - Recording/editing workflow
  - Implementation: `song.clip_trigger_quantization`
- [ ] **Set record quantization** - MIDI recording workflow
  - Implementation: `song.midi_recording_quantization`

#### Arrangement View
- [ ] **Switch to Arrangement View** - Navigate views
  - Implementation: `application.view.show_view("Arranger")`
- [ ] **Get arrangement time** - Query arrangement position
  - Implementation: `song.current_song_time`
- [ ] **Set arrangement time** - Jump to position
  - Implementation: `song.current_song_time = time`
- [ ] **Set arrangement loop** - Loop sections
  - Implementation: `song.loop`, `song.loop_start`, `song.loop_length`
- [ ] **Create locators** - Arrangement markers
  - Implementation: Limited API support, may need workarounds

#### Automation
- [ ] **Get automation envelope** - Read existing automation
  - Implementation: `parameter.automation_envelope`
- [ ] **Add automation points** - Write automation
  - Implementation: `envelope.insert_step(time, value)`
- [ ] **Clear automation** - Reset automation
  - Implementation: `envelope.clear_all()`

---

### ADVANCED PRIORITY - Full Production Power (~15% coverage gain)

#### Audio Export
- [ ] **Export/render audio** - Bounce final mix or stems
  - Implementation: Complex, may need to trigger Ableton's export dialog
  - Alternative: Use command-line rendering if available

#### CPU Management
- [ ] **Freeze tracks** - Reduce CPU load
  - Implementation: `track.freeze()` (if available in API)
- [ ] **Flatten tracks** - Consolidate frozen audio
  - Implementation: May need workarounds
- [ ] **Get track current output peak** - Metering
  - Implementation: `track.output_meter_level` (left/right)

#### Audio Manipulation
- [ ] **Warp markers** - Time-stretch control
  - Implementation: Limited API, `clip.warp_markers`
- [ ] **Set warp mode** - Choose warping algorithm
  - Implementation: `clip.warp_mode`
- [ ] **Consolidate clips** - Bounce in place
  - Implementation: Complex, may need workarounds

#### Sample/Instrument Control
- [ ] **Load sample into Simpler/Sampler** - Direct sample loading
  - Implementation: Device-specific parameter setting
- [ ] **Set sample zones** - Multi-sample instruments
  - Implementation: Very device-specific
- [ ] **Slice to MIDI** - Chop samples automatically
  - Implementation: Complex, may need trigger via menu

#### Session Management
- [ ] **Save project** - Save current state
  - Implementation: `song.save_as(path)` or `song.save()`
- [ ] **Create new project** - Fresh start
  - Implementation: `application.create_document()`
- [ ] **Get/set project tempo range** - Min/max tempo
  - Implementation: May not be exposed in API

#### Advanced Routing
- [ ] **Sidechain routing** - Sidechain compression setup
  - Implementation: Complex audio routing, device-specific
- [ ] **External instrument/effect** - Hardware integration
  - Implementation: Create External Instrument/Effect devices

---

### DREAM FEATURES - Complex/Experimental (~5% coverage gain)

#### Audio Analysis
- [ ] **Audio-to-MIDI conversion** - Analyze and recreate patterns
  - Implementation: May require external analysis, not in API
- [ ] **Get LUFS/RMS metering** - Loudness analysis
  - Implementation: Not directly in API, may need external metering

#### Groove & Feel
- [ ] **Access groove pool** - Apply swing/feel
  - Implementation: `song.groove_pool`
- [ ] **Set clip groove** - Apply groove to clip
  - Implementation: `clip.groove`

#### Advanced Clip Operations
- [ ] **Quantize notes in clip** - Clean up MIDI timing
  - Implementation: `clip.quantize(quantization)`
- [ ] **Transpose clip** - Pitch shift MIDI
  - Implementation: Manual note manipulation required

#### Max for Live Integration
- [ ] **Control Max for Live devices** - Advanced parameter access
  - Implementation: M4L devices may have custom parameter structures

---

## Implementation Priority Plan

### Phase 1: Essential Clip Editing (Week 1)
Focus: Read/write/edit existing clips
- Get clip notes
- Remove/replace notes
- Delete clips
- Duplicate clips
- Set clip loop points

**Impact**: Enables full MIDI pattern manipulation and arrangement editing

### Phase 2: Track Management (Week 2)
Focus: Full track control
- Create audio tracks
- Delete tracks
- Duplicate tracks
- Device enable/disable
- Track arming

**Impact**: Complete track lifecycle management, recording capability

### Phase 3: Workflow Enhancement (Week 3)
Focus: Professional workflow features
- Time signature control
- Track colors
- Metronome control
- Quantization settings
- Track input/output routing

**Impact**: Proper music production workflow support

### Phase 4: Advanced Features (Week 4+)
Focus: Power user features
- Automation control
- Export/render
- Peak metering
- Arrangement view control
- Session management

**Impact**: Professional-grade production capabilities

---

## Technical Notes

### Known API Limitations
- Some features may not be exposed in Live Object Model (LOM)
- Export/render may require triggering Ableton's internal dialogs
- Warp markers have limited API access
- Peak metering is available but may be resource-intensive to poll
- Max for Live devices have varying parameter structures

### Performance Considerations
- Batch operations should be preferred for bulk edits
- Real-time metering should be optional/on-demand
- Large clip note operations may need chunking

### Testing Requirements
- Each feature needs test cases for both MCP server and Remote Script
- Integration tests for complex workflows
- Performance tests for real-time operations

---

## Contributing

When implementing features from this roadmap:
1. Update both `AbletonMCP_Remote_Script/__init__.py` and `MCP_Server/server.py`
2. Add comprehensive error handling
3. Document parameter ranges and constraints
4. Update this file to mark features as complete
5. Add examples to README.md

---

*Last Updated: 2026-01-12*
*Coverage Target: 100% of practical Ableton Live API*
