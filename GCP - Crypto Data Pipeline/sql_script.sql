SELECT 
  name, 
  avg(current_price) as average_current_price
FROM `the-first-project-495311.crypto.market_data` 
group by name