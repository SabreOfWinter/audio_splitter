from pydub import AudioSegment
import os
from pathlib import Path
import time

#####################################
# PROGRAM LOGIC
# 1. Loop through all audio files
# 2. Find a matching txt file
# 3. Create a folder
# 4. Open txt file and 
# 5. Split by new line and loop through each song
# 6. Split by spaces and use the first 2 as strt and end times
# 7. Extract audio
# 8. Save audio in folder

def convert_timestamp_to_milliseconds(time):
    seconds = 0
    convert_array = [0,0,0]
    time_array = time.split(':')

    #Converts MM:SS format to HH:MM:SS
    if len(time_array) == 2:
        convert_array[0] = 0
        convert_array[1] = time.split(':')[0]
        convert_array[2] = time.split(':')[1]
    else:
        convert_array = time.split(':')

    seconds += int(convert_array[0]) * 60 * 60 #Convert hours to seconds
    seconds += int(convert_array[1]) * 60 #Convert minutes to seconds
    seconds += int(convert_array[2].replace('\u200b', '')) #Removes an invisible char in some text files

    return seconds * 1000 #Convert to milliseconds

def get_audio(start, end, sound, last_song):
    start = convert_timestamp_to_milliseconds(start)

    if last_song:
        end = len(sound)
    else:
        end = convert_timestamp_to_milliseconds(end)

    print('start time', start, ' :  end time', end)

    return sound[start:end]

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

for file in files:
    if len(file.split('.')) > 1:
        if file.split('.')[1] == 'mp3': #Check if file mp3
            album_name = file.split('.')[0] #Album name to use for naming folder
            txt_file_path = album_name + '.txt'

            if os.path.exists(txt_file_path): #Checks if there is a text document with song timestamps 
                print('\n','album: ', album_name)
                album_folder_path = str(cwd + "\\" + album_name)

                if(Path(album_folder_path).exists() == False):
                    print('Creating folder: ', Path(album_folder_path))
                    os.mkdir(Path(album_folder_path))

                #
                with open(txt_file_path, encoding='utf-8') as txt_file: #Opens text file with timestamps
                    #importing file from location by giving its path
                    file_stream = txt_file.read() 
                    open_song_elasped_start = time.perf_counter()
                    sound = AudioSegment.from_mp3(file)
                    open_song_elasped_end = time.perf_counter()
                    open_song_elasped_total = open_song_elasped_end - open_song_elasped_start
                    print(f'Time take to load playlist: {open_song_elasped_total:.6} seconds')
                    # sound = [1,3] #Test array to stop loading (used for testing txt file errors)
                    song_list = file_stream.split('\n')
                    
                    #Loop through each song with their timestamp
                    for i in range(0,len(song_list)):
                        song_details = song_list[i].split(' ', 1)
                        file_save_path = str(album_folder_path + '\\' + song_details[1] + '.mp3')
                        print(song_details[1], ' (', ((i+1)/len(song_list)*100), '% of playlist)')
                        
                        if(Path(album_folder_path).exists()):
                            if(Path(file_save_path).exists() == False):
                                elasped_start = time.perf_counter()

                                #Get the current song start and the next song start (as end)
                                #Check if the next song is also the last
                                if(i < len(song_list) - 1):
                                    song = get_audio(song_details[0], song_list[i+1].split(' ', 1)[0], sound, False) #get current song time as start, and get the next songs time as end time
                                #Get the current song start time and total length of audio file
                                else:
                                    song = get_audio(song_details[0], '0:00', sound, True)
                                
                                song.export(Path(file_save_path), format="mp3", bitrate="128k", tags={"album": album_name})
                                elasped_end = time.perf_counter()
                                elasped_total = elasped_end - elasped_start
                                
                                print(f'Time take to export song: {elasped_total:.6} seconds')
