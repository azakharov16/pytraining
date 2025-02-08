import datetime as dt
import calendar
from itertools import compress

# user_format = input("Enter date format in one of the forms: '%m/%d/%Y' or '%d.%m.%Y' >:")
# user_date1 = input("Enter start date in Russian or English format >: ")
# user_date2 = input("Enter end date in Russian or English format >: ")
# user_convention = input("Choose daycount convention from 'act/365', 'act/360', 'act/act' or '30/360' >: ")


def yearfrac(start_date, end_date, date_format = None, daycount = 'act/365'):
	if daycount not in ('act/365','act/360','30/360','act/act'):
		raise ValueError("This daycount convention is not supported")
	if date_format not in ('%m/%d/%Y','%d.%m.%Y',None):
		raise ValueError("This date format is not supported")
	if type(start_date) == str:
		start_date = dt.datetime.strptime(start_date, date_format)
	if type(end_date) == str:
		end_date = dt.datetime.strptime(end_date, date_format)

	def frac_act_365(start_date, end_date):
		delta = end_date - start_date
		return delta.days / 365

	def frac_act_360(start_date, end_date):
		delta = end_date - start_date
		return delta.days / 360

	def frac_30_360(start_date, end_date):
		delta = ((end_date.year - start_date.year) * 360 +
				 (end_date.month - start_date.month) * 30 +
				 (min(30, end_date.day) - min(30, start_date.day))) / 360
		return delta

	def frac_act_act(start_date, end_date):
		delta = end_date - start_date
		start_year = start_date.year
		end_year = end_date.year
		year_range = list(range(start_year, end_year + 1))
		leap_ind = list(map(calendar.isleap, year_range))
		right_days = 0
		left_days = 0
		mid_days = 0
		if len(year_range) == 1:
			if leap_ind:
				tenor = delta.days / 366
			else:
				tenor = delta.days / 365
		else: 
			if leap_ind[0]:
				delta_left = dt.datetime.strptime('%d/%d/%d' % (12,31,year_range[0]), '%m/%d/%Y') - start_date
				left_days = delta_left.days
			if leap_ind[-1]:
				delta_right = end_date - dt.datetime.strptime('%d/%d/%d' % (1,1,year_range[-1]), '%m/%d/%Y')
				right_days = delta_right.days
			leap_mid = list(compress(year_range, leap_ind[1:-1]))
			if leap_mid:
				for y in leap_mid:
					delta_mid = dt.datetime.strptime('%d/%d/%d' % (12,31,y), '%m/%d/%Y') - dt.datetime.strptime('%d/%d/%d' % (1,1,y), '%m/%d/%Y')
					days_in_y = delta_mid.days
					mid_days += days_in_y
			days_in_leap = left_days + mid_days + right_days
			days_not_in_leap = delta.days - days_in_leap
			tenor = days_in_leap / 366 + days_not_in_leap / 365
		return tenor

	func = {
		'act/365': frac_act_365,
		'act/360': frac_act_360,
		'30/360': frac_30_360,
		'act/act': frac_act_act}[daycount]
	return func(start_date, end_date)


if __name__ == '__main__':
	print(yearfrac("4/10/2008","6/12/2017", date_format = '%m/%d/%Y'))
	print(yearfrac("4/10/2008","6/12/2017", date_format = '%m/%d/%Y', daycount = 'act/act'))
	print(yearfrac("4/10/2008","6/12/2017", date_format = '%m/%d/%Y', daycount = 'act/365'))
	print(yearfrac("4/10/2008","6/12/2017", date_format = '%m/%d/%Y', daycount = 'act/360'))
	print(yearfrac("4/10/2008","6/12/2017", date_format = '%m/%d/%Y', daycount = '30/360'))

# print(yearfrac(user_date1, user_date2, date_format = user_format, daycount = user_convention))
