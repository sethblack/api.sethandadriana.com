from django.core.serializers.json import DjangoJSONEncoder
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from snaapi.models import UploadCode, WeddingPicture

class WeddingPictureForm(ModelForm):
    class Meta:
        model = WeddingPicture
        fields = ['owner', 'picture',]

@csrf_exempt
def wedding_pictures(request):
    response = {'wedding_pictures': []}

    for p in WeddingPicture.objects.filter(approved=True).order_by('capture_date'):
        response['wedding_pictures'].append({
            'url': p.picture.url,
            'thumbnail_url': p.thumbnail.url,
            'capture_date': p.capture_date,
            'upload_date': p.upload_date,
            'owner': p.owner,
        })

    return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

@csrf_exempt
def upload_wedding_pictures(request):
    upload_code = request.POST.get('upload_code', None)

    try:
        uc = UploadCode.objects.get(code=upload_code)
    except UploadCode.DoesNotExist:
        return HttpResponse(dumps({'error': 'Invalid upload code.'}, cls=DjangoJSONEncoder), content_type='application/json')

    files = request.FILES.getlist('wedding_pics')

    for f in files:
        form = WeddingPictureForm({'owner': uc.full_name}, {'picture': f})
        form.save()

    return HttpResponse(dumps({'status': 'Done.'}, cls=DjangoJSONEncoder), content_type='application/json')