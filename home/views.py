from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from newmaterial.models import Publishmaterial
from check_in_out.models import check_in_out
from datetime import timedelta
import datetime


@login_required(login_url='/accounts/login/')
def home(req):

    book_count = check_in_out.objects.filter(user=req.user, book_id__material_id__material_type='book', is_returned=False).count()
    magazine_count = check_in_out.objects.filter(user=req.user, book_id__material_id__material_type='magazine', is_returned=False).count()

    context = {
        'materials': Publishmaterial.objects.all().order_by('material_id__title'),
        'book_count': book_count,
        'magazine_count': magazine_count,
        'type': 'books or magazines',
        'response': 'Books and magazines',
    }
    return render(req, 'home.html', context)

@login_required(login_url='/accounts/login/')
def books(req):
    context = {
        # 'materials': newmaterial.objects.filter(material_type='book').order_by('-quantity_available','title'),
        'materials': Publishmaterial.objects.filter(material_id__material_type='book').order_by('material_id__title'),
        'type': 'books',
        'response': 'Books',
    }
    return render(req, 'home.html', context)

@login_required(login_url='/accounts/login/')
def magazines(req):
    context = {
        'materials': Publishmaterial.objects.filter(material_id__material_type='magazine').order_by('material_id__title'),
        'type': 'magazines',
        'response': 'Magazines'
    }
    return render(req, 'home.html', context)

@login_required(login_url='/accounts/login/')
def my_checkouts(req):

    user_loans = check_in_out.objects.filter(user=req.user, is_returned=False)

    book_count = check_in_out.objects.filter(user=req.user, book_id__material_id__material_type='book', is_returned=False).count()
    magazine_count = check_in_out.objects.filter(user=req.user, book_id__material_id__material_type='magazine', is_returned=False).count()

    context = {
        'user_loans': user_loans,
        'book_count': book_count,
        'magazine_count': magazine_count,
    }
    return render(req, 'my_checkouts.html', context)

@login_required(login_url='/accounts/login/')
def expired_checkouts(req):
    current_date = datetime.datetime.now()

    expired_material = check_in_out.objects.filter(checked_in_datetime__lt=current_date, is_returned=False).order_by('checked_in_datetime')

    context = {
        'date': datetime.datetime.now(),
        'expired_materials': expired_material,
    }
    is_user_staff = req.user.is_staff
    if is_user_staff: ### Check if user is staff member
        pass
    else:
        return HttpResponseRedirect(reverse('home:home'))

    return render(req, 'expired_checkouts.html', context)
