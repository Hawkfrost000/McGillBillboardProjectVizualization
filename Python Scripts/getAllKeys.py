#!/usr/bin/env python3
import csv

keys = []
key_id = 1

with open("song_summary.csv") as csvIn:
	with open("all_keys.csv", "w") as csvOut:
		reader = csv.DictReader(csvIn)
		writer = csv.writer(csvOut)
		next(reader, None)  # returns the headers or `None` if the input is empty
		writer.writerow(["Tonic_Id", "Tonic"])
		for row in reader:
			key = row["Tonic"]
			if key not in keys:
				writer.writerow([key_id, key])
				keys.append(key)
				key_id += 1


