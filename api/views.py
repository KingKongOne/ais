from django.http import JsonResponse
from django.contrib.auth.models import Group
from exhibitors.models import Exhibitor
from events.models import Event
from news.models import NewsArticle
from fair.models import Partner
import api.serializers as serializers


CURRENT_FAIR = 'Armada 2016'


def root(request):
    return JsonResponse({'message': 'Welcome to the Armada API!'})


def exhibitors(request):
    exhibitors = Exhibitor.objects.filter(
            fair__name=CURRENT_FAIR
            ).select_related('cataloginfo').prefetch_related(
                'cataloginfo__programs',
                'cataloginfo__main_work_field',
                'cataloginfo__work_fields',
                'cataloginfo__job_types',
                'cataloginfo__continents',
                'cataloginfo__values',
            )
    data = [serializers.exhibitor(request, exhibitor.cataloginfo)
            for exhibitor in exhibitors]
    return JsonResponse(data, safe=False)


def events(request):
    events = Event.objects.filter(published=True)
    data = [serializers.event(request, event) for event in events]
    return JsonResponse(data, safe=False)


def news(request):
    news = NewsArticle.public_articles.all()
    data = [serializers.newsarticle(request, article) for article in news]
    return JsonResponse(data, safe=False)


def partners(request):
    partners = Partner.objects.filter(
            fair__name=CURRENT_FAIR
            ).order_by('-main_partner')
    data = [serializers.partner(request, partner) for partner in partners]
    return JsonResponse(data, safe=False)


def organization(request):
    groups = Group.objects \
            .prefetch_related('user_set__profile') \
            .order_by('name')
    data = [serializers.organization_group(request, group) for group in groups]
    return JsonResponse(data, safe=False)
