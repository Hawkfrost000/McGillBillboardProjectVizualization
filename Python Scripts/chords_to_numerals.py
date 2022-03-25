#!/usr/bin/env python3

notes = ["C", "C#:Db", "D", "D#:Eb", "E", "F" "F#:Gb", "G", "G#:Ab", "A", "A#:Bb", "B"]
non_sharp_notes = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
sharp_notes = {"C#": 1, "Db": 1, "D#": 3, "Eb": 3, "F#": 6, "Gb": 6, "G#": 8, "Ab": 8, "A#":10, "Bb":10}
scale = ["maj", "min", "min", "maj", "maj", "min", "dim"]
numeral_map = {0: "I", 2: "ii", 4: "iii", 5: "IV", 7: "V", 9: "vi", 11: "viio"}


def getIndexOfNote(note):
	if len(note) == 1:
		return non_sharp_notes[note]
	else:
		return sharp_notes[note]

def getNumeral(tonic_index, note):
	note_index = getIndexOfNote(note)
	absolute_note_index = note_index + tonic_index
	relative_note_index = absolute_note_index % 12
	try: 
		return numeral_map[relative_note_index]
	except:
		return note

def convertChord(tonic, chord):
	index_of_tonic = getIndexOfNote(tonic)
	note = chord.split(":")[0]
	annotation = chord.split(":")[1]
	numeral = getNumeral(index_of_tonic, note)
	return numeral + ":" + annotation

def main():
	print("first song:")
	tonic = "C"
	chords = ["A:min","C:maj","F:maj","D:maj","G:maj","A:maj"]
	for chord in chords:
		print(convertChord(tonic, chord))
	print("second song:")
	tonic = "Ab"
	chords = ["Ab:maj","Db:maj","G:hdim7","F:min","C:7","Bb:min7","Eb:7","C:min7","Eb:11","Eb:maj","Ab:7","Ab:maj7","Gb:maj","Db:maj7","Gb:7","F:min7"]
	for chord in chords:
		print(convertChord(tonic, chord))

if __name__ == "__main__":
	main()