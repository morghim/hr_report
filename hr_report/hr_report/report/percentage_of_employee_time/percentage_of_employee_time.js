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
	
			"fieldname":"month",
	
			"label": __("Month"),
	
			"fieldtype": "Select",
	
			"options": "Jan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
	
			"default": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
	
				"Dec"][frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth()
				
		],
	
		},
		{
            fieldname: 'is_calc_spesfic_hour',
            label: __('Calc Real Hours'),
            fieldtype: 'Check',
        },



	]
};
