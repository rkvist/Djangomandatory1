from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import check_in_out
from newmaterial.models import Publishmaterial, newmaterial
from datetime import datetime, timedelta

@login_required(login_url='/account/login/')
def check_out(req):
    if req.method == 'POST':
        user_id = req.user
        book_post = req.POST['material_id']
        data_post = req.POST['material_data']
        book_id = Publishmaterial.objects.filter(id=book_post)
        book_data = newmaterial.objects.filter(id=data_post)

        current_checked_out_books = check_in_out.objects.filter(user=req.user, is_returned=False, book_id__material_id__material_type='book').count()
        current_checked_out_magazines = check_in_out.objects.filter(user=req.user, is_returned=False, book_id__material_id__material_type='magazine').count()

        if current_checked_out_books == 10 and current_checked_out_magazines == 3:
            print('The limit checked out is 10 books and 3 magazines')
        else:
            if book_data[0].material_type == 'book' and current_checked_out_books == 10 or book_data[0].material_type == 'magazine' and current_checked_out_magazines == 3:
                print('The user has reached the limit of books or magazines')
            else:
                current_date = datetime.now()

                does_user_have_expired_material = check_in_out.objects.filter(user=user_id, checked_in_datetime__lt=current_date, is_returned=False).exists()
                if does_user_have_expired_material:
                    print('You have a book(s) or magazine(s) which are extended past the expiration date. ')
                else:
                    current_date = datetime.now()

                    if book_data[0].material_type == 'magazine':
                        return_date = current_date+timedelta(days=7)
                    else:
                        return_date = current_date+timedelta(days=30)

                    check_out = check_in_out()
                    check_out.user = user_id
                    check_out.book_id = book_id[0]
                    check_out.checked_in_datetime = return_date
                    check_out.save()

                    book_loaned = Publishmaterial.objects.get(id=book_post)
                    book_loaned.is_loaned = True
                    book_loaned.save()

        return HttpResponseRedirect(reverse('home:home'))

@login_required(login_url='/account/login/')
def check_in(req):
    if req.method == 'POST':
        user_id = req.user
        loan_id = req.POST['loan_id']
        loan_data = check_in_out.objects.filter(id=loan_id)[0]

        if user_id == loan_data.user: 
                loan_data.is_returned = True
                loan_data.save()
                loan_published_material_id = loan_data.book_id.id
                loan_published_material = Publishmaterial.objects.filter(id=loan_published_material_id)[0]
                loan_published_material.is_loaned = False
                loan_published_material.save()
        else:
            print('This is not a loan that the authenticated user has made.')

    return HttpResponseRedirect(reverse('home:my_checkouts'))
