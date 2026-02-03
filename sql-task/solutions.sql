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

SELECT
    actor.actor_id,
    actor.first_name,
    actor.last_name,
    COUNT(rental.rental_id) AS rental_count
FROM actor
JOIN film_actor
	ON actor.actor_id = film_actor.actor_id
JOIN inventory
    ON inventory.film_id = film_actor.film_id
JOIN rental
    ON rental.inventory_id = inventory.inventory_id
GROUP BY actor.actor_id, actor.first_name, actor.last_name
ORDER BY rental_count DESC
LIMIT 10;