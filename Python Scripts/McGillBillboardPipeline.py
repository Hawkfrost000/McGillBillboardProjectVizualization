#!/usr/bin/env python3
import re
import csv

# this is a group of scripts which are designed to process the list of song files from the McGill Billboard Corpus
# and produce a series of csvs which can then be imported into a database

# this method goes through all the files and loads them into memory so that they can be used by other methods 
# in order for this script to work, all the song files need to be in the same directory, but you change the filename
# variable to follow a different path if you need to.
def getAllFiles():
	startNumFiles = 3
	endNumFiles = 892
	allFiles = []
	counter = startNumFiles
	# load all the files into memory
	while counter <= endNumFiles:
		filename = "{}-salami_chords".format(counter)
		file = open(filename)
		content = file.readlines()  # interprets the file as a list of strings, where each string is a line in the file
		allFiles.append(content)  # adds this list of strings to list so that we can iterate over it later.
		counter += 1			  # so allFiles is going to be a list of list of strings
								  # allFiles = [["a",
								  #				 "list",
								  #				 "of",
								  #				 "lines"],
								  #				["another",
								  #				 "list",
								  #				 "of",
								  #				 "lines"]] 
	return allFiles

# the first four rows of these files are formatted like;
# 		Title: A Song Title
# this script splits the string at the character ":" and returns the second part, the actual song title/artist name, etc.
def splitAndStrip(string):
	return string.split(": ")[1].strip("\n")

# This method looks at the first four lines of each file to create a summary of each song
# a csv with each song's Song_ID, Name, Artist, Metre, and Tonic
def summarizeSongData(list_of_files):
	song_id = 1
	out = open("song_summary.csv", "w")
	out.write("Song_ID,Song_Name,Artist,Metre,Tonic\n")
	for file in list_of_files:
		# the first two lines are always name and artist
		name = splitAndStrip(file[0])
		artist =  splitAndStrip(file[1])
		third = file[2]
		fourth = file[3]
		# the third and fourth line (Metre and Tonic) dont have a consistent order, so we need to check which is which
		if "# metre" in third:
			metre = splitAndStrip(third)
			tonic = splitAndStrip(fourth)
		else:
			tonic = splitAndStrip(third)
			metre = splitAndStrip(fourth)
		string = "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n".format(song_id, name, artist, metre, tonic)
		out.write(string)
		song_id += 1

# This method finds the song name, which is always the first line, and the duration, which is always the second to last line
# creates a csv with each song's Song_ID, Name, and Duration
def writeSongDuration(list_of_files):
	song_id = 1
	out = open("song_durations.csv", "w")
	out.write("Song_ID,Song_Name,Song_Duration\n")
	for file in list_of_files:
		name = splitAndStrip(file[0])
		duration = file[-2].split("	")[0]
		string = "\"{}\",\"{}\",\"{}\"\n".format(song_id, name, duration)
		out.write(string)
		song_id += 1

# returns a list of all the cords in the entire billboard corpus, and writes those chords to a file
# maybe returning a list and writing a list should be seperate functions?
def getAllChords(list_of_files):
	out = open("all_chords.txt", "w")
	out.write("\"Chord_ID\",\"Chord_Name\"\n")
	chord_counter = 1
	allChords = []
	for file in list_of_files:
		for line in file:
			chords = re.findall(r"\| \w+:\w+", line)
			for chord in chords:
				strippedChord = chord.strip("|").strip()
				if strippedChord not in allChords:
					allChords.append(strippedChord)
					string = "\"{}\",\"{}\"\n".format(chord_counter, strippedChord)
					out.write(string)
					chord_counter += 1

# write out a file containing the name, tonic, and every chord of every song
def getSongChords(list_of_files):
	out = open("songs_and_chords.txt", "w")
	song_id = 1
	for file in list_of_files:
		name = splitAndStrip(file[0])
		third = file[2]
		fourth = file[3]
		if "# metre" in third:
			tonic = splitAndStrip(fourth)
		else:
			tonic = splitAndStrip(third)
		out.write("Name: " + name + "\n")
		out.write("Tonic: " + tonic + "\n")
		out.write("Chords:\n")
		for line in file:
			chords = re.findall(r"\| \w+:\w+", line)
			for chord in chords:
				strippedChord = chord.strip("|").strip()
				out.write(strippedChord + "\n")
		out.write("\n")

# write out a file containing the song_id, tonic, and every chord of every song in sequence
def getSongChordsCSV(list_of_files):
	with open("songs_and_chords.csv", "w") as csvOut:
		writer = csv.writer(csvOut)
		writer.writerow(["Song_ID", "Tonic", "Chords"])
		song_id = 1
		for file in list_of_files:
			third = file[2]
			fourth = file[3]
			if "# metre" in third:
				tonic = splitAndStrip(fourth)
			else:
				tonic = splitAndStrip(third)
			string_of_chords = ""
			for line in file:
				chords = re.findall(r"\| \w+:\w+", line)
				for chord in chords:
					strippedChord = chord.strip("|").strip()
					string_of_chords += strippedChord + ","
			writer.writerow([song_id, tonic, string_of_chords])
			song_id += 1

# write out a file containing the song_id, tonic, and every chord of every song in sequence, ignoring repeats.
# so a line like C:maj | C:maj | C:maj | G:maj will appear as "C:maj,A:maj"
def getSongChordsCSVWithoutRepeats(list_of_files):
	with open("songs_and_chords_no_repeats.csv", "w") as csvOut:
		writer = csv.writer(csvOut)
		writer.writerow(["Song_ID", "Tonic", "Chords"])
		song_id = 1
		for file in list_of_files:
			third = file[2]
			fourth = file[3]
			if "# metre" in third:
				tonic = splitAndStrip(fourth)
			else:
				tonic = splitAndStrip(third)
			string_of_chords = ""
			last_chord = ""
			for line in file:
				chords = re.findall(r"\| \w+:\w+", line)
				for chord in chords:
					strippedChord = chord.strip("|").strip()
					if strippedChord != last_chord:
						string_of_chords += strippedChord + ","
						last_chord = strippedChord
			writer.writerow([song_id, tonic, string_of_chords])
			song_id += 1

# write out a file similar to the above but with each chord appearing only once
def getUniqueSongChords(list_of_files):
	out = open("songs_and_unique_chords.txt", "w")
	song_id = 1
	for file in list_of_files:
		song_chords = []
		name = splitAndStrip(file[0])
		third = file[2]
		fourth = file[3]
		if "# metre" in third:
			tonic = splitAndStrip(fourth)
		else:
			tonic = splitAndStrip(third)
		out.write("Name: " + name + "\n")
		out.write("Tonic: " + tonic + "\n")
		out.write("Chords:\n")
		for line in file:
			chords = re.findall(r"\| \w+:\w+", line)
			for chord in chords:
				strippedChord = chord.strip("|").strip()
				if strippedChord not in song_chords:
					out.write(strippedChord + "\n")
					song_chords.append(strippedChord)
		out.write("\n")

# writes a csv of the unique chords for each song (very similar to getUniqueSongChords, but easier to put into a database)
def getUniqueSongChordsCSV(list_of_files):
	with open("songs_and_unique_chords.csv", "w") as csvOut:
		writer = csv.writer(csvOut)
		writer.writerow(["Song_ID", "Tonic", "Chords"])
		song_id = 1
		for file in list_of_files:
			song_chords = []
			third = file[2]
			fourth = file[3]
			if "# metre" in third:
				tonic = splitAndStrip(fourth)
			else:
				tonic = splitAndStrip(third)
			string_of_chords = ""
			for line in file:
				chords = re.findall(r"\| \w+:\w+", line)
				for chord in chords:
					strippedChord = chord.strip("|").strip()
					if strippedChord not in song_chords:
						string_of_chords += strippedChord + ","
						song_chords.append(strippedChord)
			writer.writerow([song_id, tonic, string_of_chords])
			song_id += 1

# returns a list of all the song terms used 
def getAllSongTerms(list_of_files):
	terms = []
	out = open("songs_terms.txt", "w")
	out.write("Song Terms \n")
	for file in list_of_files:
		for line in file:
			term = re.search(r", \w+,", line)
			if (term):
				strippedTerm = term.group(0).strip(",").strip()
				if (strippedTerm not in terms):
					out.write(strippedTerm + "\n")
					terms.append(strippedTerm)
	return terms

#outputs a list of each term used in each song
def getTermsForEachSong(list_of_files, list_of_terms):
	out = open("songs_terms_by_song.txt", "w")
	song_id = 1
	for file in list_of_files:
		name = splitAndStrip(file[0])
		out.write("Name: " + name + "\n")
		for line in file:
			match = re.search(r", \w+,", line)
			if match:
				cleanMatch = match.group(0).strip(",").strip()
				if cleanMatch in list_of_terms:
					out.write(cleanMatch + "\n")

def main():
	list_of_files = getAllFiles()
	summarizeSongData(list_of_files)
	writeSongDuration(list_of_files)
	chords = getAllChords(list_of_files)
	getSongChords(list_of_files)
	getSongChordsCSV(list_of_files)
	getSongChordsCSVWithoutRepeats(list_of_files)
	getUniqueSongChords(list_of_files)
	getUniqueSongChordsCSV(list_of_files)
	terms = getAllSongTerms(list_of_files)
	getTermsForEachSong(list_of_files, terms)

if __name__ == "__main__":
	main()

