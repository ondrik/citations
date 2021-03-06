import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from .models import Citation, Publication, PublicationCitation

# Create your views here.
# def index(request):
#     pubs = Publication.objects.order_by('-pub_date')
#     context = { 'publications': pubs }
#     return render(request, 'cites/index.html', context)

######################################
class IndexView(generic.ListView):
    """The list of publications."""
    template_name = 'cites/index.html'
    context_object_name = 'publications'

    def get_queryset(self):
        """Return all publications."""
        return Publication.objects.order_by('-pub_date')

######################################
class ManageView(generic.ListView):
    """Management of publications."""
    template_name = 'cites/manage_pubs.html'
    context_object_name = 'publications'

    def get_queryset(self):
        """Return all publications."""
        return Publication.also_deleted_objects.order_by('-pub_date')

######################################
def pub_detail(request, pk):
    pub = get_object_or_404(Publication, pk=pk)
    # citations = pub.j
    context = {
        'publication': pub,
        'citations': pub.citations.order_by('-cited_date'),
        'publications': Publication.objects.order_by('-pub_date')
    }

    return render(request, 'cites/pub_detail.html', context)

######################################
def add_pub(request):
    """Adds a new publication."""
    abbrev = request.POST["pub_abbrev"]
    abbrev = abbrev.strip()
    if not abbrev:
        return render(request, IndexView.template_name, {
            'error_message': "The abbreviation is empty.",
            # the following is horrible solution (copies functionality)
            'publications': Publication.objects.order_by('-pub_date'),
        })

    title = request.POST["pub_title"]
    title = title.strip()
    if not title:
        return render(request, IndexView.template_name, {
            'error_message': "The title is empty.",
            # the following is horrible solution (copies functionality)
            'publications': Publication.objects.order_by('-pub_date'),
        })

    newPub = Publication()
    newPub.title = title
    newPub.abbrev = abbrev
    newPub.save()

    return redirect(reverse('cites:index'))

######################################
def add_cit(request, pk):
    """Adds a new citation."""
    title = request.POST["cit_title"]
    title = title.strip()
    pub = get_object_or_404(Publication, pk=pk)
    if not title:
        # the following is horrible solution (copies functionality)
        return render(request, 'cites/pub_detail.html', {
            'error_message': "The title is empty.",
            'publication': pub,
            'citations': pub.citations.all(),
            'publications': Publication.objects.order_by('-pub_date')
        })

    str_year = request.POST["cit_year"]
    str_year = str_year.strip()
    error = False
    try:
        year = int(str_year)
        if year < 2000 or year > 2100:
            error = True
    except:
        error = True

    if error:
        # the following is horrible solution (copies functionality)
        return render(request, 'cites/pub_detail.html', {
            'error_message': "The year is invalid.",
            'publication': pub,
            'citations': pub.citations.all(),
            'publications': Publication.objects.order_by('-pub_date')
        })

    newCit = Citation()
    newCit.title = title
    newCit.cited_date = datetime.date(year, 6, 6)
    newCit.save()

    all_pubs = [ pub ]
    other_pubs = request.POST.getlist('also-pubs-checks[]')
    for x in other_pubs:
        tmp_pub = get_object_or_404(Publication, pk=x)
        all_pubs.append(tmp_pub)
        # return HttpResponse("LaLa" + tmp_pub.__str__())

    # return HttpResponse("Ahoj" + all_pubs.__str__())

    # add all bindings
    for x in all_pubs:
        binding = PublicationCitation(publication=x, citation=newCit)
        binding.save()

    return redirect(reverse('cites:pub_detail', args=({pk})))

######################################
def del_cit(request, pub_pk, cit_pk):
    cit = get_object_or_404(PublicationCitation, publication=pub_pk, citation=cit_pk)
    cit.delete()
    return redirect(reverse('cites:pub_detail', args=({pub_pk})))


######################################
def del_pub(request, pk):
    try:
        pub = Publication.also_deleted_objects.get(pk=pk)
    except Publication.DoesNotExist:
        raise Http404("Publication does not exist")

    if not pub.deleted:
        pub.deleted = True
    else:
        pub.deleted = False

    pub.save()
    return redirect(reverse('cites:manage_pubs', ))


######################################
def cit_list_year(request):
    citations = PublicationCitation.objects.all()

    cit_map = { }
    totals = { }
    for cit in citations:
        year = cit.citation.cited_date.year
        if not year in cit_map:
            cit_map[year] = { }

        if not cit.publication in cit_map[year]:
            cit_map[year][cit.publication] = []

        cit_map[year][cit.publication].append(cit.citation)

        if not year in totals:
            totals[year] = 0

        totals[year] += 1

    context = {
        'cit_list': [(k, cit_map[k]) for k in sorted(cit_map, reverse=True)],
        'totals': totals,
    }

    return render(request, 'cites/cit_list_year.html', context)


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
