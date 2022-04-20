# McGillBillboardProjectVizualization

Wecome!

This is a small project designed to facilitate analysis on the [McGill-Billboard Corpus](https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/). It contains a few components:
1. A group of python scripts to parse the information contained in the corpus into a more database friendly format
2. A set of database schema to contain the information produced by the scripts
3. A java class to make queries against the databases, and present the information to the user.

The individual Java and Python files are documented, this file contains some documentation about the database and a more general overview of the project. If you're interested in reading more about the process of creating this proof of concept, you can read more about it in [this report](https://docs.google.com/document/d/1J2Lt2xn-FLOp-WE5PMivazp_Oy3BYYgBeE4ltFgrk1M/edit?usp=sharing).

## Database Documentation
If you havent worked with SQL before, you can find a setup tutorial [here](https://docs.microsoft.com/en-us/sql/azure-data-studio/quickstart-sql-server?view=sql-server-ver15).  
The Tables I build using the CSV files you can find in the Resulting Files folder look something like this: 
<img width="462" alt="song_database" src="https://user-images.githubusercontent.com/43019110/164148443-a9b876b8-1313-4c2b-9093-3ffae904964e.PNG">

Essentially the song_summary table contains the `song_id` which is used to connect all of the tables together with queries like `SELECT song_summary.Song_Name FROM song_summary INNER JOIN roman_chords_no_repeats ON song_summary.Song_ID = songs_and_chords_no_repeats.Song_ID WHERE songs_and_chords_no_repeats.Chords LIKE ?`. You can certainly modify these to fit your own needs, but that will impact the existing queries that I've written in the DatabaseConnection class. 
