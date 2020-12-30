class Note:
    def __init__(self, type, when_note_starts, time):
        self.type = type
        self.when_note_starts = when_note_starts
        self.time = time
    def __str__(self):
        return f"Note(type={self.type}, when_note_starts={self.when_note_starts}, time={self.time})"