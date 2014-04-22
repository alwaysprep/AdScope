from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import UploadFileForm
from models import TestQueries, TrainQueries, Words
from nltk.corpus import wordnet
from django.http import HttpResponse

from extract import from_tsv_get, hist
from rsv import updatePtUt


def is_relevant(line):
    return (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded')



def extract_data(lines, sf=None):
    words = hist(lines)
    for word in words:
        updatePtUt(word, words)



def isEnglish(sentence, words):
    sentenceList = sentence.split()
    for word in sentenceList:
        if not wordnet.synsets(word) :
            if sum(words.get(word,[0,0])[:2]) < 3:
                return False
    return True


# Create your views here.
def handle_uploaded_file(f):
    with open('data.tsv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    train, test = list(from_tsv_get(("data.tsv",), "\t", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

    train = [line for line in train if not TrainQueries.objects.filter(query = line[0]).exists()]

    extract_data(train)

    for line in train:
        t = TrainQueries(
            query = line[0],
            relevant = is_relevant(line)
        )
        t.save()

    for line in test:

        if TestQueries.objects.filter(query = line[0]).exists():
            continue

        ws = line[0].split()

        r = 0
        for w in ws:
            try:
                r += Words.objects.get(word = w).c
            except Words.DoesNotExist:
                pass

        t = TestQueries(
            query = line[0],
            processed = False,
            rsv = r
        )
        t.save()








@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            suggested_adds = TestQueries.objects.all().order_by("-rsv")[:10]
            suggested_excludes = TestQueries.objects.all().order_by("rsv")[:10]
            for sa in suggested_adds:
                sa.query = sa.query.split()

            for se in suggested_excludes:
                se.query = se.query.split()

            return render_to_response('connect-lists.html',
                                      {"suggested_adds":suggested_adds,"suggested_excludes":suggested_excludes})
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})


@csrf_exempt
def choose(request):
    if request.method == "POST":

        adds = request.POST.getlist("add_lis[]")
        excludes = request.POST.getlist("exclude_lis[]")
        nones = request.POST.getlist("none_lis[]")

        train = []
        for el in adds:
            print el
            tq = TestQueries.objects.get(id=int(el))

            train.append([tq.query, "Added", 0])
            tq.delete()

        for el in excludes:
            tq = TestQueries.objects.get(id=int(el))
            train.append([tq.query, "Excluded", 0])
            tq.delete()


        extract_data(train)

        for el in nones:
            tq = TestQueries.objects.get(id=int(el))
            tq.processed = True
            tq.save()

        for line in train:
            t = TrainQueries(
                query = line[0],
                relevant = is_relevant(line)
            )
            t.save()


        suggested_adds = TestQueries.objects.filter(processed=False).order_by("-rsv")[:10]

        suggested_excludes = TestQueries.objects.filter(processed=False).order_by("rsv")[:10]


        for sa in suggested_adds:
            sa.query = sa.query.split()

        for se in suggested_excludes:
            se.query = se.query.split()

        print suggested_excludes
        return render_to_response('partial.html', {"suggested_adds":suggested_adds,"suggested_excludes":suggested_excludes})


    suggested_adds = TestQueries.objects.filter(processed=False).order_by("-rsv")[:10]
    suggested_excludes = TestQueries.objects.filter(processed=False).order_by("rsv")[:10]
    for sa in suggested_adds:
        sa.query = sa.query.split()

    for se in suggested_excludes:
        se.query = se.query.split()

    return render_to_response('connect-lists.html',
                                      {"suggested_adds":suggested_adds,"suggested_excludes":suggested_excludes})


@csrf_exempt
def get_word_c(request):
    w = request.POST['word']
    return HttpResponse(Words.objects.get(word=w).c)
