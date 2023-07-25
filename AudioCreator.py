from gtts import gTTS
class sound:
    def play(self,name):
        self.language = "hi" 
        self.text = "Welcome to ATM System"   
        self.speech = gTTS(text = self.text,slow = False,tld = "com.au") 
        self.speech.save("welcome_om.mp3")