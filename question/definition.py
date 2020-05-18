from enum import Enum


class QuestionType(Enum):
    QA = (1, 'Listening', 'QA')
    ShortConversation = (2, 'Listening', 'Conversation')
    Grammar = (3, 'Reading', 'Grammar')
    Phrase = (4, 'Reading', 'Phrase')
    ParagraphUnderstanding = (5, 'Reading', 'ParagraphUnderstanding')


class ExamType(Enum):
    MockExam = (1, 'Mock Exam')
    Practice = (2, 'Practice')
    Listening = (3, 'Listening')
    Reading = (4, 'Reading')


class Difficulty(Enum):
    Simple = (1, 'Simple')
    Moderate = (2, 'Moderate')
    Difficult = (3, 'Difficult')


class State(Enum):
    Saved = (1, 'Saved')
    Pending = (2, 'Pending')
    Passed = (3, 'Passed')
    Rejected = (4, 'Rejected')
    Faulty = (5, 'Faulty')
    Handled = (6, 'Handled')
