from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from reply.models import Message, Comment, Reply


class MessageView(LoginRequiredMixin,View):
    def get(self,request):
        message=Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).order_by('created_at')

        return render(request,'message.html',{'message':message})

    def post(self,request):
        receiver_id=request.POST.get('receiver_id')
        product_id=request.POST.get('product_id')
        desc=request.POST.get('desc')

        if receiver_id and desc:
            Message.objects.create(
                sender=request.user,
                receiver_id=receiver_id,
                product_id=product_id,
            )
            return redirect('message_list')
        return redirect("message_list")

class ReadView(LoginRequiredMixin,View):
    def get(self,request,pk):
        message=get_object_or_404(Message,pk=pk,receiver=request.user)
        message.is_read=True
        message.save()
        return redirect('message_list')

class ReplyComment(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return render(request, 'reply_page.html', {'comment': comment})
    def post(self,request,comment_id):
        comment=get_object_or_404(Comment,id=comment_id)
        reply_text=request.POST.get('reply_text')

        if reply_text:
            Reply.objects.create(
                comment=comment,
                users=request.user,
                desc=reply_text
            )

        return redirect('dashboard')




