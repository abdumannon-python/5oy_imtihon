from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from User.models import Users
from reply.models import Message, Comment, Reply


class MessageView(LoginRequiredMixin,View):
    def get(self,request):
        pre_receiver = request.GET.get('receiver_id',)
        message=Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).order_by('created_at')

        return render(request,'message.html',{'message':message,'pre_receiver': pre_receiver})

    def post(self,request):
        receiver_id=request.POST.get('receiver_id')
        product_id=request.POST.get('product_id')
        desc=request.POST.get('desc')

        if receiver_id and desc:
            Message.objects.create(
                sender=request.user,
                receiver_id=receiver_id,
                product_id=product_id,
                desc=desc
            )
            return redirect('message_list')
        return redirect("message_list")


class ReplyMessageView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        original_message = get_object_or_404(Message, id=message_id)

        receiver_id = original_message.sender.id

        return redirect(f"{reverse('message_list')}?receiver_id={receiver_id}")
class ReadView(LoginRequiredMixin,View):
    def get(self,request,pk):
        message=get_object_or_404(Message,pk=pk,receiver=request.user)
        message.is_read=True
        message.save()
        return redirect('message_list')


class ReplyComment(LoginRequiredMixin,View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return render(request, 'reply_page.html', {'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        reply_text = request.POST.get('reply_text')

        if comment.user == request.user:
            messages.error(request, "O'z sharhingizga javob yozishingiz mumkin emas!")
            return redirect('details', pk=comment.product.pk)

        if reply_text:
            Reply.objects.create(
                comment=comment,
                users=request.user,
                text=reply_text
            )
            messages.success(request, "Javobingiz muvaffaqiyatli qo'shildi!")
            return redirect('details', pk=comment.product.pk)

        else:
            messages.warning(request, "Javob matnini kiriting!")
            return redirect('reply_comment_page', comment_id=comment_id)
class CommentUpdate(LoginRequiredMixin,View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        return render(request, 'comment_update.html', {'comment': comment})
    def post(self,request, comment_id):
        comment=get_object_or_404(Comment,id=comment_id,user=request.user)
        desc=request.POST.get('desc')
        if desc:
            comment.desc=desc
            comment.save()
            messages.success(request, "Sharh yangilandi")
            print(desc)
        return redirect('details',pk=comment.product.pk)

class CommentDelete(LoginRequiredMixin,View):
    def post(self,request,comment_id):
        comment = get_object_or_404(Comment,id=comment_id,user=request.user)
        comment.delete()
        messages.success(request, "Sharh o‘chirildi")
        return redirect('details', pk=comment.product.pk)

class MessageDeleteView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        message = get_object_or_404(Message,id=message_id,sender=request.user)
        message.delete()
        messages.success(request, "Xabar o‘chirildi")
        return redirect('message_list')
class MessageEditView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        message = get_object_or_404(Message,id=message_id,sender=request.user)
        text = request.POST.get('desc')
        if text:
            message.desc = text
            message.save()
        return redirect('message_list')










