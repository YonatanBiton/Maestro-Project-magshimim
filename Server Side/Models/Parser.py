import py_midicsv as pm
class Parser:
    def __init__(self, file_path, midi_file_path):
        self.midi_file_path = midi_file_path
        self.file_path = file_path
        self.file = open(self.file_path, "a")
    
    def parse(self):
        # Load the MIDI file and parse it into CSV format
        csv_string = pm.midi_to_csv(self.midi_file_path)

        #variables
        stringToList = ""
        listOfNotes = []
        times = []
        note_list = []

        #this loop will parse the csv string and will put it into a list of the object Note
        for sent in csv_string:
            temp = sent.split()
            key_Note = temp[2]
            time = temp[1]

            if(key_Note == "Note_on_c,"):
                note_in_csv = temp[4]
                note_in_csv = note_in_csv[:-1]
                note_in_csv = int(note_in_csv)
                stringToList += chr(note_in_csv)

                if(time[-1] == ','):
                    times.append(time[:-1])
                note = Note(stringToList, int(time[:-1]), 0)
                note_list.append(note)

            if(key_Note == "Note_off_c,"):
                note_in_csv = temp[4]
                note_in_csv = note_in_csv[:-1]
                note_in_csv = int(note_in_csv)
                listOfNotes.append(stringToList)

                if (time[-1] == ','):
                    times.append(time[:-1])

                #this for loop will find how long the note is playing
                for note in reversed(note_list):
                    if(note.type == chr(note_in_csv)):
                        note.time = int(time[:-1]) - note.when_note_starts
                        break
            stringToList = ""
        file.write(listToString(csv_string))
        file.close(self.file_path)
   
