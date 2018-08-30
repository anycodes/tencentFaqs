from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import faqs.models
import faqs.Recommended
# Create your views here.


def trans(request):
    try:
        my_bot = ChatBot("apioss")
        my_bot.set_trainer(ListTrainer)

        for eveQuesAns in faqs.models.QAData.objects.all():
            my_bot.train([
                eveQuesAns.question,
                eveQuesAns.answer
            ])
        result = {
            "code":"0",
            "message":"success"
        }
    except Exception as e:
        result = {
            "code": "-1",
            "message": str(e)
        }
    return JsonResponse(result)

@csrf_exempt
def index(request):

    token = request.GET.get("token")

    if request.method == "POST":
        inputData = request.POST.get("s")
        if inputData:
            my_bot = ChatBot("apioss", read_only=True)
            resultTitle = "最佳匹配结果"
            resultContent = my_bot.get_response(inputData)
            docTextList = []
            docText = []
            allData = faqs.models.QAData.objects.all()
            for eve in allData:
                if eve.answer != resultContent:
                    docTextList.append((eve.qid,eve.question))
            listData = faqs.Recommended.RecommendedHandle(numCount=4).getArticleList(inputData,docTextList)
            resultList = []
            for eve in listData:
                resultList.append(allData.get(qid=eve))
            searchSt = 1
    else:
        listData =faqs.models.QAData.objects.all().order_by("?")[0:5]

        resultTitle = listData[0].question
        resultContent = listData[1].answer
        resultList = listData[1:]


    return render(request, "faq.html", locals())
