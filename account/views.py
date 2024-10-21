from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from random import randint, choice, shuffle
from string import ascii_letters, digits, punctuation
from jdatetime import datetime, timedelta
from django.contrib.auth import login, logout
from .models import User, EmailNotification
from product.models import Product
from .forms import UserUpdateProfileForm
from django.contrib.auth import update_session_auth_hash
from shop.sms import LOGIN_VERIFICATION, send_sms


def validate_phone(request, phone: str) -> int:
    if not phone:
        messages.error(request, 'شماره تلفن مورد نیاز است.')
        return 0
    if len(phone) != 11:
        messages.error(request, 'شماره تلفن را به صورت 11 رقمی وارد کنید.')
        return 0
    if not phone.isdigit():
        messages.error(request, 'شماره تلفن فقط شامل اعداد می باشد.')
        return 0
    if not phone.startswith('09'):
        messages.error(request, 'شماره تلفن باید با 09 آغاز شود.')
        return 0
    try:
        return User.objects.get(phone=phone).id
    except User.DoesNotExist:
        pass

    return -1


def generate_password() -> str:
    password = [choice(ascii_letters) + choice(digits) + choice(punctuation) for _ in range(5)]
    shuffle(password)
    return ''.join(password)


# persian_to_english_mapping = {
#     '۰': '0',
#     '۱': '1',
#     '۲': '2',
#     '۳': '3',
#     '۴': '4',
#     '۵': '5',
#     '۶': '6',
#     '۷': '7',
#     '۸': '8',
#     '۹': '9'
# }
#
#
# def convert_persian_to_english_number(persian_number: str) -> str:
#     print('persian number', persian_number)
#     if isinstance(persian_number, str):
#         english_number = ''.join(persian_to_english_mapping.get(char, char) for char in persian_number)
#         return english_number
#     return '000000'

@login_required
def logout_view(request):
    cart = request.session['cart']
    logout(request)
    request.session['cart'] = cart
    request.session.modified = True
    messages.info(request, 'شما از حسابتان خارج شدید.')
    return redirect('account:login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    if request.method == 'POST':
        phone = request.POST.get('username', None)
        user_id = validate_phone(request, phone)
        if user_id != 0:
            expire = datetime.now() + timedelta(minutes=2)
            request.session['auth'] = {'id': user_id, 'phone': phone, 'token': str(randint(100000, 999999)),
                                       'time': expire.strftime('%Y-%m-%dT%H:%M:%S')}
            request.session.modified = True
            send_sms(LOGIN_VERIFICATION, request.session['auth']['phone'], code=request.session['auth']['token'])
            return redirect('account:verify')
    return render(request, 'account-login.html')


def verify_view(request):
    if not request.session.get('auth', None):
        return redirect('account:login')
    if request.method == 'POST':
        try:
            auth = request.session['auth']
            if request.POST.get('token', None) == auth['token']:
                if datetime.now() > datetime.strptime(auth['time'], '%Y-%m-%dT%H:%M:%S'):
                    messages.error(request, 'کد تایید منقضی شده است لطفا دوباره تلاش کنید.')
                    del auth
                    return redirect('account:login')
                if auth['id'] == -1:
                    user = User(
                        phone=auth['phone'],
                        first_name='بدون',
                        last_name='نام'
                    )
                    user.set_password(generate_password())
                    user.save()
                else:
                    user = User.objects.get(id=auth['id'])
                del request.session['auth']
                session = request.session
                login(request, user)
                request.session = session
                request.session.modified = True
                next_page = request.session.get('next_page', None)
                if next_page is not None:
                    print('redirecting to', next_page)
                    del request.session['next_page']
                    return redirect(next_page)
                return redirect('shop:home')
            messages.error(request, 'کد تایید اشتباه است.')
        except Exception as e:
            print('Exception', e)
            messages.error(request, 'مشکلی پیش آمد لطفا دوباره تلاش کنید.')
            return redirect('account:login')
    return render(request, 'verify-code.html')


def add_to_notifications_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if email is not None:
            try:
                EmailNotification.objects.create(email=email)
            except Exception as e:
                print('Exception', e)
    return redirect('shop:home')


@login_required
def profile_view(request):
    user = request.user  # Get the current logged-in user

    # Store session data before making any changes
    session_data = request.session.get('cart')

    if request.method == 'POST':
        form = UserUpdateProfileForm(request.POST, instance=user)  # Bind form with POST data and current user instance

        # Check if the form is valid
        if form.is_valid():
            # Check if current password is provided for password change
            current_password = request.POST.get('password')
            new_password1 = form.cleaned_data.get('password1')
            new_password2 = form.cleaned_data.get('password2')

            if current_password and user.check_password(current_password):
                # If current password is correct, check new password fields
                if new_password1 and new_password1 != new_password2:
                    messages.error(request, 'رمز عبور جدید و تأیید رمز عبور مطابقت ندارد.')
                    return redirect('account:profile')  # Redirect after error

                elif new_password1:  # Only set a new password if it's provided
                    user.set_password(new_password1)
                    update_session_auth_hash(request, user)  # Keep the user logged in after password change

            elif current_password:  # If current password was provided but is incorrect
                messages.error(request, 'رمز عبور فعلی نادرست است.')
                return redirect('account:profile')  # Redirect after error

            # Save other fields regardless of whether the password was changed or not
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت تغییر یافت.')

            request.session['cart'] = session_data  # Restore saved session data
            request.session.modified = True

            return redirect('account:profile')  # Redirect to a profile page or another appropriate page

        else:
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')  # General error for invalid form
            return render(request, 'profile.html', {
                'form': form,
                'bought_products': Product.visible_products.filter(bought__in=[user]),
            })

    else:
        form = UserUpdateProfileForm(instance=user)  # Prepopulate form with user's current data

    return render(request, 'profile.html', {
        'form': form,
        'bought_products': Product.visible_products.filter(bought__in=[user]),
    })