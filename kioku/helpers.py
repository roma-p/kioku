import datetime


def format_now() :

	now = datetime.datetime.now()
	now_str = str(now.year)+'.'+str(now.month)+'.'+str(now.day)+'.'+str(now.hour)+':'+str(now.minute)
	return now_str