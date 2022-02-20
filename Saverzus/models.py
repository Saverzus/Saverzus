from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Notification(models.Model):

	# Кому отправляется уведомление
	target 						= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	# Пользователь, который инициировал создание уведомления
	from_user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="from_user")

	redirect_url				= models.URLField(max_length=500, null=True, unique=False, blank=True, help_text="The URL to be visited when a notification is clicked.")

	# оператор, описывающее уведомление
	verb 						= models.CharField(max_length=255, unique=False, blank=True, null=True)

	# Когда уведомление было создано/обновлено
	timestamp 					= models.DateTimeField(auto_now_add=True)

	# Некоторые уведомления могут быть помечены как «прочитанные». (Я использовал «читать» вместо «активно». Я думаю, что это более уместно)
	read 						= models.BooleanField(default=False)

	# Общий тип, который может относиться к запросу на добавление в друзья, непрочитанному сообщению или любому другому типу «уведомления».
	# Статья: https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
	content_type 				= models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id 					= models.PositiveIntegerField()
	content_object 				= GenericForeignKey()

	def __str__(self):
		return self.verb

	def get_content_object_type(self):
		return str(self.content_object.get_cname)