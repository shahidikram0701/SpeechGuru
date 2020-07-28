import azure.cognitiveservices.speech as speechsdk
import time
# import process_sentences
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt

debug = False

def debug_print(*args):
    if(debug):
        print(*args)

with open("input.txt", "r") as file:
    input_speech= file.read()

tokens_input = word_tokenize(input_speech)
word_counts_input = {}
word_counts_input = word_counts_input.fromkeys(tokens_input)
for i in word_counts_input:
    word_counts_input[i] = tokens_input.count(i)
# debug_print("word_counts_input: ", word_counts_input)


filler_words = [ "um", "ah", "basically", "umm", "right", "actually", "so", "like" ]
profanity = ["shit", "damn", "fuck", "heck", "hell", "bullshit", "crap", "nigga"]


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
            text += evt.result.text + "\n\n"
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

def process_sentences_filler_words_and_profanity(text):
    global word_counts_text
    profanity_words_detected = []
    filler_words_detected = []
    for i in profanity:
        if i in word_counts_text:
            profanity_words_detected.append({i: word_counts_text[i]})

    for i in filler_words:
        if(i in word_counts_text):
            filler_words_detected.append({i: word_counts_text[i]})

    return filler_words_detected, profanity_words_detected

def process_tone(text):
    feedback = {}

    global word_counts_input
    global word_counts_text
    num_paras_actual = input_speech.count("\n\n")
    num_paras_transcribed = text.count("\n\n")

    debug_print("num_paras_actual: ", num_paras_actual)
    debug_print("num_paras_transcribed: ", num_paras_transcribed)

    if(num_paras_actual < num_paras_transcribed):
        feedback["paras"] = 1
    elif(num_paras_actual > num_paras_transcribed):
        feedback["paras"] = -1
    else:
        feedback["paras"] = 0
    try:
        num_sentences_actual = word_counts_input["."]
    except:
        num_sentences_actual = 0

    try:
        num_sentences_transcribed = word_counts_text["."]
    except:
        num_sentences_transcribed = 0

    debug_print("num_sentences_actual: ", num_sentences_actual)
    debug_print("num_sentences_transcribed: ", num_sentences_transcribed)

    if(num_sentences_actual < num_sentences_transcribed):
        feedback["sentences"] = 1
    elif(num_sentences_actual > num_sentences_transcribed):
        feedback["sentences"] = -1
    else:
        feedback["sentences"] = 0


    try: 
        num_questions_actual = word_counts_input["?"]
    except:
        num_questions_actual = 0
    
    try:
        num_questions_transcribed = word_counts_text["?"]
    except:
        num_questions_transcribed = 0

    debug_print("num_questions_actual: ", num_questions_actual)
    debug_print("num_questions_transcribed: ", num_questions_transcribed)

    if(num_questions_actual < num_questions_transcribed): 
        feedback["questions"] = 1
    elif(num_questions_actual > num_questions_transcribed):
        feedback["questions"] = -1
    else:
        feedback["questions"] = 0

    try:
        num_exclamations_actual = word_counts_input["!"]
    except:
        num_exclamations_actual = 0
    try:
        num_exclamtions_transcribed = word_counts_text["!"]
    except:
        num_exclamtions_transcribed = 0

    debug_print("num_exclamations_actual: ", num_exclamations_actual)
    debug_print("num_exclamtions_transcribed: ", num_exclamtions_transcribed)

    if(num_exclamations_actual < num_exclamtions_transcribed):
        feedback["exclamation"] = 1
    
    elif(num_exclamations_actual > num_exclamtions_transcribed):
        feedback["exclamation"] = -1
    
    else:
        feedback["exclamation"] = 0


    try:
        num_commas_actual = word_counts_input[","]
    except:
        num_commas_actual = 0
    try:
        num_commas_transcribed = word_counts_text[","]
    except:
        num_commas_transcribed = 0

    debug_print("num_commas_actual: ", num_commas_actual)
    debug_print("num_commas_transcribed: ", num_commas_transcribed)

    if(num_commas_actual < num_commas_transcribed):
        feedback["commas"] = 1
    
    elif(num_commas_actual > num_commas_transcribed):
        feedback["commas"] = -1
    
    else:
        feedback["commas"] = 0

    return feedback
# text = speech_recognize_continuous_from_file("temp_audio.wav")
# debug_print("Text Transcribed from Speech Service")
# debug_print("*" * 100)
# debug_print("transcribed Text: ", text)
# with open("transcribed_text.txt", "w") as file:
#     file.write(text)
# debug_print("*" * 100)
# debug_print("\n" * 5)
# response = process_sentences(text)
# debug_print("Processed Sentence [word: count]\n", [(key, response[key]) for key in response])


with open("transcribed_text.txt", "r") as file:
    text = file.read()

text = text.lower()
tokens_text = word_tokenize(text)
word_counts_text = {}
word_counts_text = word_counts_text.fromkeys(tokens_text)
for i in word_counts_text:
    word_counts_text[i] = tokens_text.count(i)
# debug_print("word_counts_text: ", word_counts_text)

tone_feedback = process_tone(text)
debug_print("feedback: ", tone_feedback)


filler_words_detected, profanity_words_detected  = process_sentences_filler_words_and_profanity(text)
debug_print("filler_words_detected: ", filler_words_detected)
debug_print("profanity_words_detected: ", profanity_words_detected)


def generateFeeback(tone_feedback, filler_words_detected, profanity_words_detected):
    global word_counts_text
    feedback_message = "_" * 100
    feedback_message += "\n\n A detailed report I could come up with listening to you speak! Hope I can be of any help :) \n\n"
    feedback_message += "Lets start with analysis of the tone with which you were speaking!\n\n"
    tone_feedback_message = {
        "paras": {
            -1: "It appears that the deliberate long pauses between the different paragraphs could be something we could improve upon.",
            0: "Spot on with the deliberate long pauses between the different paragraphs.",
            1: "Oopsie, Seems like there were quite a few extra long pauses you had right there. Maybe we could improve upon exerting those long pauses as approproate, and not overdoing it. :)"
        },
        "sentences": {
            -1: "Oops, May be we hurried up a bit there. Felt like some sentences couldn't be distiguished from the other. If we could work upon those tiny little pauses to be able to differentiate sentences, may be the audience could connect better. You know what I am saying yeah?",
            0: "Perfecto. Seems like every sentence you delivered was crisp and clear. Way to go!",
            1: "Ouch seems like we had an un-necessary pause mid-sentence in some places. Lets work on delivering each sentence, clearly and confidently without breaks!"
        },
        "questions": {
            -1: "Did we miss a question out there. Seems like it didnt sound like one. Maybe if we could get the right tone to stimulate a train of thoughts in the audience, to make them curious for an answer, it would be more engaging. Don't you think?", 
            0: "Aha! Bravo. Every question you put out there, piqued my curiosity to wanting to know the answer right away. Well done! Lets keep the tone rolling!",
            1: "Did we just end up making something that not a queston, sound like one and leave the audience confused? Let's work on it! We could do better. Can't we?"
        },
        "exclamation": {
            -1: "Aye! Where's that excitement hiding mate. Bring it out. Seems like we need to go Hurraayy!!!! a bit more. The secret to getting a listener excited and wanting for more is the energy that you radiate. Lets get the enrgy up!",
            0: "Wow! That was terrific! You nailed all the exlamations with all the energy you got! Good job buddy! Way to go!",
            1: "Ooh! That was a high energy exciting talk.",
        },
        "commas": {
            -1: "We could probably work on those soft pauses during a sentence.",
            0: "That right there was perfection. The soft pauses during the sentences capturing the attention of the audience done graciously. Job Well done!!",
            1: "Aah, Seemed like we had one too many soft pauses in a sentence right there. Let us work on getting them right! What say?" 
        }
    }
    feedback_message += "\t1. "+ tone_feedback_message["paras"][tone_feedback["paras"]] + "\n\t2. " + tone_feedback_message["sentences"][tone_feedback["sentences"]] + "\n\t3. " + tone_feedback_message["questions"][tone_feedback["questions"]] + "\n\t4. " + tone_feedback_message["exclamation"][tone_feedback["exclamation"]] + "\n\t5. " + tone_feedback_message["commas"][tone_feedback["commas"]]

    if(len(filler_words_detected) > 0):
        filler_words_detected.sort(key=lambda x: list(x.values())[0], reverse=True)
        feedback_message += "\n\nFiller Words details: \n" + "Your top 5 most used filler words are: \n"
        for i in range(min(5, len(filler_words_detected))):
            item = list(filler_words_detected[i].items())[0]
            feedback_message += "\t" + str(i+1) + ". "+ "'" + item[0] + "'" + " used " + str(item[1]) + " times\n"

        total_words_spoken = sum(list(word_counts_text.values()))
        # total_filler_words_spoken = sum([i for i in list(filler_words_detected[i].values())[0]])
        total_filler_words_spoken = sum(list(map(lambda x: list(x.values())[0], filler_words_detected)))

        percentage_filler_words = (total_filler_words_spoken / total_words_spoken) * 100

        feedback_message += "\nOkay we have another interesting insight that might help you. Looks like your speech contains {:.2f}% of filler words! Hope this helps you improve refining your talk :)".format(percentage_filler_words)

    if(len(profanity_words_detected) > 0):
        feedback_message += "\n\nDid you just say that?! :O\n\nLooks like I heard some words there that might well qualify to go behind a beep! Ooopppss!\n"
        feedback_message += "Words that you might have uttered unconciosly that would probably need a little reconsideration, if appropriate to be used whilst talking to an audience as I could point out would be:\n"
        profanity_words_detected.sort(key=lambda x: list(x.values())[0], reverse=True)
        for i in range(len(profanity_words_detected)):
            item = list(profanity_words_detected[i].items())[0]
            feedback_message += "\t" + str(i+1) + ". " + "'" + item[0] + "'" + " used " + str(item[1]) + " times\n"

        feedback_message += "\nI think it would be wonderful if we could reduce the usage of these words as if would create a sense of uncomforatability for certain people in the audience! It wont hurt to come clean every once in a while...Will it now?! :P\n\n"

    feedback_message += "_" * 100

    return feedback_message


feedback_report = generateFeeback(tone_feedback, filler_words_detected, profanity_words_detected)
print(feedback_report)



    





        


        


