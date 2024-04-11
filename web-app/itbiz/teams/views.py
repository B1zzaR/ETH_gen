from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView


def teams_home(request):
    team = Articles.objects.order_by('-date')
    return render(request, "teams/teams_home.html", {'team': team})

class TeamDetailView(DetailView):
    model = Articles
    template_name = 'teams/details_view.html'
    context_object_name = 'article'


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'


    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, "teams/create.html", data)