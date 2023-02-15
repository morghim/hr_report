// Copyright (c) 2022, Ibrahim Morghim and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Percentage of employee time"] = {
	"filters": [
		{
            fieldname: 'employee',
            label: __('Employee'),
            fieldtype: 'Link',
            options: 'Employee',
        },
		{
			fieldname: 'from_date',
            label: __('From Date'),
            fieldtype: 'Date',
			reqd: 1

		},
		{
			fieldname: 'to_date',
            label: __('To Date'),
            fieldtype: 'Date',
			reqd: 1

		},
		{
            fieldname: 'is_calc_spesfic_hour',
            label: __('Calc Real Hours'),
            fieldtype: 'Check',
        },



	]
};
