from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .forms import ProfileUpdateForm, RegisterForm
from .models import PendingSignup, Profile

User = get_user_model()


def _send_profile_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirm_url = request.build_absolute_uri(
        reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
    )
    subject = "Confirmation de votre adresse email"
    message = render_to_string(
        "registration/email_confirmation.txt",
        {
            "user": user,
            "confirm_url": confirm_url,
            "site_name": "EMI Shop",
        },
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def _send_signup_confirmation_email(request, pending_signup):
    confirm_url = request.build_absolute_uri(
        reverse('confirm_signup', kwargs={'token': str(pending_signup.token)})
    )
    subject = "Confirmez la creation de votre compte"
    message = render_to_string(
        "registration/signup_confirmation.txt",
        {
            "pending_signup": pending_signup,
            "confirm_url": confirm_url,
            "site_name": "EMI Shop",
        },
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pending_signup.email],
        fail_silently=False,
    )


def _get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def _clear_expired_pending_signups():
    PendingSignup.objects.filter(expires_at__lt=timezone.now()).delete()


def signup(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    _clear_expired_pending_signups()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            PendingSignup.objects.filter(
                username=form.cleaned_data["username"]
            ).delete()
            PendingSignup.objects.filter(
                email=form.cleaned_data["email"]
            ).delete()

            pending_signup = PendingSignup.objects.create(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password_hash=make_password(form.cleaned_data["password1"]),
            )
            _send_signup_confirmation_email(request, pending_signup)
            request.session["pending_signup_email"] = pending_signup.email
            messages.success(request, "Un email de confirmation a ete envoye. Votre compte sera cree apres validation.")
            return redirect("signup_pending")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    return render(
        request,
        "registration/profile.html",
        {"profile_state": _get_profile(request.user)},
    )


@login_required
def edit_profile(request):
    profile_state = _get_profile(request.user)
    initial_email = request.user.email

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            if user.email != initial_email:
                profile_state.email_verified = False
                profile_state.save(update_fields=['email_verified', 'updated_at'])
                _send_profile_confirmation_email(request, user)
                messages.info(request, "Votre email a change. Merci de confirmer la nouvelle adresse.")
            messages.success(request, "Votre profil a ete mis a jour.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        "registration/edit_profile.html",
        {"form": form, "profile_state": profile_state},
    )


@login_required
def resend_confirmation_email(request):
    if request.method != "POST":
        raise Http404()

    profile_state = _get_profile(request.user)
    if profile_state.email_verified:
        messages.info(request, "Votre adresse email est deja confirmee.")
    elif not request.user.email:
        messages.error(request, "Ajoutez d'abord une adresse email dans votre profil.")
    else:
        _send_profile_confirmation_email(request, request.user)
        messages.success(request, "Un nouvel email de confirmation a ete envoye.")
    return redirect('profile')


def signup_pending(request):
    return render(
        request,
        "registration/signup_pending.html",
        {"pending_signup_email": request.session.get("pending_signup_email")},
    )


def resend_signup_confirmation(request):
    if request.method != "POST":
        raise Http404()

    pending_email = request.session.get("pending_signup_email")
    if not pending_email:
        messages.error(request, "Aucune inscription en attente n'a ete retrouvee dans cette session.")
        return redirect('signup')

    pending_signup = PendingSignup.objects.filter(email=pending_email).first()
    if pending_signup is None:
        messages.error(request, "Cette inscription en attente est introuvable ou a expire.")
        return redirect('signup')

    if pending_signup.is_expired():
        pending_signup.delete()
        messages.error(request, "Le lien a expire. Merci de refaire votre inscription.")
        return redirect('signup')

    _send_signup_confirmation_email(request, pending_signup)
    messages.success(request, "Le mail de confirmation a ete renvoye.")
    return redirect('signup_pending')


def confirm_signup(request, token):
    pending_signup = PendingSignup.objects.filter(token=token).first()
    if pending_signup is None:
        messages.error(request, "Le lien de confirmation est invalide.")
        return redirect('signup')

    if pending_signup.is_expired():
        pending_signup.delete()
        messages.error(request, "Le lien de confirmation a expire. Merci de refaire votre inscription.")
        return redirect('signup')

    if User.objects.filter(username=pending_signup.username).exists() or User.objects.filter(email=pending_signup.email).exists():
        pending_signup.delete()
        messages.error(request, "Un compte existe deja avec ces informations. Connectez-vous directement.")
        return redirect('login')

    user = User.objects.create(
        username=pending_signup.username,
        email=pending_signup.email,
        is_active=True,
    )
    user.password = pending_signup.password_hash
    user.save()

    profile_state = _get_profile(user)
    if not profile_state.email_verified:
        profile_state.email_verified = True
        profile_state.save(update_fields=['email_verified', 'updated_at'])

    pending_signup.delete()
    request.session.pop("pending_signup_email", None)
    login(request, user)
    messages.success(request, "Votre email est confirme et votre compte a ete cree avec succes.")
    return redirect('product_list')


def confirm_email(request, uidb64, token):
    from django.utils.encoding import force_str
    from django.utils.http import urlsafe_base64_decode

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profile_state = _get_profile(user)
        if not profile_state.email_verified:
            profile_state.email_verified = True
            profile_state.save(update_fields=['email_verified', 'updated_at'])
        messages.success(request, "Votre adresse email a bien ete confirmee.")
        if request.user.is_authenticated:
            return redirect('profile')
        return redirect('login')

    messages.error(request, "Le lien de confirmation est invalide ou a expire.")
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')
