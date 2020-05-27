from django import forms

from question.models import Question, Choice
from question.definition import QuestionType, Difficulty


class ListeningQuestionForm(forms.ModelForm):
    q_file = forms.FileField(required=True)
    QUESTION_TYPES = []
    for type in QuestionType.__members__.values():
        if type.value[1] == 'Listening':
            QUESTION_TYPES.append((type.value[0], type.value[2]))
    q_type = forms.ChoiceField(required=True,
                               choices=QUESTION_TYPES,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               error_messages={'required': "Please set the type of the question."})
    DIFFICULTIES = [(_.value[0], _.value[1]) for _ in Difficulty.__members__.values()]
    difficulty = forms.ChoiceField(required=True,
                                   choices=DIFFICULTIES,
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   error_messages={'required': "Please set the difficulty of the question."})

    class Meta:
        model = Question
        fields = ['q_file', 'q_type', 'difficulty']


class ChoiceForm(forms.ModelForm):
    c_content = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Please Enter the content of the choice'}))

    def __init__(self, name):
        super().__init__()
        self.name = name

    class Meta:
        model = Choice
        fields = ['source', 'c_content']
