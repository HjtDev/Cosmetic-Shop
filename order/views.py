from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import OrderItem, Order
from uuid import uuid4
from cart.models import Cart


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
            print('SMS Notification')
            print(f'مشتری گرامی سفارش شما با کد {order.order_id} ثبت شد. با سپاس از خرید شما')
            return redirect('shop:home')
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
            form = OrderForm()
            return render(request, 'product-checkout.html', {'form': form})
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart:cart_list')
