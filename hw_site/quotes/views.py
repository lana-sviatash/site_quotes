from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag

from bson import ObjectId
from .utils import get_mongodb

# # Create your views here.
def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
# def main(request, page=1):
#     quotes = Quote.objects.all()
#     per_page = 10
#     paginator = Paginator(quotes, per_page)
#     quotes_on_page = paginator.get_page(page)
#     return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
    else:
        form = AuthorForm()
    
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            author = form.cleaned_data['author']

            tags_input = str(form.cleaned_data['tags'])

            tags_list = [tag.strip() for tag in tags_input.split(',')]
            
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]

            quote = Quote(quote=quote_text, author=author)
            quote.save()
            # for tag in tags:
            #     quote.tags.add(tag)
            tags_to_add = [tag for tag in tags if tag not in quote.tags.all()]
            quote.tags.add(*tags_to_add)

            return redirect(reverse('quotes:root'))

    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})



@login_required
def delete_quote(request, id_):
    try:
        quote = Quote.objects.get(id=id_)
        quote.delete()
    except Quote.DoesNotExist:
        pass
    return redirect('quotes:root')


# def author_detail(request, id_):
#     author = get_object_or_404(Author, id=id_)
#     return render(request, 'quotes/author_detail.html', context={'author': author})

def author_detail(request, id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return render(request, 'quotes/author_detail.html', context={'author': author})


