from pyexpat.errors import messages

from django.contrib.auth.mixins import LoginRequiredMixin
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

        return redirect('card_detail')

class CartDetailView(View):
    def get(self,request):
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        return render(request,'cart.html',{'cart':cart})


class RemoveFromCartView(View):
    def post(self,request,id):
        product=get_object_or_404(Products,id=id)
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        cart_item=CartItem.objects.get(cart=cart,product=product)

        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart_detail')
class DeleteCart(View):
    def post(self,request,product_id):
        cart=Cart.objects.get(user=request.user,is_orderes=False)
        CartItem.objects.get(cart=cart,product_id=product_id).delete()
        return redirect('cart_detail')


class CheckOut(View):
    def get(self,request):
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        if not cart or not cart.items.exists():
            return redirect('index')

        return render(request,'chekout.html',{'cart':cart})

    def post(self,request):
        cart=get_object_or_404(Cart,user=request.user,is_ordered=False)

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
                price=item.product.discount_price,
                quantity=item.quantity,
            )
        cart.is_ordered=True
        cart.save()
        return render(request, 'order_success.html', {'order': order})

class OrderItemView(View):
    def get(self,request):
        order_item =OrderItem.objects.filter(product__user=request.user)
        context={
            'order_item':order_item
        }
        return render(request,'orderitem.html',context)
class OrderView(View):
    def get(self,request):
        order=OrderItem.objects.filter(product__user=request.user).select_related('order','product')
        context={
            'order':order
        }
        return render(request,'Order.html',context)
    def post(self,request):
        order_item_id=request.POST.get('order_item_id')
        new_status=request.POST.get('status')
        orderitem=get_object_or_404(OrderItem,id=order_item_id,product__user=request.user)

        order=orderitem.order


        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status=new_status
            order.save()

        return redirect("order_view")

class OrderUserView(View):
    def get(self,request):
        order_item=OrderItem.objects.filter(order_id=request.user)
        return render(request,'orderuser.html',{"order_item":order_item})
    def post(self,request):
        order_item_id=request.POST.get('order_item_id')
        orderitem=get_object_or_404(OrderItem,id=order_item_id)
        order=orderitem.order


        if order.user==request.user:
            if order.status=='pending':
                order.status='cancelled'
                order.save()
            else:
                messages.erorr(request,"BU buyurtmani bekor qilib bo'lmaydi")

        return redirect('orderuser')


class WishlisView(View):
    def get(self,request):
        wishlis=Wishlis.objects.filter(user=request.user)
        return render(request,'wishlis.html',{'wishlis':wishlis})
    def post(self,request,pk):
        product=get_object_or_404(Products,id =pk)
        user=request.user

        wishles=Wishlis.objects.filter(user=user,product=product)
        if wishles:
            wishles.delete()
        else:
            Wishlis.objects.create(user=user,product=product)
        return redirect('home')










