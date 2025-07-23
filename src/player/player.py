class Player:
    from pygame import mixer
    
    def __init__(self):
        self.mixer.init()
    
    def play(self, music_path):
        self.mixer.music.load(music_path)
        self.mixer.music.play()
        
    def pause(self):
        self.mixer.music.pause()
        
    def unpause(self):
        self.mixer.music.unpause()