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

-- 3. Output the category of movies on which the most money was spent.

SELECT 
	category.name AS category_name,
	SUM(payment.amount) AS total_revenue
FROM category
JOIN film_category
    ON film_category.category_id = category.category_id
JOIN inventory
    ON inventory.film_id = film_category.film_id
JOIN rental
    ON rental.inventory_id = inventory.inventory_id
JOIN payment
    ON payment.rental_id = rental.rental_id
GROUP BY category.name
ORDER BY total_revenue DESC
LIMIT 1;

-- 4. Print the names of movies that are not in the inventory. 
-- Write a query without using the IN operator.

SELECT 
    film.film_id,
    film.title
FROM film
LEFT JOIN inventory
    ON inventory.film_id = film.film_id
WHERE inventory.inventory_id IS NULL;


-- 5. Output the top 3 actors who have appeared the most in movies in the “Children” category. 
-- If several actors have the same number of movies, output all of them.

WITH actor_children_films AS (
SELECT 
	actor.actor_id,
	actor.first_name,
	actor.last_name,
	COUNT(film_category.film_id) AS film_count
FROM actor
	JOIN film_actor
        ON film_actor.actor_id = actor.actor_id
    JOIN film_category
        ON film_category.film_id = film_actor.film_id
    JOIN category
        ON category.category_id = film_category.category_id
    WHERE category.name = 'Children'
    GROUP BY actor.actor_id, actor.first_name, actor.last_name
),
ranked AS(
	SELECT 
        actor_id,
        first_name,
        last_name,
        film_count,
        DENSE_RANK() OVER (ORDER BY film_count DESC) AS rank_position
    FROM actor_children_films
)
SELECT 
    actor_id,
    first_name,
    last_name,
    film_count
FROM ranked
WHERE rank_position <= 3
ORDER BY film_count DESC;
	
