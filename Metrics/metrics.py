metrics_map = {
    # 1. Top or Low Selling Product by Quantity
    'product_quantity': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity) AS total_quantity_sold
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        ORDER BY total_quantity_sold {order_direction}
        LIMIT {limit};
    """,

    # 2. Top or Low Selling Product by Revenue
    'product_revenue': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,

    # 3. Top or Low Selling Product by Profit
    'product_profit': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) AS total_profit
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        ORDER BY total_profit {order_direction}
        LIMIT {limit};
    """,

    # 4. Top or Low Selling Product by Profit Margin
    'product_profit_margin': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) AS total_profit,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue,
            (SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        HAVING total_revenue > 0
        ORDER BY profit_margin_percentage {order_direction}
        LIMIT {limit};
    """,

    # 5. Top or Low Revenue from Sales Orders
    'sales_order_revenue': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,

    # 6. Top or Low Cost of Goods Sold (COGS) from Sales Orders
    'sales_order_cogs': """
        SELECT
            i.name AS 'name',
            SUM(sr.quantity * i.buying_price) AS cogs
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = 10
        GROUP BY i.id, i.name
        ORDER BY cogs DESC
        LIMIT 5;

    """,

    # 7. Top or Low Profit from Sales Orders
    'sales_order_profit': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) AS total_profit
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        ORDER BY total_profit {order_direction}
        LIMIT {limit};
    """,

    # 8. Top or Low Profit Margin from Sales Orders
    'sales_order_profit_margin': """
        SELECT
            i.name AS product_name,
            (SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name
        HAVING SUM(sr.quantity * sr.cost_per_unit) > 0
        ORDER BY profit_margin_percentage {order_direction}
        LIMIT {limit};
    """,

    # 9. Top or Low Revenue from Customers
    'customer_revenue': """
        SELECT
            c.company_name,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN customers c ON s.customer_id = c.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY c.company_name
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,

    # 10. Total Amount Spent on Purchases
    'purchase_spend': """
        SELECT
            SUM(po.total) AS total_purchase_spend
        FROM purchase_orders po
        WHERE po.organization_id =  %(organization_id)s
        {time_filter};
    """,

    # 11. Total Purchase Orders
    'purchase_orders': """
        SELECT
            COUNT(po.id) AS total_purchase_orders
        FROM purchase_orders po
        WHERE po.organization_id =  %(organization_id)s
        {time_filter};
    """,

    # 12. Revenue, COGS, Profit, Profit Margin
    'revenue_cogs_profit_query': """
        SELECT
            i.name AS product_name,
            SUM(sr.quantity * sr.cost_per_unit) AS revenue,
            SUM(sr.quantity * i.buying_price) AS cogs,
            SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) AS profit,
            (SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.name;
    """,

    # 13. Customer Metrics
    'customer_metrics_query': """
            SELECT
                s.customer_id,
                MIN(s.order_date) AS first_order_date,
                COUNT(DISTINCT s.id) AS total_orders,
                SUM(s.total) AS total_revenue
            FROM sales_orders s
            WHERE s.organization_id = %(organization_id)s
            {time_filter}
            GROUP BY s.customer_id
            LIMIT 5;

    """,

    # 14. Top Customers by Revenue
    'top_customers_query': """
        SELECT
            c.company_name,
            SUM(s.total) AS total_revenue
        FROM sales_orders s
        JOIN customers c ON s.customer_id = c.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY c.id, c.company_name
        ORDER BY total_revenue {order_direction}
        LIMIT 15;
    """,

    # 15. Customer Performance Report
    'customer_performance_query': """
        SELECT
            c.company_name,
            SUM(sr.quantity * sr.cost_per_unit) AS revenue,
            SUM(sr.quantity) AS quantity,
            SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) AS profit,
            (SUM(sr.quantity * (sr.cost_per_unit - i.buying_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_orders s ON sr.sales_order_id = s.id
        JOIN customers c ON s.customer_id = c.id
        JOIN items i ON sr.item_id = i.id
        WHERE s.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY c.id, c.company_name
        ORDER BY revenue {order_direction};
    """,

    #16.Items by SKU
    'item_sku' : """
        SELECT i.name, i.buying_price, i.selling_price
        FROM items i
        JOIN sales_orders s ON s.id = i.id
        WHERE i.sku = %(sku)s AND i.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.id
        LIMIT %(limit)s;
        """,

    #17.Items by name
    'item_name' : """
        SELECT i.sku, i.buying_price, i.selling_price
        FROM items i
        JOIN sales_orders s ON s.id = i.id
        WHERE i.name = %(name)s AND i.organization_id = %(organization_id)s
        {time_filter}
        GROUP BY i.id
        LIMIT %(limit)s;
      """,

    #17.Search customers by name
    'customers_by_name' : """
        SELECT
            c.contact_name,
            c.company_name,
            c.contact_email,
            c.contact_phone,
            CONCAT(b.street, ', ', b.city, ', ', b.state, ', ', b.zipcode) AS billing_address,
            CONCAT(s.street, ', ', s.city, ', ', s.state, ', ', s.zipcode) AS shipping_address
        FROM customers c
        LEFT JOIN addresses b ON c.billing_address = b.id
        LEFT JOIN addresses s ON c.shipping_address = s.id
        WHERE c.organization_id = %(organization_id)s
        AND c.contact_name = %(contact_name)s
        {time_filter}
        ORDER BY c.created_at {order_direction}
        LIMIT %(limit)s;

    """
}
