


"""
function.py

Implements:
1. explain_sentence: Arabic sentence/question to Hebrew explanation
2. explain_word: Word to abstract JSON (root, binyan, singular, plural)
"""

from gemini import init_model
import arabic_reshaper
from bidi.algorithm import get_display
class Dialog:

	def __init__(self, model_name="gemini-1.5-flash"):
		"""
		Initialize the dialog with a specific model.
		Default is "gemini-1.5-flash".
		"""
		self.model_name = model_name
		self.gemini = init_model(model_name=model_name)
		self.conversation = []  # Placeholder for dialog object if needed later

	def answer_to_conversation(self):
		conversation_text = ""
		for question in self.conversation:
			conversation_text += question + "\n" 
		print(f"conversation_text: {conversation_text}")
		return self.convert_arabic(self.gemini.ask(f" תמשיך את השיחה (משפט אחד) בערבית וכתוב תרגום שורה מתחת בעברית: {conversation_text}", short_answer=True))


	def convert_arabic(self, text):
		reshaped = arabic_reshaper.reshape(text)       # Connect letters
		bidi_text = get_display(reshaped)              # Apply RTL direction
		return bidi_text


	def explain_sentence(self, sentence_ar: str, question_ar: str,  model_name="gemini-1.5-flash") -> str:
		"""
		Receives an Arabic sentence and a question in Arabic.
		Returns a Hebrew sentence with an explanation about the question in Hebrew.
		"""
		# Placeholder implementation
		# In production, replace with actual translation and explanation logic
		question = f"המשפט בערבית: {sentence_ar}  השאלה: {question_ar} ענה תשובה קצרה וקולעת"
		self.conversation.append(self.convert_arabic(question))  # Add question to dialog history if needed
		# שליחת השאלה
		answer = self.gemini.ask(question, short_answer=True)
		answer = self.convert_arabic(answer)  # Convert answer to Hebrew
		self.conversation.append(answer)  # Add answer to dialog history if needed
		return f"{answer}"


	def explain_word(self, word: str, model_name="gemini-1.5-flash -> dict"):
		"""
		Receives a word.
		Returns an abstract JSON explaining root, binyan, singular, and plural.
		"""
		# Placeholder implementation
		# In production, replace with actual morphological analysis
		question = f"המילה בערבית: {word} ענה: מה השורש שלה, מה הבניין שלה, מה הצורה היחידאית שלה ומה הצורה הרבים שלה התוצאה צריכה להיות רק את המילים בערבית ובפורמט מהבא: שורש : בניין : יחיד : רבים?"
		self.conversation.append(self.convert_arabic(question))
		gemini = init_model(model_name=model_name)
		# שליחת השאלה
		answer = gemini.ask(question, short_answer=True)
		answer = self.convert_arabic(answer)
		self.conversation.append(answer)
		parts = [part.strip() for part in answer.split(":")]
		result = {
			"word": self.convert_arabic(word),
			"root": parts[3] if len(parts) > 0 else "",
			"binyan": parts[2] if len(parts) > 1 else "",
			"singular": parts[1] if len(parts) > 2 else "",
			"plural": parts[0] if len(parts) > 3 else ""
		}
		return result




dialog = Dialog()
print(dialog.explain_word("جميلة", "gemini-1.5-flash"))
print(dialog.explain_sentence("اللغة العربية جميلة", "מה זה אומר על השפה הערבית?", "gemini-1.5-flash"))
print(dialog.answer_to_conversation())