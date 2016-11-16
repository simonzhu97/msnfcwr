#coding=utf-8 
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from liu_yan_ban.models import Comment, UserID, Transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404
import random

fei_id = 'msnfcwr_id'
page_max = 30
price = {0:0,1:3,3:8,7:16,9:20}
# Create your views here.

def check_auth(f):
	def wrap(request, *args, **kwargs):
		if not request.user.is_authenticated():
			# current_url = request.get_full_path()
			# current_url = quote(current_url, safe='')
			return HttpResponseRedirect(reverse('Submit'))
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

def check_browser(f):
	def wrap(request, *args, **kwargs):
		if 'MicroMessenger' in request.META['HTTP_USER_AGENT']:
			return render_to_response('liu_yan_ban/weixin.html')
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

def check_session(f):
	def wrap(request, *args, **kwargs):
		if fei_id not in request.session:
			user = UserID()
			user.save()
			user_id = user.id
			request.session[fei_id] = user_id
		else:
			user_id = request.session[fei_id]
		kwargs['user_id'] = user_id
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

@check_auth
@check_browser
def index(request):
	comments = Comment.objects.filter(is_handled = False).order_by('pub_date')
	return render_to_response('liu_yan_ban/index.html',{'comments':comments})

@check_auth
def home(request):
	comments = Comment.objects.filter(is_sensored = True).order_by('-pub_date')
	count_all = comments.count()
	comments_top = comments.filter(is_top = True)
	comments = comments.filter(is_top=False)
	count_top = len(comments_top)
	count = max(0, min(count_all, page_max) - count_top)
	comments_no_top = list(enumerate(comments[:count]))
	random.shuffle(comments_no_top, random.seed(37))
	return render_to_response('liu_yan_ban/home.html',{'comments_no_top':comments_no_top, 'comments_top':comments_top})

@check_auth
def show(request, comment_id):
	comment = Comment.objects.get(pk=comment_id)
	# messages.success(request, "comment.short")
	comment.is_handled = True
	comment.is_sensored = True
	comment.save()
	return HttpResponseRedirect(reverse('Index'))

@check_auth
def dismiss(request, comment_id):
	comment = Comment.objects.get(pk=comment_id)
	# messages.error(request, comment.short)
	comment.is_handled = True
	comment.is_sensored = False
	comment.save()
	return HttpResponseRedirect(reverse('Index'))

@check_session
@check_browser
def submit(request, *args, **kwargs):
	user_id = kwargs.get('user_id')
	error=''
	success =''
	comments_handled = Comment.objects.filter(user_id=user_id).filter(is_handled=True).filter(is_viewed=False)
	comments_approved = list(comments_handled.filter(is_sensored=True))
	comments_rejected = list(comments_handled.filter(is_sensored=False))
	transaction_confirmed = Transaction.objects.filter(user_id=user_id).filter(is_confirmed=True).filter(is_delivered=False)
	for comment in comments_handled:
		comment.is_viewed = True
		comment.save()
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
	return render_to_response('liu_yan_ban/submit.html',{
		'comments_approved': comments_approved, \
		'comments_rejected' :comments_rejected, \
		'error':error, \
		'success':success, \
		'user_id':user_id,
		'trans':transaction_confirmed})

@check_browser
def success(request):
	return render_to_response('liu_yan_ban/success.html')

@check_auth
def top(request, comment_id, option):
	comment = Comment.objects.get(pk=comment_id)
	comment.is_top = not comment.is_top
	comment.is_handled = True
	comment.is_sensored = True
	comment.save()
	if int(option) == 1:
		return HttpResponseRedirect(reverse('Home'))
	else:
		return HttpResponseRedirect(reverse('Index'))

def view(request):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	comments_handled = Comment.objects.filter(user_id=user_id).filter(is_handled=True).filter(is_viewed=False)
	for comment in comments_handled:
		comment.is_viewed = True
		comment.save()
	return HttpResponseRedirect(reverse('Submit'))

@check_session
@check_browser
def flower_self(request, *args, **kwargs):
	return render_to_response('liu_yan_ban/flower_self.html')

@check_session
@check_browser
def flower_msn(request, *args, **kwargs):
	return render_to_response('liu_yan_ban/flower_msn.html')

@check_session
@check_browser
def flower_self_submit(request, *args, **kwargs):
	user_id = kwargs.get('user_id')
	error = '缺少必填部分!'
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

@check_session
@check_browser
def flower_msn_submit(request, *args, **kwargs):
	user_id = kwargs.get('user_id')
	error = '缺少必填部分!'
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

@check_browser
def confirmation(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	return render_to_response('liu_yan_ban/confirmation.html',{'trans':trans})

@check_auth
def process(request,trans_id):
	trans = Transaction.objects.get(pk=trans_id)
	trans.is_processed=True
	trans.save()
	return HttpResponseRedirect(reverse('Delivery'))

@check_auth
def delivery(request):
	transaction = Transaction.objects.filter(is_confirmed=True)
	transaction_delivered = transaction.filter(is_delivered=True)
	transaction_processed = transaction.filter(is_processed=True, is_delivered=False)
	transaction_new = transaction.filter(is_delivered=False, is_processed=False)
	return render_to_response("liu_yan_ban/delivery.html",{\
		'processed':transaction_processed,\
		'delivered':transaction_delivered, \
		'new':transaction_new})

@check_auth
def handle(request, trans_id):
	trans = Transaction.objects.get(pk=trans_id)
	trans.is_delivered=True
	trans.save()
	return HttpResponseRedirect(reverse('Delivery'))

@check_browser
def cancel(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.delete()
	return HttpResponseRedirect(reverse('Submit'))

@check_browser
def confirm(request, trans_id):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user_id = request.session[fei_id]
	trans = Transaction.objects.get(pk=trans_id)
	if user_id != trans.user_id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.is_confirmed = True
	trans.save()
	money = _calc_total(trans.quantity)
	return render_to_response('liu_yan_ban/payment.html',{'trans_id':trans_id, 'money':money})

def error(request):
	return HttpResponseRedirect(reverse('Submit'))

def _calc_total(quantity):
	if quantity not in price:
		return HttpResponseRedirect(reverse('Submit'))
	return price[quantity]
