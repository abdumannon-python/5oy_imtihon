from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Products, Category,ProductImages
from reply.models import Message,Comment

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_seller:
            return redirect('home')

        products = Products.objects.filter(user=request.user)

        unread_messages = Message.objects.filter(receiver=request.user, is_read=False)

        comments = Comment.objects.filter(user=request.user).order_by('-created_at')

        context = {
            'products': products,
            'unread_messages': unread_messages,
            'comments': comments,
        }
        return render(request, 'dashboard.html', context)


class ReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, product__seller=request.user)
        reply_text = request.POST.get('reply_text')

        if reply_text:
            Message.objects.create(
                sender=request.user,
                receiver=comment.user,
                product=comment.product,
                desc=f"Sizning '{comment.desc[:30]}...' kommentingizga javob: {reply_text}"
            )
        return redirect('dashboard')

class ProductDeleteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        product=get_object_or_404(Products,pk=pk, seller=request.user)
        product.delete()
        return redirect('dashboard')

class ProductCreateView(LoginRequiredMixin,View):
    def get(self,request):
        category=Category.objects.all()
        return render(request,'products/product_form.html',{'category':category})

    def post(self,request):
        category_id=request.POST.get('category')

        product=Products.objects.create(
            user=request.user,
            category_id=category_id,
            title=request.POST.get('title'),
            brand=request.POST.get('brand'),
            price=request.POST.get('price'),
            present=request.POST.get("present"),
            main_image=request.FILES.get('main_image'),
            stock=request.POST.get('stock'),
            desc=request.POST.get('desc'),
        )
        product.save()
        extra_images=request.FILES.getlist('images')

        for img in extra_images:
            ProductImages.objects.create(product=product,image=img)

        return redirect('dashboard')

class ProductUpdateView(LoginRequiredMixin,View):
    def get(self,request,pk):
        product=get_object_or_404(Products,pk=pk,user=request.user)
        category=Category.objects.all()
        return render(request,'products/product_form.html',{
            'product':product,
            'category':category,
        })

    def post(self,request,pk):
        product=get_object_or_404(Products,pk=pk,user=request.user)

        product.category_id=request.POST.get('category')
        product.title = request.POST.get('title')
        product.brand = request.POST.get('brand')
        product.price = request.POST.get('price')
        product.present = request.POST.get("present")
        product.stock = request.POST.get('stock')
        product.desc = request.POST.get('desc')

        if request.FILES.get('main_image'):
            product.main_image=request.FILES.get('main_image')
        product.save()

        new_extra_images=request.FILES.getlist('images')
        if new_extra_images:
            for img in new_extra_images:
                ProductImages.objects.create(product=product,image=img)

        return redirect('dashboard')
class ProductDetailView(View):
    def get(self,request,pk):
        product=get_object_or_404(Products,pk=pk)
        similer_product=Products.objects.filter(category=product.category).exclude(pk=pk)[:4]

        comments=Comment.objects.filter(product=product).order_by('-created_at')

        context={
            'product':product,
            'similer_product':similer_product,
            'comment':comments
        }

        return render(request,'products/product_details.html',context)
    def post(self,request,pk):

        product=get_object_or_404(Products,pk=pk)

        if not request.user.is_authenticated:
            return redirect('login')

        comment_text=request.POST.get('text')

        if comment_text:
            Comment.objects.create(
                product=product,
                users=request.user,
                desc=comment_text,
            )

        return redirect('details',pk=pk)
