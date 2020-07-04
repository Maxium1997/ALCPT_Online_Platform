from django import forms

from question.models import Question, Choice
from question.definition import QuestionType, Difficulty, State


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


class ListeningQuestionEditForm(forms.ModelForm):
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
        fields = ['q_type', 'difficulty']


class ReadingQuestionForm(forms.ModelForm):
    q_content = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control',
                                                             'rows': '5',
                                                             'placeholder': 'Enter the content of the question'}))
    QUESTION_TYPES = []
    for type in QuestionType.__members__.values():
        if type.value[1] == 'Reading':
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
        fields = ['q_content', 'q_type', 'difficulty']


class ChoiceForm(forms.ModelForm):
    c_content = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Please Enter the content of the choice'}))

    class Meta:
        model = Choice
        exclude = ['source']


class RejectReasonForm(forms.Form):
    faulty_reason = forms.CharField(required=True,
                                    widget=forms.Textarea(attrs={'class': 'form-control',
                                                                 'rows': '5'}))

    class Meta:
        fields = ['faulty_reason']


class QuestionFilterForm(forms.Form):
    content = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 float-left',
                                                            'placeholder': 'Filter by question content'}))
    QUESTION_TYPES = [('', 'Filter by type')] + [(_.value[0], _.value[2]) for _ in QuestionType.__members__.values()]
    type = forms.ChoiceField(required=False,
                             choices=QUESTION_TYPES,
                             widget=forms.Select(attrs={'class': 'form-control custom-select col-lg-2 float-left'}))
    STATES = [('', 'Filter by state')] + [(_.value[0], _.value[1]) for _ in State.__members__.values()]
    state = forms.ChoiceField(required=False,
                              choices=STATES,
                              widget=forms.Select(attrs={'class': 'form-control custom-select col-lg-2 float-left'}))
