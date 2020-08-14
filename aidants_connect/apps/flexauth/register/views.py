from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import qrcode.image.svg

from . import forms


User = get_user_model()

TEMPLATES_PATH = 'flexauth/register'


def register_identity(request):
    if request.method == 'POST':
        form = forms.IdentityForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session['new_user_id'] = new_user.id
            return redirect(request.POST.get('next'))
    else:
        form = forms.IdentityForm()

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'identity')
    return render(request, template_name, {
        'form': form,
        'next': 'flexauth:register_organisation',
    })


def register_organisation(request):
    try:
        new_user = User.objects.get(pk=request.session.get('new_user_id'))
    except User.DoesNotExist:
        return redirect('flexauth:register')

    if request.method == 'POST':
        form = forms.OrganisationForm(request.POST, instance=new_user)
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('next'))
    else:
        form = forms.OrganisationForm()

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'organisation')
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:register',
        'next': 'flexauth:register_first_factor',
        'new_user': new_user,
    })


def register_first_factor(request):
    try:
        new_user = User.objects.get(pk=request.session.get('new_user_id'))
    except User.DoesNotExist:
        return redirect('flexauth:register')

    if request.method == 'POST':
        form = forms.FirstFactorForm(request.POST, instance=new_user)
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('next'))
    else:
        form = forms.FirstFactorForm()

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'first_factor')
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:register_organisation',
        'next': 'flexauth:register_second_factor',
        'new_user': new_user,
    })


def register_second_factor(request):
    try:
        new_user = User.objects.get(pk=request.session.get('new_user_id'))
    except User.DoesNotExist:
        return redirect('flexauth:register')

    if request.method == 'POST':
        form = forms.SecondFactorForm(request.POST, instance=new_user)
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('next'))
    else:
        form = forms.SecondFactorForm()

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'second_factor')
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:register_first_factor',
        'next': 'flexauth:validate_second_factor',
        'new_user': new_user,
    })


def validate_second_factor(request):
    try:
        new_user = User.objects.get(pk=request.session.get('new_user_id'))
    except User.DoesNotExist:
        return redirect('flexauth:register')

    if request.method == 'POST':
        form = forms.SecondFactorValidationForm(request.POST, user=new_user)
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('next'))

    else:
        form = forms.SecondFactorValidationForm()

    template_name = "%s/%s_%s.html" % (
        TEMPLATES_PATH,
        'second_factor_validation',
        new_user.second_factor,
    )
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:register_second_factor',
        'next': 'flexauth:register_success',
        'new_user': new_user,
    })


def generate_totp_qrcode(request, totp_device_id):
    totp_device = TOTPDevice.objects.get(pk=totp_device_id)
    response = HttpResponse(content_type='image/svg+xml')
    img = qrcode.make(totp_device.config_url, image_factory=qrcode.image.svg.SvgImage)
    img.save(response)
    return response


def success(request):
    try:
        new_user = User.objects.get(pk=request.session.get('new_user_id'))
    except User.DoesNotExist:
        return redirect('flexauth:register')

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'success')
    return render(request, template_name, {})


