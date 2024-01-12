from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Rean
from .forms import PostForm
from django.shortcuts import redirect
#from django.forms.fields import BooleanField
#from django.forms.fields import CheckboxInput

MD={'file': 'main', 'nId': 0, 'nClic': 0, 'dif': 'lw', 'filter': '', 'var': ['w', 'p', 'l', 'e', 'm', 'd'], 'curId': []}

'''
мы создали переменную для QuerySet: posts. Можешь думать о ней как об имени для нашего QuerySet. Теперь мы можем обращаться к нему, используя имя.
осталось передать QuerySet posts в шаблон
'''
def post_list(request):
    global MD
    posts = Rean.objects.all() # имя QuerySet:
    data={}
    var='' if not '/post/' in str(request) else str(request).split('/')[2]
    print('var '+str(var)+' '+str())
    if var in MD['var']: # filter
        if not var in MD['filter']:
            MD['filter'] += ' '+(var)
        else:
            sp=MD['filter'].split(' ')
            ind=sp.index(var)
            sp.pop(ind)
            MD['filter']=' '.join(sp)
    if var=='start': # start
        print('start '+str()+' '+str())
    #posts = [{'content': str(MD['asd'][0])},{'content': str(MD['asd'][1])},{'content': str(MD['asd'][2])},{'content': str(MD['asd'][3])}]
    #context = {'posts': posts}
    MD['curId']=[]
    for i in posts:
        if str(i.title_dif[1]) in MD['filter']:
            if str(i.title_dif[0]) in MD['filter']:
                MD['curId'].append(str(i.id))
                print(' '+str(i.title_ru)+' '+str(i.title_dif)+' '+str(i.id))
    data=MD['filter']+' '+str(len(MD['curId']))
    return render(request, 'rean/post_list.html', {'posts': posts, 'cod': data}) # QuerySet (posts) --> post_list.html

def post_detail(request, pk):
    post = get_object_or_404(Rean, pk=pk)
    return render(request, 'rean/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # при нажатии сохранить - есть post.pk
            print('post.pk1 '+str(post.pk)+' '+str())
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'rean/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Rean, pk=pk)
    # при вызове поста - есть post.pk
    print('post.pk0 '+str(post.pk)+' '+str())
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # при нажатии сохранить - есть post.pk
            print('post.pk1 '+str(post.pk)+' '+str())
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'rean/post_edit.html', {'form': form})

def post_filter(request):
    global MD
    sdf={"header": MD['filter']}
    print(' '+str(sdf)+' '+str(v))
    return render(request, 'rean/post_base.html', context=sdf)
    
    #posts = Rean.objects.filter(title_dif__contains=MD['dif'])
    #post_filter(request, MD['filter'])
