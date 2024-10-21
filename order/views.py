from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import OrderItem, Order
from uuid import uuid4
from cart.models import Cart
from shop.sms import ORDER_SUBMITED, OWNER_ORDER_NOTIFICATION, send_sms


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            if not cart:
                messages.error(request, 'سبد خرید شما خالی است.')
                return redirect('cart:cart_list')
            order = form.save(commit=False)
            order.user = request.user
            order.order_id = str(uuid4())[:10]
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item.get('product'),
                    price=item.get('price'),
                    quantity=item.get('quantity')
                )
            cart.clear()
            send_sms(ORDER_SUBMITED, request.user.phone, code=order.order_id)
            send_sms(OWNER_ORDER_NOTIFICATION, '09132017122', name=f'{order.first_name} {order.last_name}', code=order.order_id)
            messages.success(request, 'سفارش شما ثبت شد.')
            return redirect('account:profile')
        else:
            return render(request, 'product-checkout.html', {'form': form})

    else:
        if not request.user.is_authenticated:
            messages.error(request, 'لطفا برای ادامه شماره موبایل خود را تایید کنید.')
            request.session['next_page'] = 'order:checkout'
            return redirect('account:login')
        if request.user.orders.exclude(status=Order.OrderStatus.DONE).exists():
            messages.error(request, 'شما نمی توانید بیشتر از یک سفارش فعال داشته باشید لطفا بخش سفارشات خود را برسی کرده و در صورت بروز مشکل با ما تماس بگیرید..')
            return redirect('account:profile')
        if request.session.get('cart', None).get('products', None):
            cart = Cart(request)
            for item in cart:
                print(item)
                if item['product'].inventory == 0:
                    messages.error(request, 'یکی از محصولات انتخابی شما در انبار موجود نیست لطفا تا موجود شدن صبر نموده و یا جهت پیگیری بیشتر با پشتیبانی تماس بگیرید.')
                    return redirect('cart:cart_list')
                if int(item['quantity']) > item['product'].inventory:
                    messages.error(request, f'یکی از محصولات سبد خرید شما بیش از تعداد موجود در انبار است. ابتدا تعداد محصولات سفارشی خود را اصلاح کرده و آن را ذخیره کنید سپس مجددا برای ثبت سفارش اقدام فرمایید.')
                    return redirect('cart:cart_list')
            form = OrderForm()
            return render(request, 'product-checkout.html', {'form': form})
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart:cart_list')
