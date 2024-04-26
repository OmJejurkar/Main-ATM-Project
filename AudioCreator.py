from gtts import gTTS

language = "hi" 
text = "Welcome to SecureVault System"   
speech = gTTS(text = text,slow = False,tld = "com.au") 
speech.save("welcome_om.mp3")