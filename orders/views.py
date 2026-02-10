from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View

from .models import Cart, Order, CartItem, OrderItem,Wishlis
from product.models import Products


class AddCartView(LoginRequiredMixin,View):
    def post(self,request,id):
        product=get_object_or_404(Products,id=id)
        cart,created=Cart.objects.get_or_create(user=request.user,is_ordered=False)

        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,product=product)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()

        return redirect('cart_view')

class CartView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        return render(request,'cart.html',{'cart':cart})


class RemoveFromCartView(LoginRequiredMixin,View):
    def post(self,request,id):
        product=get_object_or_404(Products,id=id)
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        cart_item=CartItem.objects.filter(cart=cart,product=product).first()
        if not cart_item:
            return redirect('cart_view')
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart_view')
class DeleteCart(LoginRequiredMixin,View):
    def post(self,request,product_id):
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        CartItem.objects.filter(cart=cart,product_id=product_id).delete()
        return redirect('cart_view')


class CheckOut(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        if not cart or not cart.items.exists():
            return redirect('home')


        return render(request,'chekout.html',{'cart':cart})

    def post(self,request):
        cart=get_object_or_404(Cart,user=request.user,is_ordered=False)

        for item in cart.items.all():
            if item.product.stock < item.quantity:


                messages.error(request,
                               f"Kechirasiz, {item.product.title} mahsulotidan omborda yetarli emas. Qoldiq: {item.product.stock} ta")
                return redirect('cart_view')

        username=request.POST.get('username')
        phone=request.POST.get('phone')
        address=request.POST.get('address')



        order = Order.objects.create(
            user=request.user,
            username=username,
            phone=phone,
            address=address,
            total_price=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.is_ordered = True
        cart.save()
        return render(request, 'order_success.html', {'order': order})

class OrderStatusView(LoginRequiredMixin,View):
    def get(self,request):
        order=OrderItem.objects.filter(product__user=request.user).select_related('order','product')
        context={
            'order':order
        }
        return render(request,'orders.html',context)
    def post(self,request):
        order_item_id=request.POST.get('order_item_id')
        new_status=request.POST.get('status')
        orderitem=get_object_or_404(OrderItem,id=order_item_id,product__user=request.user)

        order=orderitem.order


        if new_status in dict(Order.STATUS_CHOICES).keys():
            old_status = order.status
            if new_status=='cancelled':
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
            order.status=new_status
            order.save()
            messages.success(
                request,
                f"Buyurtma #{order.id} holati '{old_status}' dan '{new_status}' ga o'zgartirildi!"
            )
        else:
            messages.error(request, "Noto'g'ri holat tanlandi!")

        return redirect("orderstatus")
class OrderCancelledView(LoginRequiredMixin,View):
    def get(self,request):
        order_item=OrderItem.objects.filter(order__user=request.user).select_related('order', 'product')
        return render(request,'orderuser.html',{"order_item":order_item})
    def post(self,request):
        order_id = request.POST.get('order_item_id')
        order=get_object_or_404(Order,user=request.user,id=order_id)


        if order.user==request.user:
            if order.status=='pending':
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
                order.status='cancelled'
                order.save()
            else:
                messages.error(request,"BU buyurtmani bekor qilib bo'lmaydi")

            return redirect('orderuser')


class WishlisView(LoginRequiredMixin,View):
    def get(self,request,pk=None):

        if pk is not None:
            product = get_object_or_404(Products, pk=pk)
            wishlis=Wishlis.objects.filter(user=request.user,product=product)
            if wishlis:
                wishlis.delete()
            else:
                Wishlis.objects.create(user=request.user, product=product)
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        my_wishlist = Wishlis.objects.filter(user=request.user)
        return render(request, 'wishlis.html', {'wishlis': my_wishlist})
    def post(self,request,pk):
        product=get_object_or_404(Products,pk=pk)
        user=request.user

        wishles=Wishlis.objects.filter(user=user,product=product)
        if wishles:
            wishles.delete()
        else:
            Wishlis.objects.create(user=user,product=product)
        return redirect('home')










