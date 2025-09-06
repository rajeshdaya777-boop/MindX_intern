tools = [
    {
        "type": "function",
        "function": {
            "name": "sales_order_time_filter_query",
            "description": "Fetch the top or low-performing metrics for products, customers, or sales orders based on a specific metric and and time period (monthly, quarterly, half-yearly, or annually).",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "description": "The metric to rank products by. Possible values: 'quantity', 'revenue', 'profit', 'profit_margin'.",
                        "enum": ["product_quantity", "product_revenue", "product_profit", "product_profit_margin",
                            "customer_profit_margin", "customer_profit", "customer_quantity", "customer_revenue",
                            "sales_order_profit_margin", "sales_order_profit", "sales_order_cogs", "sales_order_revenue"]
                    },
                    "time_period": {
                        "type": "string",
                        "description": "The time period for filtering the products. Possible values: 'monthly', 'quarterly', 'half_yearly', 'annually'.if not given anything about time period use monthly",
                        "enum": ["monthly", "quarterly", "half_yearly", "annually"]
                    },
                    "specific_period": {
                        "type": "string",
                        "description": "The specific period for the chosen time period. Format: 'YYYY-MM' for monthly, 'YYYY-QX' for quarterly, 'YYYY-HX' for half-yearly, or 'YYYY' for annually.",
                        "default": "Use Current Year and August Month as 2024-08"
                    },
                    "order_direction": {
                    "type": "string",
                    "description": "The direction of sorting. Use 'DESC' for top products and 'ASC' for low-performing products.",
                    "enum": ["ASC", "DESC"],
                    "default": "DESC"
                   },
                    "limit": {
                        "type": "integer",
                        "description": "The number of top products to return.",
                        "default": 5
                    }
                },
                "required": ["metric", "time_period", "specific_period", "limit"]
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "purchase_order_time_filter_query",
            "description": "Fetch the top or low-performing purchase order based on a specific metric (purchase_spend,purchase_orders) and time period (monthly, quarterly, half-yearly, or annually).",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "description": "The metric to rank products by. Possible values: 'purchase_orders','purchase_spend'.",
                        "enum": ["purchase_spend","purchase_orders"]
                    },
                    "time_period": {
                        "type": "string",
                        "description": "The time period for filtering the products. Possible values: 'monthly', 'quarterly', 'half_yearly', 'annually'.if not given anything about time period use monthly",
                        "enum": ["monthly", "quarterly", "half_yearly", "annually"]
                    },
                    "specific_period": {
                        "type": "string",
                        "description": "The specific period for the chosen time period. Format: 'YYYY-MM' for monthly, 'YYYY-QX' for quarterly, 'YYYY-HX' for half-yearly, or 'YYYY' for annually.",
                        "default": "Use Current Year and August Month as 2024-08"
                    },
                    "order_direction": {
                    "type": "string",
                    "description": "The direction of sorting. Use 'DESC' for top products and 'ASC' for low-performing products.",
                    "enum": ["ASC", "DESC"],
                    "default": "DESC"
                   },
                    "limit": {
                        "type": "integer",
                        "description": "The number of top products to return.",
                        "default": 5
                    }
                },
                "required": ["metric", "time_period", "specific_period", "limit"]
            }
        }
    },
       {
        "type": "function",
        "function": {
            "name": "fetch_item_details",
            "description": "Fetch item details based on SKU or item name, with optional time filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "The SKU or item name based on identifier_type."
                    },
                    "identifier_type": {
                        "type": "string",
                        "description": "Specify whether the identifier is 'sku' or 'name'.",
                        "enum": ["sku", "name"]
                    },
                    "organization_id": {
                        "type": "string",
                        "description": "The organization ID to filter by. Default is '10'.",
                        "default": "10"
                    },
                    "time_period": {
                        "type": "string",
                        "description": "The time period for filtering the data. Possible values: 'monthly', 'quarterly', 'half_yearly', 'annually'. Default is None.",
                        "enum": ["monthly", "quarterly", "half_yearly", "annually"]
                    },
                    "specific_period": {
                        "type": "string",
                        "description": "The specific period for the chosen time period. Format: 'YYYY-MM' for monthly, 'YYYY-QX' for quarterly, 'YYYY-HX' for half-yearly, or 'YYYY' for annually. Default is None."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of results to return. Default is 10.",
                        "default": 10
                    }
                },
                "required": ["identifier", "identifier_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_customer_details_by_name",
            "description": "Fetch customer details based on customer name with optional time filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {
                        "type": "string",
                        "description": "The name of the customer."
                    },
                    "organization_id": {
                        "type": "string",
                        "description": "The organization ID to filter by. Default is '10'.",
                        "default": "10"
                    },
                    "time_period": {
                        "type": "string",
                        "description": "The time period for filtering the data. Possible values: 'monthly', 'quarterly', 'half_yearly', 'annually'. Default is None.",
                        "enum": ["monthly", "quarterly", "half_yearly", "annually"]
                    },
                    "specific_period": {
                        "type": "string",
                        "description": "The specific period for the chosen time period. Format: 'YYYY-MM' for monthly, 'YYYY-QX' for quarterly, 'YYYY-HX' for half-yearly, or 'YYYY' for annually. Default is None."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of results to return. Default is 10.",
                        "default": 10
                    },
                    "order_direction": {
                        "type": "string",
                        "description": "The direction to order the results. Can be 'ASC' or 'DESC'. Default is 'DESC'.",
                        "enum": ["ASC", "DESC"],
                        "default": "DESC"
                    }
                },
                "required": ["contact_name"]
            }
        }
    }
]
