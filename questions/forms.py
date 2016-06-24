from django import forms
from .models import LEVELS, Question, Answer

class UserResponseForm(forms.Form):
	question_id = forms.IntegerField()
	answer_id = forms.IntegerField()
	importance_level = forms.ChoiceField(choices=LEVELS)
	their_answer_id = forms.IntegerField()
	their_importance_level = forms.ChoiceField(choices=LEVELS)
	
	def clean_question_id(self):
		question_id = self.cleaned_data.get('question_id')
		try:
			obj = Question.objects.get(id=question_id)
		except:
			raise forms.ValidationError('Es gab ein Problem mit deiner Frage.')
		
		return question_id
	

	def clean_answer_id(self):
		answer_id = self.cleaned_data.get('answer_id')
		try:
			obj = Answer.objects.get(id=answer_id)
		except:
			raise forms.ValidationError('Es gab ein Problem mit deiner Antwort.')
	
		return answer_id


	def clean_their_answer_id(self):
		their_answer_id = self.cleaned_data.get('their_answer_id')
		try:
			obj = Answer.objects.get(id=their_answer_id)
		except:
			if their_answer_id == -1:
				return their_answer_id
			else:
				raise forms.ValidationError('Es gab ein Problem mit deiner Antwort. Also mit der..... du weisst schon.')

		return their_answer_id