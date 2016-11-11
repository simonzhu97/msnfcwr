#coding=utf-8 
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from liu_yan_ban.models import Comment, UserID, Transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404

fei_id = 'ff_id'
price = {0:0,1:3,3:8,7:16,9:10}
# Create your views here.
def index(request):
	if request.user.is_authenticated():
		comments = Comment.objects.filter(is_handled = False).order_by('-pub_date')
		return render_to_response('liu_yan_ban/index.html',{'comments':comments})
		# if request.user.username == 'zeizyy':
		# 	comments = Comment.objects.filter(is_handled = False).order_by('-pub_date')
		# 	return render_to_response('liu_yan_ban/index.html',{'comments':comments})
		# else:
		# 	return HttpResponseRedirect(reverse('Delivery'))
	else:
		return HttpResponse(request.META['HTTP_USER_AGENT'])
		if 'MicroMessenger' in request.META['HTTP_USER_AGENT']:
			return render_to_response('liu_yan_ban/weixin.html')
		else:
			return HttpResponseRedirect(reverse('Submit'))
		# return render_to_response('liu_yan_ban/weixin.html')

def home(request):
	if request.user.is_authenticated():
		comments = Comment.objects.filter(is_sensored = True).order_by('-pub_date')
		count_all = len(comments)
		comments_top = comments.filter(is_top = True)
		comments = comments.filter(is_top=False)
		count_top = len(comments_top)
		count = max(0,min(count_all,24)-count_top)
		# return HttpResponse(count)
		count = (count+1)//2
		comments_left = comments[:count]
		count2 = count*2
		comments_right = comments[count:count2]
		return render_to_response('liu_yan_ban/home.html',{'comments_left':comments_left, 'comments_right':comments_right, 'comments_top':comments_top})
	else:
		return HttpResponseRedirect(reverse('Submit'))

def show(request, comment_id):
	if request.user.is_authenticated():
		comment = Comment.objects.get(pk=comment_id)
		comment.is_handled = True
		comment.is_sensored = True
		comment.save()
		return HttpResponseRedirect(reverse('Index'))
	else:
		return HttpResponseRedirect(reverse('Submit'))

def dismiss(request, comment_id):
	if request.user.is_authenticated():
		comment = Comment.objects.get(pk=comment_id)
		comment.is_handled = True
		comment.is_sensored = False
		comment.save()
		return HttpResponseRedirect(reverse('Index'))
	else:
		return HttpResponseRedirect(reverse('Submit'))

def submit(request):
	if fei_id not in request.session:
		user = UserID()
		user.save()
		user_id = user.id
		request.session[fei_id] = user_id
	else:
		user_id = request.session[fei_id]
	error=''
	success =''
	comments_handled = Comment.objects.filter(user_id=user_id).filter(is_handled=True).filter(is_viewed=False)
	comments_approved = comments_handled.filter(is_sensored=True)
	comments_dismissed = comments_handled.filter(is_sensored=False)
	transaction_confirmed = Transaction.objects.filter(user_id=user_id).filter(is_confirmed=True).filter(is_delivered=False)

	if request.method == "POST":
		name = request.POST["name"]
		content = request.POST["content"]
		if not content:
			error = '发言不能为空!'
		else:
			if not name:
				comment = Comment(content=content)
			else:
				comment = Comment(author=name, content=content)
			comment.user_id = user_id
			try:
				comment.save()
			except:
				return HttpResponseRedirect(reverse('Submit'))
			if request.user.is_authenticated():
				comment.author = '管理员'
				comment.save()
				return HttpResponseRedirect(reverse('Show',args=[comment.id]))
			return HttpResponseRedirect(reverse('Success'))
			# success = '发言成功，请等待管理员审核.现在可继续发表评论.'
	return render_to_response('liu_yan_ban/submit.html',{
		'approved':comments_approved, \
		'dismissed':comments_dismissed, 'error':error, \
		'success':success,'user_id':user_id,
		'trans':transaction_confirmed})

def success(request):
	return render_to_response('liu_yan_ban/success.html')

def top(request, comment_id, option):
	if request.user.is_authenticated():
		comment = Comment.objects.get(pk=comment_id)
		comment.is_top = not comment.is_top
		comment.is_handled = True
		comment.is_sensored = True
		comment.save()
		if int(option) == 1:
			return HttpResponseRedirect(reverse('Home'))
		else:
			return HttpResponseRedirect(reverse('Index'))
	else:
		return HttpResponseRedirect(reverse('Submit'))

def view(request):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	comments_handled = Comment.objects.filter(user_id=user_id).filter(is_handled=True).filter(is_viewed=False)
	for comment in comments_handled:
		comment.is_viewed = True
		comment.save()
	return HttpResponseRedirect(reverse('Submit'))

def flower_self(request):
	if fei_id not in request.session:
		user = UserID()
		user.save()
		user_id = user.id
		request.session[fei_id] = user_id
	else:
		user_id = request.session[fei_id]
	return render_to_response('liu_yan_ban/flower_self.html')

def flower_msn(request):
	if fei_id not in request.session:
		user = UserID()
		user.save()
		user_id = user.id
		request.session[fei_id] = user_id
	else:
		user_id = request.session[fei_id]
	return render_to_response('liu_yan_ban/flower_msn.html')

def flower_self_submit(request):
	if fei_id not in request.session:
		user = UserID()
		user.save()
		user_id = user.id
		request.session[fei_id] = user_id
	else:
		user_id = request.session[fei_id]
	error = '缺少必填字段!'
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('FlowerSelf'))
	if not request.POST['name'] or \
		not request.POST['quantity'] or\
		not request.POST['location']:
		return render_to_response('liu_yan_ban/flower_self.html',{'error':error})
	name = request.POST['name']
	quantity = request.POST['quantity']
	location = request.POST['location']
	transaction = Transaction(name=name, quantity=quantity,\
		location=location,is_self=True, user_id=user_id, money=price[int(quantity)])
	transaction.save()
	return HttpResponseRedirect(reverse('Confirmation',args=[transaction.id]))

def flower_msn_submit(request):
	if fei_id not in request.session:
		user = UserID()
		user.save()
		user_id = user.id
		request.session[fei_id] = user_id
	else:
		user_id = request.session[fei_id]
	error = '缺少必填字段!'
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('FlowerMSN'))
	if not request.POST['name'] or \
		not request.POST['quantity'] or\
		not request.POST['recipient']:
		return render_to_response('liu_yan_ban/flower_msn.html',{'error':error})
	shown_name = '匿名'
	name = request.POST['name']
	# liuyan = request.POST['liuyan']
	quantity = request.POST['quantity']
	recipient = request.POST['recipient']
	if request.POST['shown_name']:
		shown_name = request.POST['shown_name']
	transaction = Transaction(name=name, shown_name=shown_name,\
				quantity = quantity, recipient=recipient,\
		is_self=False, user_id=user_id, money = price[int(quantity)])
	transaction.save()
	return HttpResponseRedirect(reverse('Confirmation',args=[transaction.id]))

def confirmation(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	return render_to_response('liu_yan_ban/confirmation.html',{'trans':trans})

def process(request,trans_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('Submit'))
	trans = Transaction.objects.get(pk=trans_id)
	trans.is_processed=True
	trans.save()
	return HttpResponseRedirect(reverse('Delivery'))

def delivery(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('Submit'))
	transaction = Transaction.objects.filter(is_confirmed=True)
	transaction_delivered = transaction.filter(is_delivered=True)
	transaction_processed = transaction.filter(is_processed=True, is_delivered=False)
	transaction_new = transaction.filter(is_delivered=False, is_processed=False)
	return render_to_response("liu_yan_ban/delivery.html",{\
		'processed':transaction_processed,\
		'delivered':transaction_delivered, \
		'new':transaction_new})

def handle(request, trans_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('Submit'))
	trans = Transaction.objects.get(pk=trans_id)
	trans.is_delivered=True
	trans.save()
	return HttpResponseRedirect(reverse('Delivery'))

def cancel(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.delete()
	return HttpResponseRedirect(reverse('Submit'))

def confirm(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.is_confirmed = True
	trans.save()
	money = calc_total(trans.quantity)
	return render_to_response('liu_yan_ban/payment.html',{'money':money})

def error(request):
	return HttpResponseRedirect(reverse('Submit'))

def calc_total(quantity):
	if quantity not in price:
		return HttpResponseRedirect(reverse('Submit'))
	return price[quantity]
