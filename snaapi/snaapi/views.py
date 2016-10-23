from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from snaapi.models import WeddingPicture

@csrf_exempt
def wedding_pictures(request):
    response = {'wedding_pictures': []}

    for p in WeddingPicture.objects.filter(approved=True).order_by('capture_date'):
        response['wedding_pictures'].append({
            'url': p.picture.url,
            'capture_date': p.capture_date,
            'upload_date': p.upload_date,
            'owner': p.owner,
        })

    return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')