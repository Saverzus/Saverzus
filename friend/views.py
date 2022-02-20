from django.shortcuts import render, redirect
from django.http import HttpResponse, response
import json

from account.models import Account
from friend.models import FriendRequest, FriendList

def friends_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("Пользователь не найдет")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Не удалось найти {this_user.username}")
			
			# Must be friends to view a friends list
			if user != this_user:
				if not user in friend_list.friends.all():
					return HttpResponse("Вы должны быть в друзьях, что бы проматривать друзей")
			friends = [] # [(friend1, True), (friend2, False), ...]
			# get the authenticated users friend list
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	else:		
		return HttpResponse("Вы должны быть в друзьях, что бы проматривать друзей")
	return render(request, "friend/friend_list.html", context)
	

def friend_requests(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		account = Account.objects.get(pk=user_id)
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("Вы не можете просматривать запросы в друзья другого пользователя")
	else:
		redirect("login")
	return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("Вы уже отправили запрос в друзья этому пользователю")
					# If none are active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Запрос на дружбу отправлен"
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Запрос на дружбу отправлен"

			if payload['response'] == None:
				payload['response'] = "Что-то пошло не так"
		else:
			payload['response'] = "Не удалось отправить запрос в друзья."
	else:
		payload['response'] = "Вы должны быть авторизованны, что бы отправлять запрос в друзья"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now accept it
					updated_notification = friend_request.accept()
					payload['response'] = "Запрос на дружбу принят"

				else:
					payload['response'] = "Что-то пошло не так"
			else:
				payload['response'] = "Это не ваш запрос на дружбу"
		else:
			payload['response'] = "Неудалось принять запрос на дружбу"
	else:
		# По идее никогда не должно случиться
		payload['response'] = "Вы должны быть авторизованны, что бы принять запрос на дружбу"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Вы успешно удалили друга из списка друзей"
			except Exception as e:
				payload['response'] = f"Что-то пошло не так: {str(e)}"
		else:
			payload['response'] = "Ошибка. Не удалось удалить этого друга"
	else:
		# По идее никогда не должно случиться
		payload['response'] = "Вы должны быть авторизованны, что бы удалить из друзей"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now decline it
					updated_notification = friend_request.decline()
					payload['response'] = "Запрос на дружбу отменён"
				else:
					payload['response'] = "Что-то пошло не так"
			else:
				payload['response'] = "Это не ваш запрос на дружбу"
		else:
			payload['response'] = "Невозможно отклонить этот запрос на дружбу"
	else:
		# should never happen
		payload['response'] = "Вы должны быть авторизованными, что бы отклонить запрос на дружбу"
	return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "Нечего отменять, т.к. запроса не дружбу не было"

			# There should only ever be ONE active friend request at any given time. Cancel them all just in case.
			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cance()
				payload['response'] = "Запрос на дружбу отменён"
			else:
				# found the request. Now cancel it
				friend_requests.first().cancel()
				payload['response'] = "Запрос на дружбу отменён"
		else:
			payload['response'] = "Невозможно отменить этот запрос о дружбе"
	else:
		# should never happen
		payload['response'] = "Вы должны быть авторизованы, что бы отменить этот запрос на дружбу"
	return HttpResponse(json.dumps(payload), content_type="application/json")