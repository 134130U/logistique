with stock as (select  a.id as product_id,a.created_at,serial,d.name as product,a.etat,d.prefix,
				case when d.prefix is not null then right(serial,length(serial) - length(d.prefix)) else serial end  as true_serial,
b.stock_type,c.locality as region,is_main_system,main_system_id,first_main_system_id,
b.name as stock_name,s.name as systems,
case when s.name isnull then d.name else s.name end as product_type,d.category,
case when b.tenant_id = 1 then 'Senegal'
	when b.tenant_id = 2 then 'Mali'
    when b.tenant_id = 3 then 'Nigeria'
    When b.tenant_id = 4 then 'Burkina'
    when b.tenant_id = 5 then 'Niger'
 	when b.tenant_id = 6 then 'Cameroun'
    else  'others' end as country,
case when lower(b.name) like '%zzz%' or lower(b.name) like '%yyy%' or lower(b.name) like '%xxx%' then True else False end is_archived
from public.stocks_products sp
inner join (select * from public.products)a on product_id = a.id
inner join (select * from public.stocks )b on stock_id = b.id
inner join(select id as id_loc,name as locality,type_locality from public.localities)c on locality_id = c.id_loc
inner join(select * from public.product_types)d on a.product_type_id = d.id
left join(select * from system_types)s on a.system_type_id = s.id)
select now()::date - interval '1 day'  as date_at,to_char(now()::date - interval '1 day','yyyy-mm') as mois,*
from stock
left join(select serial_number,cost_price,carton_id from product_hashes)ph on ph.serial_number=true_serial
where lower(stock_name) not like '%test%' and lower(product) not like '%test%'