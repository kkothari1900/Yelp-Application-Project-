--update numCheckins
update yelp_business
set numCheckins = subquery.ct
from(
select yelp_business.business_id, count(checkin_time) as ct
from checkins, yelp_business
where checkins.business_id = yelp_business.business_id
group by yelp_business.business_id) as subquery
where yelp_business.business_id = subquery.business_id;

--update numTips
update yelp_business
set numTips = subquery.ct
from(
select yelp_business.business_id, count(user_id) as ct
from yelp_tips, yelp_business
where yelp_tips.business_id = yelp_business.business_id
group by yelp_business.business_id) as subquery
where yelp_business.business_id = subquery.business_id;

--update totalLikes
update yelp_user
set totallikes = subquery.ct
from(
select yelp_user.user_id, sum(likes) as ct
from yelp_tips, yelp_user
where yelp_tips.user_id = yelp_user.user_id
group by yelp_user.user_id) as subquery
where yelp_user.user_id = subquery.user_id;

--update tipcount
update yelp_user
set tipcount = subquery.ct
from(
select yelp_user.user_id, count(yelp_user.user_id) as ct
from yelp_tips, yelp_user
where yelp_tips.user_id = yelp_user.user_id
group by yelp_user.user_id) as subquery
where yelp_user.user_id = subquery.user_id;