#!/usr/bin/python

from midiutil.MidiFile import MIDIFile
from midigen import guido


def main():
    lyric = input("Enter lyric : ")
    if lyric == "":
        print("Substituting pangram for empty string")
        lyric = "Sphinx of black quartz, judge my vow."
    note_list = guido.guido(lyric)

    track = 0
    time = 0
    channel = 0
    volume = 127
    duration = 1

    partition = lyric[8::-1].partition(" ")
    if partition[2] == "":
        track_name = partition[0][::-1]
    else:
        track_name = partition[2][::-1]

    output_file = MIDIFile(1)
    output_file.addTrackName(track, time, track_name)

    for index, pitch in enumerate(note_list):
        time = index
        output_file.addNote(track, channel, pitch, time, duration, volume)

    filename = track_name + ".mid"

    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)


if __name__ == "__main__":
    main()
