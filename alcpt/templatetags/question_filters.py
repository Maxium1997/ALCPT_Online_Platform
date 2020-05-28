from django import template

from question.definition import QuestionType, State, Difficulty

register = template.Library()


@register.filter(name='readableQuestionType')
def readableQuestionType(value):
    for q_type in QuestionType.__members__.values():
        if value == q_type.value[0]:
            return q_type.value[2]


@register.filter(name='readableQuestionState')
def readableQuestionState(value):
    for state in State.__members__.values():
        if value == state.value[0]:
            return state.value[1]


@register.filter(name='readableDifficulty')
def readableDifficulty(value):
    for difficulty in Difficulty.__members__.values():
        if value == difficulty.value[0]:
            return difficulty.value[1]
