-- test code with mistakes
select
    client_name,
    client_city,
    client_country,
    sum(revenue_total) as revenue_total
from reports.clients
group by 1, 2, 3
order by 1 asc;
