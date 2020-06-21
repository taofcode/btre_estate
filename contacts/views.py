from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing  = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone= request.POST['phone']
        user_id= request.POST['user_id']
        realtor_email= request.POST['realtor_email']
        print(realtor_email)
        message = request.POST['message']
        # check if enquiry already made
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an enquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,
        phone=phone,message=message,user_id=user_id )
        contact.save()

        # Send mail
        send_mail(
             subject='Property Listing Inqury',
              message='There has been an inqury for '+ listing + 'Sign into the admin panel for more info',
              from_email='kuverengamari@gmail.com',
              recipient_list=[realtor_email,'taofcode@gmail.com'],
              fail_silently=False


        )

        messages.success(request,'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)

