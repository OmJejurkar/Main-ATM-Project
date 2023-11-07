from gtts import gTTS

language = "hi" 
text = "Ganesh Jorwekaer"   
speech = gTTS(text = text,slow = False,tld = "com.au") 
speech.save("welcome_vaishnavi.mp3")