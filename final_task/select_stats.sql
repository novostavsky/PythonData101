SELECT
	location,
	added_on,
	PERCENTILE_DISC(0.05) WITHIN GROUP (ORDER BY round( cast(price_usd as float) / cast(total_area as float), 2))
								OVER (PARTITION BY location, added_on) AS perc_05,
	PERCENTILE_DISC(0.95) WITHIN GROUP (ORDER BY round( cast(price_usd as float) / cast(total_area as float), 2))
								OVER (PARTITION BY location, added_on) AS perc_95
FROM [olx].[dbo].[Apartment]
WHERE (total_area <> 0) AND (price_usd <> 0)
