-- test code with mistakes
select
*,
sum(revenue_total) as revenue_total
from reports.clients
group by 1,2,3,4,5,6,7,8,9;
