import azure.cognitiveservices.speech as speechsdk
import time

def speech_recognize_continuous_from_file(file):
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription="****", region="eastus")
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

print("_" * 50)
print(speech_recognize_continuous_from_file("temp_audio.wav"))
print("_" * 50)
