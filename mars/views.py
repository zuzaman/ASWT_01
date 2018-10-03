from django.http import HttpResponse
from django.shortcuts import render, redirect
from mars.models import Moon

# Create your views here.
def main(request):
	return render(request,'mars/home.html')

def result(request):
	dInterval = request.POST['deimos_interval']
	pInterval = request.POST['phobos_interval']

	moon_ = Moon.objects.create(dInterval = request.POST['deimos_interval'], pInterval= request.POST['phobos_interval'])
	moon_.process_periods()
	moon_.generalise_time()
	overlap = moon_.calculate_overlap()
	moon_.save()

	return render(request,'mars/result.html', {'overlap' : overlap})
