import yaml
from pprint import pprint
import argparse
from enum import Enum
from typing import Dict, List, Union


class QuestionType(Enum):
    FREE_RESPONSE = 0
    MULTIPLE_CHOICE = 1
    MATCHING = 2
    UNKNOWN = 3


QuestionTypeDict = {
    'FREE RESPONSE': QuestionType.FREE_RESPONSE,
    'MATCHING': QuestionType.MATCHING,
    'MULTIPLE CHOICE': QuestionType.MULTIPLE_CHOICE,
}

QuestionTypeDictReversed = {v: k for k, v in QuestionTypeDict.items()}


def promptYN() -> bool:
    """Get y/n from a user."""
    while True:
        answer = input('[Yy]es/[Nn]o \n > ')

        if answer[0].capitalize() == 'Y':
            return True
        if answer[0].capitalize() == 'N':
            return False


class Question:
    def __init__(self, data):
        self.data = data
        self.answered = False
        self.answer = None
        self.correct = False

    @staticmethod
    def validate_free_response(correct_answers: List[str], proposed_answer: str) -> bool:
        """Given a list of correct answers and 1 proposed answer, return True if the answer exists in the list of correct answers."""
        answers_uppercase = [x.upper() for x in correct_answers]
        proposed_answer_u = proposed_answer.upper()

        if proposed_answer_u in answers_uppercase:
            return True

        return False

    @staticmethod
    def validate_matching_response(correct_mappings: Dict[str, str],
                                   proposed_mappings: Dict[str, str]) -> Dict[str, str]:
        """Given a list of proposed mappings of a matching question response, return a mapping of incorrect answers.
        If the returned mapping is empty, then all answers are correct."""

        incorrect_mappings = {}

        for key in correct_mappings:
            if not (correct_mappings[key] == proposed_mappings[key]):
                incorrect_mappings[key] = proposed_mappings[key]

        return incorrect_mappings

    def printQuestionHeader(self):
        print('-' * 30)
        print(f"Type:       {self.getQuestionTypePretty()}")
        print(f"Question:   {self.getTitle()}")

    def printAnswersAsList(self):
        for s in self.getAnswers():
            print(f"- {s}")

    def askMatchingQuestion(self):
        """Ask a matching question to stdin and store results in myself."""
        print("fml. implement me.")

        print("Match the alphabetic items to the numeric items.")

        pprint(self.getAnswers())

        exit(1)

    def askFreeResponseQuestion(self):
        """Ask a free response question to stdin and store results in myself."""
        user_input = input(" > ")

        if self.validate_free_response(self.getAnswers(), user_input):
            self.correct = True
            self.answered = True
            self.answer = user_input
            print(f"Correct! You answered '{user_input}'. The correct answers were:")
            self.printAnswersAsList()

        else:
            print("These were the correct answers:")
            self.printAnswersAsList()
            print("You may be potentially incorrect, but I cannot tell as I'm just a computer.")
            print(f"Did your answer of '{user_input}' match the above answers enough to be counted as a correct "
                  f"answer? Please be honest.")
            self.correct = promptYN()
            self.answered = True
            self.answer = user_input

    def askQuestion(self):
        """Ask a question to stdin and store results in myself."""

        self.printQuestionHeader()

        if self.getQuestionType() == QuestionType.FREE_RESPONSE:
            self.askFreeResponseQuestion()

        if self.getQuestionType() == QuestionType.MATCHING:
            self.askMatchingQuestion()

        if self.getQuestionType() == QuestionType.MULTIPLE_CHOICE:
            print("Todo implement asking user to answer MULTIPLE_CHOICE question")
            exit(1)

        if self.getQuestionType() == QuestionType.UNKNOWN:
            print("lol you need to fix this question:")
            print(self)
            exit(1)

    def __str__(self):
        return f"""{self.getTitle()}
Type: {self.getQuestionType().name}"""

    def getTitle(self) -> str:
        return self.data['title']

    def getAnswers(self) -> List:
        return self.data['answers']

    def getQuestionTypeRaw(self) -> str:
        return self.data['type']

    def getQuestionTypePretty(self) -> str:
        return self.getQuestionTypeRaw().lower().capitalize()

    def getQuestionType(self) -> QuestionType:
        if self.getQuestionTypeRaw().upper() in QuestionTypeDict:
            return QuestionTypeDict[self.getQuestionTypeRaw().upper()]

        return QuestionType.UNKNOWN


class QuestionBank():
    def __init__(self, questions=None):
        if questions is None:
            questions = []

        self.questions = questions

    def add_question(self, question: Question):
        self.questions.append(question)

    def run_quiz(self):
        for question in self.questions:
            if not question.answered:
                question.askQuestion()


if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--file", required=True, help="Quiz datafile")

    # Read arguments from command line
    args = parser.parse_args()

    print("Using quiz file " + args.file)

    with open(args.file) as f:
        quizYaml = yaml.load(f, Loader=yaml.UnsafeLoader)

    questionBank = QuestionBank()

    for questionData in quizYaml['questions']:
        question = Question(data=questionData)
        questionBank.add_question(question)
        # print(question)

    questionBank.run_quiz()

    exit(0)
