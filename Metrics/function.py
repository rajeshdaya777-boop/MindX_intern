result_revenue = sales_order_time_filter_query(
    metric='product_quantity',
    time_period='monthly',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("Product Quantity:", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='product_revenue',
    time_period='monthly',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("Product Revenue:", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='product_profit',
    time_period='annually',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025'
)
print("Product Profit:", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='product_profit_margin',
    time_period='monthly',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("Product Profit Margin:", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='sales_order_revenue',
    time_period='monthly',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("Top Revenue:", result_revenue)

result_cogs = sales_order_time_filter_query(
    metric='sales_order_cogs',
    time_period='quarterly',
    organization_id='10',
    limit=5,
    order_direction='ASC',
    specific_period='2025-Q1'
)
print("Top COGS:", result_cogs)

result_profit = sales_order_time_filter_query(
    metric='sales_order_profit',
    time_period='annually',
    organization_id='10',
    limit=5,
    order_direction='ASC',
    specific_period='2025'
)
print("Top Profit:", result_profit)

result_profit_margin = sales_order_time_filter_query(
    metric='sales_order_profit_margin',
    time_period='annually',
    organization_id='10',
    limit=5,
    order_direction='DESC',
    specific_period='2025'
)
print("Top Profit Margin:", result_profit_margin)

result_revenue = sales_order_time_filter_query(
    metric='customer_revenue',
    time_period='monthly',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("customer_revenue:", result_revenue)

result_purchase_spend = purchase_order_time_filter_query(
    metric='purchase_spend',  
    time_period='monthly',  
    organization_id='10', 
    limit=5,  
    order_direction='DESC',  
    specific_period='2025-01'  
)
print("Purchase Spend Amount:", result_purchase_spend)

result_purchase_spend = purchase_order_time_filter_query(
    metric='purchase_orders',  
    time_period='monthly',  
    organization_id='10',  
    limit=5,  
    order_direction='DESC',  
    specific_period='2025-01'  
)
print("Purchase Order:", result_purchase_spend)

# Get Total Production Orders
result_production_orders = manufacturing_time_filter_query(
    metric='production_orders',  
    time_period='annually',  
    organization_id='10',  
    limit=5,  
    order_direction='DESC',  
    specific_period='2025'  
)
print("Production Orders:", result_production_orders)

result_revenue = sales_order_time_filter_query(
    metric='revenue_cogs_profit_query',
    time_period='annually',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-01'
)
print("Revenue Cogs :", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='customer_metrics_query',
    time_period='annually',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025'
)
print("Customer query :", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='top_customers_query',
    time_period='annually',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-02'
)
print("Customer query :", result_revenue)

result_revenue = sales_order_time_filter_query(
    metric='customer_performance_query',
    time_period='annually',
    organization_id='10',
    limit=10,
    order_direction='DESC',
    specific_period='2025-02'
)
print("Customer performance :", result_revenue)

item_sku = fetch_item_details(
    identifier='1051',
    identifier_type='sku',
    time_period='monthly',
    specific_period='2025-01',
    organization_id='10'
)
print("Item Details by SKU:", item_sku)

item_name = fetch_item_details(
    identifier='Item 1',
    identifier_type='name',
    time_period='monthly',
    specific_period='2025-01',
    organization_id='10'
)
print("Item Details by Name:", item_name)

result_customer_metrics = fetch_customer_details_by_name(
    contact_name='Rajesh',
    organization_id='10',
    time_period='annually',  # This can be monthly, quarterly, half_yearly, or annually
    specific_period='2024',  # Pass the year for annual query
    limit=10
)

print("Customer query:", result_customer_metrics)
