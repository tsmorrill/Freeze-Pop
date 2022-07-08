# Freeze Pop
Generate MIDI files with tracker-inspired methods.

## Objects

### State Machines

A state machine is a function which is called without any input. These are analogous to function generators and sequencers in modular synthesis. They can be chained together to form more complicated structure, such as a sequential switch. The syntax is a little tricky; consult the examples on GitHub.

Most things in Freeze Pop can actually be state machines, so long as the given state machine outputs the correct kind of object when it is called, usually an integer from 0-127 inclusive. Many of the built-in state machines are based on mathematical systems, and output floating point numbers. The quantize state machine is very useful for working with these.

### Songs
A song is a list of tracks, which correspond to the tracks of a MIDI file.

### Tracks
A track is a list of sections.

### Sections
A section is a list of phrases. They are analogous to chains in most tracker programs.

### Phrases
A phrase is a list of notes.

### Notes
A note is a triple of the form (pitch, vel, freezer). Writing a single integer instead of a triple will generate the default vel and freezer options. Writing None generates a rest instead.

### Pitches

A pitch an integer from 0-127 inclusive. These correspond to the standard MIDI note values. Import convenient aliases for these values from frzpop.notes.

### Velocities
A velocity is an integer from 0-127 inclusive. These correspond to the standard MIDI note values. A velocity of zero will not generate any note events.

### Freezers
A freezer is description of how to process an abstract note into one or more note events in a MIDI file. Freezers are used similarly to commands in tracker programs.
