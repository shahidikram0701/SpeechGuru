import azure.cognitiveservices.speech as speechsdk
import time
import process_sentences
from collections import defaultdict

filler_words = [ "um", "ah", "basically", "umm", "right", "actually" ]

def speech_recognize_continuous_from_file(file):
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription="75ea7877e1ac405aac11036d4fe62f37", region="eastus")
    audio_config = speechsdk.audio.AudioConfig(filename=file)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    text = ""

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        nonlocal text
        nonlocal done
        if(evt.result.reason == speechsdk.ResultReason.RecognizedSpeech):
            text += evt.result.text
        if(evt.result.reason == speechsdk.ResultReason.Canceled):
            done = True
        
    speech_recognizer.recognized.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    return text

def process_sentences(text):
    text = "".join((char if char.isalpha() else " ") for char in text)
    global filler_words
    filler_words_dict = defaultdict(lambda: 0)
    sentences = text.split(".")
    for i in range(0, len(sentences), 1):
        sentence = sentences[i].lower().strip().split(" ")
        for word in sentence:
            word = word.strip()
            if word in filler_words:
                filler_words_dict[word] += 1
    return filler_words_dict

text = speech_recognize_continuous_from_file("temp_audio.wav")
print("Text Transcribed from Speech Service")
print("*" * 100)
print(text)
print("*" * 100)
print("\n" * 5)
response = process_sentences(text)
print("Processed Sentence [word: count]\n", [(key, response[key]) for key in response])
