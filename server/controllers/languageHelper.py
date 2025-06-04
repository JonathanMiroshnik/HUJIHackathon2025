import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from services.LLM.gemini import init_model

import arabic_reshaper
from bidi.algorithm import get_display

def convert_arabic(text):
		reshaped = arabic_reshaper.reshape(text)       # Connect letters
		bidi_text = get_display(reshaped)              # Apply RTL direction
		return bidi_text

def print_rtl(word: str):
	print(convert_arabic(word))

"""
function.py

Implements:
1. explain_sentence: Arabic sentence/question to Hebrew explanation
2. explain_word: Word to abstract JSON (root, binyan, singular, plural)
"""
class Dialog:
	def __init__(self, model_name='gemini-1.5-flash'):
		"""
		Initialize the dialog with a specific model.
		Default is "gemini-1.5-flash".
		"""
		self.model_name = model_name
		self.gemini = init_model(model_name=model_name)
		self.conversation = []  # Placeholder for dialog object if needed later

	def answer_to_conversation(self):
		# Turning the conversation up untill now into a single string
		conversation_text = ""
		for question in self.conversation:
			conversation_text += question + "\n"

		prompt: str = f""" 
		תמשיך את השיחה עם משפט אחד בערבית וכתוב תרגום שורה מתחת בעברית:\n\n
		{conversation_text}
		"""

		return self.gemini.ask(prompt, short_answer=True)

	def explain_sentence(self, sentence_ar: str, question_ar: str,  model_name='gemini-1.5-flash') -> str:
		"""
		Receives an Arabic sentence and a question in Arabic.
		Returns a Hebrew sentence with an explanation about the question in Hebrew.
		"""
		# Placeholder implementation
		# In production, replace with actual translation and explanation logic
		question = f"המשפט בערבית: {sentence_ar}  השאלה: {question_ar} ענה תשובה קצרה וקולעת"
		# question = f"""
		# המשך את השיחה 
		# """
		self.conversation.append(question)  # Add question to dialog history if needed

		answer = self.gemini.ask(question, short_answer=True)

		# answer = self.convert_arabic(answer)  # Convert answer to Hebrew
		self.conversation.append(answer)  # Add answer to dialog history if needed
		return f"{answer}"
	
	def explain_conversation(self, sentence_ar: list[str], model_name='gemini-1.5-flash') -> str:
		"""
		Receives an Arabic conversation.
		Returns an explanation of the conversation in Hebrew.
		"""
		result = ""
		for i, line in enumerate(sentence_ar):
			prefix = f"אדם {1 + i % 2}: "  # Alternates between User 1 and User 2
			result += prefix + line + "\n"
		
		prompt = f"מלפניך שיחה בין שני אנשים, בבקשה תסביר את השיחה בעברית, בלי לכתוב את ההסבר כשיחה. השיחה: {result}"
		# prompt = f"הסבר את השיחה בערבית בעברית, שים לב לא להוסיף את המילה משתמש או את המספר, זאת אומרת רק תסביר את השיחה ללא שום דיון נוסף, השיחה עד עכשיו: {result}"
		answer = self.gemini.chat.send_message(prompt)

		return answer.text

	def translate_conversation(self, sentence_ar: list[str], model_name='gemini-1.5-flash') -> str:
		"""
		Receives an Arabic conversation.
		Returns an explanation of the conversation in Hebrew.
		"""
		result = ""
		for i, line in enumerate(sentence_ar):
			prefix = f"אדם {1 + i % 2}: "  # Alternates between User 1 and User 2
			result += prefix + line + "\n"
		
		prompt = f"""
		לפניך שיחה בין שני אנשים, 
		בבקשה תתרגם את השיחה בעברית, 
		בלי לכתוב את התרגום כשיחה, 
		זאת אומרת בלי האינדיקטור אדם ונקודותיים, השיחה:\n\n
		{result}
		"""
		answer = self.gemini.chat.send_message(prompt)

		return answer.text

	def continue_conversation(self, sentence_ar: list[str], model_name='gemini-1.5-flash') -> str:
		"""
		Receives an Arabic conversation.
		Returns an Arabic sentence that continues the conversation.
		"""
		result = ""
		for i, line in enumerate(sentence_ar):
			prefix = f"אדם {1 + i % 2}: "  # Alternates between User 1 and User 2
			result += prefix + line + "\n"

		# prompt = f"תמשיך את השיחה בערבית בעוד משפט אחד, שים לב לא להוסיף את המילה אדם או את המספר, זאת אומרת רק את המשפט עצמו ללא שום דיון נוסף, השיחה עד עכשיו: {result}"
		prompt = f"""
		תמשיך את השיחה בערבית בעוד משפט אחד, 
		שים לב לא להוסיף את המילה אדם או את המספר, 
		זאת אומרת רק את המשפט עצמו ללא שום דיון נוסף, השיחה עד עכשיו:\n\n
		{result}
		"""
		answer = self.gemini.chat.send_message(prompt)

		return answer.text


	def explain_word(self, word: str, model_name='gemini-1.5-flash'):
		"""
		Receives a word.
		Returns an abstract JSON explaining root, binyan, singular, and plural.
		"""

		question = f"""
		המילה בערבית: {word}\n\n
		ענה:\n\n
		מה המשמעות שלה בעברית(בעברית), 
		מה השורש שלה(השורש כולו בערבית, לא להוסיף את אם אין שורש), 
		מה הבניין שלה(הבניין כולו בערבית, לא להוסיף את אם אין בניין), 
		מה צורת היחיד שלה(עם ניקוד, לא להוסיף את אם אין צורת יחיד), 
		מה צורת הרבים שלה(עם ניקוד, לא להוסיף את אם אין צורת רבים), 
		התוצאה צריכה להיות רק את המילים בערבית:\n
		יש לשים לב שאם שדה כלשהו אינו אמור להיכתב, אין להוסיפו לתוצאה הסופית.\n
		בפורמט JSON הבא:\n\n
		משמעות:\n
		שורש:\n
		בניין:\n
		יחיד:\n
		רבים:\n
		?
		"""
		# self.conversation.append(question)

		gemini = init_model(model_name=model_name)

		# Sending the request
		answer = gemini.json_chat.send_message(question)
		self.conversation.append(answer)

		partsStr: str = answer.candidates[0].content.parts[0].text		
		data = json.loads(partsStr)

		result: dict = {
			"meaning": data.get("משמעות"),
			"root": data.get("שורש"),
			"stem": data.get("בניין"),
			"singular": data.get("יחיד"),
			"plural": data.get("רבים")
		}

		return result


# dialog = Dialog()
# print(dialog.explain_word("جميلة", "gemini-1.5-flash"))
# print(dialog.explain_sentence("اللغة العربية جميلة", "מה זה אומר על השפה הערבית?", "gemini-1.5-flash"))
# print(dialog.answer_to_conversation())