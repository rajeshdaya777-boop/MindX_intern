def sales_order_time_filter_query(metric, time_period, organization_id='10', limit=10, order_direction=' ', **kwargs):

    time_params = {}

    # Determine time parameters based on the provided time_period
    if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

    elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, quarter = specific_period.split('-')
                time_params = {'year': year, 'quarter': quarter}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")

    elif time_period == 'half_yearly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, half = specific_period.split('-')
                time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
        else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

    elif time_period == 'annually':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year = specific_period
                time_params = {'year': year}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

    else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
    query = metrics_map.get(metric).format(
        time_filter=time_filters['sales_orders'].get(time_period),  # Updated table name
        order_direction=order_direction,
        limit=limit,
        organization_id=organization_id,
    )

    # Add time filter parameters like year, month, etc.
    # Execute the query with the provided time_params
    conn = connect_to_database()  # Assuming this is a function to connect to the database
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
    result = cursor.fetchall()
    return result


def purchase_order_time_filter_query(metric, time_period, organization_id = '10', limit=int,order_direction=' ',**kwargs):

   time_params = {}

    # Determine time parameters based on the provided time_period
   if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

   elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
           try:
              year = specific_period
              quarter = '2'
              time_params = {'year': year, 'quarter': quarter}
           except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")


   elif time_period == 'half_yearly':
         specific_period = kwargs.get('specific_period')
         if specific_period:
            try:
              year = specific_period
              half = '1'
              time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
         else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

   elif time_period == 'annually':
        specific_period = kwargs.get('specific_period')
        if specific_period:
          try :
            year = specific_period
            time_params = {'year': year}
          except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

   else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
   query = metrics_map.get(metric).format(
        time_filter=time_filters['purchase_orders'].get(time_period),
        order_direction=order_direction,
        limit=limit,
    )
  # Add time filter parameters like year, month, etc.
  # Execute the query with the provided time_params
   conn = connect_to_database()
   cursor = conn.cursor(dictionary=True)
   cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
   result = cursor.fetchall()
   return result


def fetch_item_details(identifier, identifier_type, organization_id='10', time_period=None, specific_period=None, limit=10):
    """
    Fetch item details based on either SKU or item name.

    :param identifier: SKU or item name based on identifier_type
    :param identifier_type: 'sku' or 'name' to determine search criteria
    :param organization_id: Organization ID (default: '10')
    :param time_period: Time filter type (e.g., 'monthly', 'quarterly', 'annually')
    :param specific_period: Specific period string (e.g., '2025-01' for monthly)
    :param limit: Limit number of results (default: 10)
    :return: Item details (sku, name, buying price, selling price)
    """
    time_params = {}
    
    # Determine time parameters based on the provided time_period
    if time_period == 'monthly':
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")
    
    elif time_period == 'quarterly':
        if specific_period:
            try:
                year, quarter = specific_period.split('-')
                time_params = {'year': year, 'quarter': quarter}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")
    
    elif time_period == 'half_yearly':
        if specific_period:
            try:
                year, half = specific_period.split('-')
                time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
        else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")
    
    elif time_period == 'annually':
        if specific_period:
            try:
                year = specific_period
                time_params = {'year': year}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")
    
    elif time_period is not None:
        raise ValueError(f"Unsupported time_period: {time_period}")
    
    # Determine the correct query and parameters based on identifier type
    if identifier_type == 'sku':
        metric = 'item_sku'
        param_key = 'sku'
    elif identifier_type == 'name':
        metric = 'item_name'
        param_key = 'name'
    else:
        raise ValueError("Invalid identifier_type. Use 'sku' or 'name'.")
    
    # Ensure metric exists in the metrics map
    if metric not in metrics_map:
        raise ValueError(f"Metric '{metric}' not found in metrics_map.")
    
    # Prepare the query by replacing the time_filter placeholder with the correct filter
    query = metrics_map.get(metric).format(
        time_filter=time_filters['sales_orders'].get(time_period, "")
    )
    
    # Merge parameters
    params = {
        'organization_id': organization_id,
        param_key: identifier,
        'limit': limit,  # Ensure limit is included in the params dictionary
        **time_params
    }
    
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
    finally:
        # Close connection
        cursor.close()
        conn.close()
    
    return result


def fetch_customer_details_by_name(contact_name, organization_id='10', time_period=None, specific_period=None, limit=10, order_direction='DESC'):
    """
    Fetch customer details based on customer name with optional time filters.

    :param contact_name: Name of the customer.
    :param organization_id: Organization ID (default: '10')
    :param time_period: Time filter type (e.g., 'monthly', 'quarterly', 'annually')
    :param specific_period: Specific period string (e.g., '2025-01' for monthly)
    :param limit: Limit number of results (default: 10)
    :param order_direction: The direction to order the results, either 'ASC' or 'DESC' (default: 'DESC')
    :return: Customer details (name, contact info, sales data, etc.)
    """
    time_params = {}
    time_filter = ""
    
    # Determine time parameters based on the provided time_period
    if time_period in time_filters['customer_time_filters']:
        if specific_period:
            try:
                if time_period == 'monthly':
                    year, month = specific_period.split('-')
                    time_params = {'year': year, 'month': month}
                elif time_period == 'quarterly':
                    year, quarter = specific_period.split('-')
                    time_params = {'year': year, 'quarter': quarter}
                elif time_period == 'half_yearly':
                    year, half = specific_period.split('-')
                    time_params = {'year': year, 'half_year': half}
                elif time_period == 'annually':
                    year = specific_period
                    time_params = {'year': year}
                time_filter = " AND " + time_filters['customer_time_filters'][time_period]
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period} for {time_period}.")
        else:
            raise ValueError(f"specific_period is required for {time_period} time period.")
    
    # Ensure the correct metric (customer by name) is used for the query
    metric = 'customers_by_name'
    if metric not in metrics_map:
        raise ValueError(f"Metric '{metric}' not found in metrics_map.")
    
    # Prepare the query with proper WHERE clause
    query = metrics_map.get(metric).format(
        time_filter=time_filter,
        order_direction=order_direction
    )
    
    # Merge parameters for the query execution
    params = {
        'organization_id': organization_id,
        'contact_name': contact_name,
        'limit': limit,  # Ensure limit is included in params dictionary
        **time_params
    }
    
    # Connect to the database and execute the query
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    conn.close()
    
    return result
  
