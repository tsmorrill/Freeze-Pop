# Freeze Pop
Generate MIDI files with tracker-inspired methods.

## Installation

Run
```
pip install frzpop
```
or run
```
pip install .
```
from inside the project directory.

## Objects

### Songs
A song is a list of tracks.

### Tracks
A track is a list of sections.

### Sections
A section is  a list of phrases.

### Phrases
A phrase is either a list of notes, or a function of the form
```
phrase(s)
```
which outputs a list of notes. Here, s is the index of the phrase in its section at the time it is frozen.

### Notes
A note is either an integer from 0-127 inclusive, a tuple of the form (pitch, vel, freezer), a function of the form
```
note(t)
```
which outputs a tuple of the form (pitch, vel, freezer). Here, t is the index of the note in its phrase at the time it is frozen. A note which is an integer is automatically converted into the tuple [pitch, 80, default_freezer].

### Pitches

A pitch either is an integer from 0-127 inclusive, or a function of the form
```
pitch(t)
```
which outputs an integer from 0-127 inclusive. Here, t is the index of the note in its phrase at the time it is frozen. These are handled according to the MIDI standard.

### Velocities
A velocity is either an integer from 0-127 inclusive, or a function of the form
```
vel(t)
```
which outputs an integer from 0-127 inclusive. Here, t is the index of the note in its phrase at the time it is frozen. These are handled according to the MIDI standard. In particular, notes with velocity zero are treated as rests.

### Freezers
A freezer is a function of the form
```
freezer(pitch, vel, time, s, t)
```
which outputs a tuple (ice_tray, time). Here, t is the index of the note in its phrase, and s is the index of the phrase in its section at the time they are frozen. Freezers are used similarly to commands in tracker programs.

### Ice Trays
An ice tray is a list of cubes.

### Cubes
A cube is a list of the form [pitch, time, note_len, vel]. They are used to place MIDI notes into a MIDI file.
