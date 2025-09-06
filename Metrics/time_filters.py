# Define the mapping for time filters
time_filters = {
    'sales_orders': {  # Updated table name
        'monthly': "AND YEAR(s.order_date) = %(year)s AND MONTH(s.order_date) = %(month)s",
        'quarterly': "AND YEAR(s.order_date) = %(year)s AND QUARTER(s.order_date) = %(quarter)s",
        'half_yearly': "AND YEAR(s.order_date) = %(year)s AND CASE WHEN MONTH(s.order_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "AND YEAR(s.order_date) = %(year)s"
    },
    'purchase_orders': {  # Updated table name
        'monthly': "AND YEAR(po.order_date) = %(year)s AND MONTH(po.order_date) = %(month)s",
        'quarterly': "AND YEAR(po.order_date) = %(year)s AND QUARTER(po.order_date) = %(quarter)s",
        'half_yearly': "AND YEAR(po.order_date) = %(year)s AND CASE WHEN MONTH(po.order_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "AND YEAR(po.order_date) = %(year)s"
    },
    'customer_time_filters' : {
        'monthly': "YEAR(c.created_at) = %(year)s AND MONTH(c.created_at) = %(month)s",
        'quarterly': "YEAR(c.created_at) = %(year)s AND QUARTER(c.created_at) = %(quarter)s",
        'half_yearly': "YEAR(c.created_at) = %(year)s AND CASE WHEN MONTH(c.created_at) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "YEAR(c.created_at) = %(year)s"
}
}
