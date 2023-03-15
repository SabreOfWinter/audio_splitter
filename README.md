# audio_splitter

Python program using pydub to look through the working directory to find any mp3 files and a text file with a matching file name. 
The text file has a format below:

00:00:00 Song name
or
00:00 Song name

Current version will throw up an error if the file name contains any chars not allowed to be used for a file name (e.g. \/ : * ? " <> | )
(A file name clearner will need to be added (Should be when the filename is grabbd from the textfile))

Will need to add an option for cutting songs using only silence
(pydub has a feature for this, will just need to add it in)

Possibly, a GUI added to the program my be useful for further expansion, with features such as selecting current directory, a song list with details, a checkbox for options (such as cut by silence), an dropdown option for file formats to recognised and to save as.
