select distinct *,case when age<3 then '0 a 3 mois'
	when age>3 and age<6 then '3 a 6 mois'
	when age>6 and age<9 then '6 a 9 mois'
	when age>9 and age<12 then '9 a 12 mois'
	when age >12 then '> 12 mois' end bucket
from  (select unnest(products) as product_id,(extract (days from(now()::date - interval '1 day' - created_at)))/30 as age,created_at as recieved_at,type_movement,tenant_id from stock_movements
where type_movement='receiving')t 
