import json

from django.http import HttpResponse
from django.shortcuts import render
from question_answer.question_classifier import *
from question_answer.question_parser import *
from question_answer.answer_search import *

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '对不起，小助手暂时回答不了您的问题。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

handler = ChatBotGraph()
def answer_search(request):
    result_json = {}
    if request.POST:
        question = request.POST.get('enter_Question')
        answer = handler.chat_main(question)
        print("21414321")
        print(answer)
        result_json = json.dumps({
            "answer": answer,
        })
        return HttpResponse(result_json)
    return HttpResponse(result_json)
