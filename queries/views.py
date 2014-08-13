from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from forms import UploadFileForm
from models import TestQueries, TrainQueries, Words, Sessions
from django.http import HttpResponse
import random

from config import rsv_threshold
from extract import from_tsv_get, hist
from rsv import updatePtUt
import old_rsv
import old_extract

def is_relevant(line):
    return (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded')

def old_extract_data(lines, sf=None):
    words = old_extract.hist(lines)
    lins = old_extract.rel_non_rel_lines(lines)

    for word in words:
        words[word] = list(old_rsv.calculatePtUt(word,words,lins))
        words.get(word).append(old_rsv.calculateC(word, words))

    return words

def extract_data(lines, sf=None):
    words = hist(lines)
    for word in words:
        updatePtUt(word, words)


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
        add_rsv = [float(i) for i in request.POST.getlist("add_lis_rsv[]")]
        exclude_rsv = [float(i) for i in request.POST.getlist("exclude_lis_rsv[]")]


        refuse_excluded = 0
        refuse_added = 0
        confirm_excluded = 0
        confirm_added = 0



        for add in add_rsv:
            if add < rsv_threshold:
                refuse_excluded += 1
            else:
                confirm_added += 1

        for exclude in exclude_rsv:
            if exclude > rsv_threshold:
                refuse_added += 1
            else:
                confirm_excluded += 1

        print confirm_added, confirm_excluded, refuse_added, refuse_excluded
        se = Sessions(confirm_added= confirm_added, confirm_excluded=confirm_excluded,
                      refuse_added=refuse_added, refuse_excluded=refuse_excluded)
        se.save()


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
    try:
        w = Words.objects.get(word = request.POST['word']).c
    except Words.DoesNotExist:
        w = None
    return HttpResponse(w if w else "unknown")


@csrf_exempt
def get_precision(request):
    t = TrainQueries.objects.all()
    t = list(enumerate(t))

    good = 0
    bad = 0
    random.shuffle(t)

    total = len(t)

    trains = [[el.query,"Added" if el.relevant else "Excluded", 0] for i, el in t[:4 * total/5]]
    tests = [[el.query, el.relevant] for i, el in t[4 * total/5: ]]

    words = old_extract_data(trains)

    for test in tests:


        if (old_rsv.calculateRsv(test[0], words) > 1.6):
            if test[1]:
                good += 1
            else:
                bad += 1
        else:
            if test[1]:
                bad += 1
            else:
                good += 1

    return HttpResponse(str(good/float(len(tests))))


@csrf_exempt
def showSessions(request):
    sessions = Sessions.objects.all()
    return render_to_response("sessions.html", {"sessions": sessions})