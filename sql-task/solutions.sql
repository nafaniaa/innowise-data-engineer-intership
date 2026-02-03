-- 1. Output the number of movies in each category, sorted descending.
SELECT
	c.name AS category_name,
	COUNT(fc.film_id) AS film_count
FROM category c
JOIN film_category fc
	ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY film_count DESC;

-- 2. Output the 10 actors whose movies rented the most, sorted in descending order.