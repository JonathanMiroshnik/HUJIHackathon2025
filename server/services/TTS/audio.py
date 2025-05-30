import pyttsx3
import speech_recognition as sr
import arabic_reshaper
from bidi.algorithm import get_display


# pip install pyttsx3
# pip install SpeechRecognition
# pip install pipwin
# pipwin install pyaudio



def convert_arabic(text):
	reshaped = arabic_reshaper.reshape(text)       # Connect letters
	bidi_text = get_display(reshaped)              #<aApply RTL direction
	return bidi_text


def say_message(message):
    """
    מקריא בקול את ההודעה שניתנת כפרמטר
    """
    print("say massage:", message)
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


def listen_and_recognize_arabic(text):
    """
    מאזין למה שנאמר ומחזיר את הטקסט שזוהה בערבית
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(convert_arabic("הקשב: התחל לדבר עכשיו (בערבית)..." + text))
        audio = recognizer.listen(source)
        print(convert_arabic("מעבד את הדיבור..."))

    try:
        # זיהוי דיבור בשפה הערבית
        text = recognizer.recognize_google(audio, language="ar")
        return text
    except sr.UnknownValueError:
        return "لم أفهم ما قيل."  # לא הצלחתי להבין את מה שנאמר
    except sr.RequestError:
        return "هناك خطأ في الاتصال بخدمة التعرف."  # תקלה בחיבור לשירות הזיהוי

def conversation_with_user(text):
    """
	מנהל שיחה עם המשתמש, מקשיב לדיבור ומחזיר את הטקסט המוכר
	"""
    # say_message(convert_arabic(text))
    list_text = convert_arabic(text.replace(',', '').replace('.', '').replace('،','')).split()
    list_text.reverse()
    print(f"list_text: {list_text}")
    recognized_text = convert_arabic(listen_and_recognize_arabic(text))
    print(recognized_text)
    miss_words = []
    words_list = recognized_text.split()
    print(f"word list: {words_list}")
    len_text_list = len(list_text)
    index1 = 0
    index2=0
    print(f"text_list: {list_text}, words_list: {words_list}")
    words_list.reverse()
    while index2 < len_text_list:
        print(f" tour {list_text[index2]}")
        if words_list[index1] != list_text[index2]:
             print(f"missed word: {list_text[index2]} the word said was: {words_list[index1]}")
             miss_words.append(list_text[index2])
             index2 += 1
             if index2 > len_text_list:
                  break
             if words_list[index1] in list_text:
                    while words_list[index1] != list_text[index2]:
                          if index2 > len_text_list:
                                break
                          miss_words.append(list_text[index2])
                          print(f"word in list: missed word: {list_text[index2]} the word said was: {words_list[index1]}")
                          index2 += 1
                          
					
        index1 += 1
        index2 += 1
        if index1 >= len(words_list):
             i = index2
             while i < len_text_list:
                 miss_words.append(list_text[i])
                 i += 1
             break
    
    if miss_words:
        final_words = []
        for w in miss_words:
             final_words.append(convert_arabic(w))
        return final_words
    return []

def main():
    """
    הפונקציה הראשית שמפעילה את כל התהליך
    """
    coorrect = conversation_with_user("مرحبًا، اسمي محمد")
    print(coorrect)

if __name__ == "__main__":
    main()
