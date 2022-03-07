USE jobsity_DEC_CURATED;
DROP VIEW IF EXISTS trips_w_average;
CREATE VIEW trips_w_average AS 
Select
A.*
,avg(A.trips_per_week) over(PARTITION BY region, `Year`, `Month`) trips_average_week
FROM 
(	SELECT 
		REGION,
		`Year` ,
		`Month` ,
		Week  , 
		sum(cnt_trips) trips_per_week
	FROM jobsity_DEC_CURATED.trips_detailed
	GROUP BY 
		REGION,
		`Year` ,
		`Month` ,
		Week
) A  
