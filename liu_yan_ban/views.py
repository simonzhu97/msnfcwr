#coding=utf-8 
from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from liu_yan_ban.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
import random

fei_id = 'msnfcwr_id'
fei_like = 'msnfcwr_like'
min_like = 40
page_max = 30
like_max = 15
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
			user = AUser.objects.create()
			user_id = user.id
			request.session[fei_id] = user.id
		else:
			user_id = request.session[fei_id]
			user = AUser.objects.get(pk=user_id)
		kwargs['user'] = user
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

def get_session_or_redirect(f):
	def wrap(request, *args, **kwargs):
		if fei_id not in request.session:
			return HttpResponseRedirect('Submit')
		else:
			user_id = request.session[fei_id]
			user = AUser.objects.get(pk=user_id)
		kwargs['user'] = user
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

def check_like_session(f):
	def wrap(request, *args, **kwargs):
		if fei_like not in request.session:
			request.session[fei_like] = []
		user_likes = request.session[fei_like]
		kwargs[fei_like] = user_likes
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap

@check_auth
@check_browser
def index(request):
	comments = Comment.objects.filter(is_handled = False).order_by('pub_date')
	return render_to_response('liu_yan_ban/index.html',{'comments':comments})

@check_like_session
@get_session_or_redirect
def home(request, *args, **kwargs):
	is_auth = request.user.is_authenticated()
	comments_max = Comment.objects.filter(is_sensored = True).order_by('-pub_date')[:page_max]
	comments_top = [comments for comments in comments_max if comments.is_top or comments.likes >= min_like]
	if is_auth:
		comments_no_top = [comments for comments in comments_max if not comments.is_top and not comments.likes >= 4]
	else:
		comments_no_top = comments_max[:like_max]
	comments_no_top = list(enumerate(comments_no_top))
	if is_auth:
		random.shuffle(comments_no_top, random.seed(37))
	if not is_auth:
		user_likes = kwargs[fei_like]
		comments_no_top = [(index, comment) for index, comment in comments_no_top if comment.id not in user_likes]
	return render_to_response('liu_yan_ban/home.html',{'comments_no_top':comments_no_top, 'comments_top':comments_top, 
							'is_auth':is_auth, 'is_auth_home':is_auth})

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
	user = kwargs.get('user')
	error=''
	success =''
	comments_handled = Comment.objects.filter(user=user).filter(is_handled=True).filter(is_viewed=False)
	comments_approved = list(comments_handled.filter(is_sensored=True))
	comments_rejected = list(comments_handled.filter(is_sensored=False))
	dms = list(DM.objects.filter(user=user).filter(is_viewed=False))
	transaction_confirmed = Transaction.objects.filter(user=user).filter(is_confirmed=True).filter(is_delivered=False)
	
	for comment in comments_handled:
		comment.is_viewed = True
		comment.save()

	for dm in dms:
		dm.is_viewed = True
		dm.save()

	if request.method == "POST":
		name = request.POST["name"]
		content = request.POST["content"]
		if not content:
			error = '发言不能为空!'
		else:
			if not name:
				comment = Comment(content=content)
			else:
				user.name = name
				user.save()
				comment = Comment(user=user, content=content)
			comment.user = user
			try:
				comment.save()
			except:
				return HttpResponseRedirect(reverse('Submit'))
			if request.user.is_authenticated():
				user.name = "管理员"
				user.save()
				comment.user = user
				comment.save()
				return HttpResponseRedirect(reverse('Show',args=[comment.id]))
			return HttpResponseRedirect(reverse('Success'))
	return render_to_response('liu_yan_ban/submit.html',{
		'comments_approved': comments_approved, \
		'comments_rejected' :comments_rejected, \
		'dms': dms, \
		'error':error, \
		'success':success, \
		'user': user, \
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

@check_like_session
def like(request, comment_id, *args, **kwargs):
	user_likes = kwargs[fei_like]
	if comment_id in user_likes:
		return HttpResponseRedirect(reverse('Submit'))
	user_likes.append(int(comment_id))
	request.session[fei_like] = user_likes[-page_max:]
	comment = Comment.objects.get(pk=comment_id)
	comment.like()
	return HttpResponseRedirect(reverse('Home'))

@check_like_session
def dislike(request, comment_id, *args, **kwargs):
	user_likes = kwargs[fei_like]
	if comment_id in user_likes:
		return HttpResponseRedirect(reverse('Submit'))
	user_likes.append(int(comment_id))
	request.session[fei_like] = user_likes[-page_max:]
	comment = Comment.objects.get(pk=comment_id)
	comment.dislike()
	return HttpResponseRedirect(reverse('Home'))

def view(request):
	if fei_id not in request.session:
		return HttpResponseRedirect(reverse('Submit'))
	user = request.session[fei_id]
	comments_handled = Comment.objects.filter(user=user).filter(is_handled=True).filter(is_viewed=False)
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
	user = kwargs.get('user')
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
		location=location,is_self=True, user=user, money=price[int(quantity)])
	transaction.save()
	return HttpResponseRedirect(reverse('Confirmation',args=[transaction.id]))

@check_session
@check_browser
def flower_msn_submit(request, *args, **kwargs):
	user = kwargs.get('user')
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
		is_self=False, user=user, money = price[int(quantity)])
	transaction.save()
	return HttpResponseRedirect(reverse('Confirmation',args=[transaction.id]))

@get_session_or_redirect
@check_browser
def confirmation(request, trans_id, *args, **kwargs):
	user = kwargs.get('user')
	trans = Transaction.objects.get(pk=trans_id)
	if user.id != trans.user.id:
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

@get_session_or_redirect
@check_browser
def cancel(request, trans_id, *args, **kwargs):
	user = kwargs.get('user')
	trans = Transaction.objects.get(pk=trans_id)
	if user.id != trans.user.id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.delete()
	return HttpResponseRedirect(reverse('Submit'))

@get_session_or_redirect
@check_browser
def confirm(request, trans_id, *args, **kwargs):
	user = kwargs.get('user')
	trans = Transaction.objects.get(pk=trans_id)
	if user.id != trans.user.id:
		return HttpResponseRedirect(reverse('Submit'))
	trans.is_confirmed = True
	trans.save()
	money = _calc_total(trans.quantity)
	return render_to_response('liu_yan_ban/payment.html',{'trans_id':trans_id, 'money':money})

@check_auth
def direct_message(request, user_id):
	to_user = AUser.objects.get(pk = user_id)
	if request.method == 'POST':
		content = request.POST.get('content')
		if not content:
			return HttpResponseRedirect(reverse('DM'))
		dm = DM.objects.create(user=to_user, content=content)
		return HttpResponseRedirect(reverse('Success'))
	return render_to_response('liu_yan_ban/direct_message.html', {'user': to_user})

@check_auth
def direct_message_all(request):
	if request.method == 'POST':
		content = request.POST.get('content')
		if not content:
			return HttpResponseRedirect(reverse('DM'))
		users = AUser.objects.all()
		for user in users:
			dm = DM.objects.create(user=user, content=content)
		return HttpResponseRedirect(reverse('Index'))
	return render_to_response('liu_yan_ban/direct_message.html')


def error(request):
	return HttpResponseRedirect(reverse('Submit'))

def _calc_total(quantity):
	if quantity not in price:
		return HttpResponseRedirect(reverse('Submit'))
	return price[quantity]
