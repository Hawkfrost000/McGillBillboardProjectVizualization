#!/usr/bin/env python3
import re
import csv

notes = ["C", "C#:Db", "D", "D#:Eb", "E", "F" "F#:Gb", "G", "G#:Ab", "A", "A#:Bb", "B"]
non_sharp_notes = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
sharp_notes = {"C#": 1, "Db": 1, "D#": 3, "Eb": 3, "Fb": 4, "F#": 6, "Gb": 6, "G#": 8, "Ab": 8, "A#":10, "Bb":10, "Cb":11}
scale = ["maj", "min", "min", "maj", "maj", "min", "dim"]
numeral_map = {0: "i", 2: "ii", 4: "iii", 5: "iv", 7: "v", 9: "vi", 11: "viio"}
chromatic_numerals_map = {0: "I", 1: "bII", 2: "II" ,3: "bIII", 4: "III", 5: "IV", 6: "#IV", 7: "V", 8: "bVI", 9: "VI", 10: "bVII", 11: "VII"}


def getIndexOfNote(note):
	if len(note) == 1:
		return non_sharp_notes[note]
	else:
		return sharp_notes[note]

def getNumeral(tonic_index, note):
	note_index = getIndexOfNote(note)
	distance_from_tonic = note_index - tonic_index
	if distance_from_tonic < 0:
		distance_from_tonic += 12
	try: 
		return numeral_map[distance_from_tonic]
	except:
		return note

def getNumeralUsingChromaticNumerals(tonic_index, note):
	note_index = getIndexOfNote(note)
	distance_from_tonic = note_index - tonic_index
	if distance_from_tonic < 0:
		distance_from_tonic += 12
	return chromatic_numerals_map[distance_from_tonic]

def convertChord(tonic, chord):
	index_of_tonic = getIndexOfNote(tonic)
	note = chord.split(":")[0]
	try: 
		annotation = chord.split(":")[1]
	except:
		annotation = ""
	numeral = getNumeralUsingChromaticNumerals(index_of_tonic, note)
	return numeral + ":" + annotation

def convertFile(infile_name, outfile_name):
	with open(infile_name, newline='') as csvfile, open(outfile_name, "w") as csvOut:
		file_reader = csv.reader(csvfile)
		file_writer = csv.writer(csvOut)
		headers = next(file_reader, None)  # returns the headers or `None` if the input is empty
		if headers:
			file_writer.writerow(headers)
		for row in file_reader:
			song_id = row[0]
			tonic = row[1]
			chords = row[2]
			list_of_chords = chords.split(",")
			numeral_chords = ""
			for chord in list_of_chords:
				if chord:
					numeral_chords += convertChord(tonic, chord) + ","
			file_writer.writerow([song_id, tonic, numeral_chords])

def main():
	convertFile("songs_and_unique_chords.csv", "songs_and_unique_chords_numerals.csv")
	convertFile("songs_and_chords.csv", "songs_and_chords_numerals.csv")
	convertFile("songs_and_chords_no_repeats.csv", "songs_and_chords_numerals_no_repeats.csv")

if __name__ == "__main__":
	main()