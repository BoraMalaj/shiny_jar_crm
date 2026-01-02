INSERT INTO transactions (transaction_date, amount, type, category_id, description, customer_id, payment_method)
SELECT 
    -- Generates a random date within the last 730 days (approx. 2 years)
    CURRENT_DATE - (random() * 730)::int AS transaction_date,
    -- Generates a random numeric(10,2) between 10.00 and 500.00
    (random() * (500 - 10) + 10)::numeric(10,2) AS amount,
    'income' AS type,
    (ARRAY[9, 10, 11, 12, 13])[floor(random() * 5 + 1)] AS category_id,
    'Randomized Transaction' AS description,
    cust_id AS customer_id,
    (ARRAY['card', 'paypal', 'bank_transfer', 'stripe'])[floor(random() * 4 + 1)] AS payment_method
FROM 
    -- Specifies the target customer IDs
    unnest(ARRAY[2, 3, 4]) AS cust_id,
    -- Generates 3 rows for each ID
    generate_series(1, 3);