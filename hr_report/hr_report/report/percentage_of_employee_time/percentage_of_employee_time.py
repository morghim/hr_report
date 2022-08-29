# Copyright (c) 2022, Ibrahim Morghim and contributors
# For license information, please see license.txt

from dataclasses import fields
from pkgutil import get_data
from tracemalloc import start
import frappe
from frappe import utils
from frappe.utils import cstr, cint, getdate, add_to_date
from frappe import msgprint, _
from calendar import monthrange
from datetime import datetime, timedelta
import calendar
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday


def execute(filters=None):

    columns = [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "fieldname": "employee_name",
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fetch_from": "employee.employee_name",
        },
        {
            "fieldname": "full_time",
            "label": _("Full Time"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "employee_time",
            "label": _("Employee Time"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "precentage_time",
            "label": _("Precentage Employee Time"),
            "fieldtype": "Percent",
        },
    ]
    data = []
    filters_t = {'status': 'Active'}
    if filters.employee:
        filters_t = {'name': filters.employee}

    employees = frappe.db.get_list(
        "Employee", fields=['name', 'default_shift', 'employee_name', 'holiday_list'], filters=filters_t)
    for i in employees:
        if i.default_shift and i.holiday_list:
            sh = get_shift_time(i.default_shift)
            employee_data = get_employee_checkin_by_shift(
                i.name, sh, filters.month, i)
            data.append(employee_data)
        else:
            data.append(
                {
                    "employee": i.name,
                    "employee_name": i.employee_name,
                    "full_time": 0,
                    "employee_time": 0,
                    "precentage_time": 0}

            )

    return columns, data


def get_shift_time(shif_type):
    return frappe.db.sql("""
	select working_hour_per_month, start_time, end_time, working_hours_per_day from `tabShift Type` where name = '%s'
	""" % (shif_type))


def get_employee_checkin_by_shift(employee_name, shift_details, month, employee):
    emloyee_data = {}

    d = datetime.now()
    i = monthrange(d.year, month_map[month])
    start_date = d.replace(month=month_map[month]).replace(day=1)
    end_date = start_date.replace(day=i[1])
    employee_check_in = frappe.db.get_all('Employee Checkin', filters={'employee': employee_name, 'time': [
                                          '>=', start_date], 'time': ['<=', end_date]}, fields=['name', 'time'], order_by='time')
    for i in employee_check_in:
        if i.time.date() in emloyee_data:
            if 'in' in emloyee_data[i.time.date()]:
                if i.time < emloyee_data[i.time.date()]['in']:
                    emloyee_data[i.time.date()]['in'] = i.time
            else:
                emloyee_data[i.time.date()]['in'] = i.time

            if 'out' in emloyee_data[i.time.date()]:
                if i.time > emloyee_data[i.time.date()]['out']:
                    emloyee_data[i.time.date()]['out'] = i.time
            else:
                emloyee_data[i.time.date()]['out'] = i.time
        else:
            emloyee_data[i.time.date()] = {
                'in': i.time,
                'out': i.time
            }
    d = process_data_used_shift(emloyee_data, shift_details)
    if d:
        c = calculate_employee_time(d, True, employee, shift_details)
        data = {
            "employee": employee.name,
            "employee_name": employee.employee_name,
            "full_time": shift_details[0][0],
            "employee_time": c,
            "precentage_time": (c/shift_details[0][0]) * 100}
        return data
    else:
        data = {
            "employee": employee.name,
            "employee_name": employee.employee_name,
            "full_time": 0,
            "employee_time": 0,
            "precentage_time": 0}
        return data


def process_data_used_shift(data, shift_details):

    new_data = data
    start_hour, start_minute = get_hours_from_shift(shift_details, 1)
    end_hour, end_minute = get_hours_from_shift(shift_details, 2)
    if not start_hour:
        return
    if not start_minute:
        return
    for k in new_data:
        start_time = new_data[k]['in'].replace(
            hour=start_hour, minute=start_minute)
        end_time = new_data[k]['out'].replace(hour=end_hour, minute=end_minute)
        if new_data[k]['in'] < start_time:

            new_data[k]['in'] = start_time
        if new_data[k]['out'] > end_time:
            new_data[k]['out'] = end_time
    return new_data


def get_hours_from_shift(shift_details, key):
    try:
        return shift_details[0][key].seconds//3600, (shift_details[0][key].seconds//60) % 60
    except:
        return None, None


def calculate_employee_time(data, with_holidays=True, employee=None, shift_data=None):
    total_hours = 0
    for k, v in data:
        hour_per_day = data[k]['out'] - data[k]['in']
        minute = (hour_per_day.total_seconds()//60) % 60
        if hour_per_day.total_seconds() // 3600 > 0:
            if not is_holiday(employee.holiday_list, v):
                tot_h = hour_per_day.total_seconds() // 3600
                if tot_h < shift_data[0][3]:
                    total_hours = total_hours + hour_per_day.total_seconds() // 3600
                    if minute:
                        total_hours = total_hours + minute / 60
                else:
                    total_hours = total_hours + shift_data[0][3]
    return total_hours


month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}
