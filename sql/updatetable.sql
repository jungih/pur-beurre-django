CREATE TABLE IF NOT EXISTS foods_temp AS
	SELECT code,
		   url,
		   product_name,
		   quantity,
		   brands,
		   categories_fr,
		   nutrition_grade_fr,
		   image_url,
		   countries_fr,
		   fat_100g,
		   saturated_fat_100g,
		   sugars_100g,
		   salt_100g
FROM foods_food;

TRUNCATE foods_temp;

COPY foods_temp
	FROM 'path/csv/fr.products.csv'
	CSV HEADER ENCODING 'utf-8' DELIMITER E'\t';

UPDATE foods_food a
	SET
		url = b.url,
		product_name = b.product_name,
		quantity = b.quantity,
		categories_fr = b.categories_fr,
		image_url = b.image_url,
		nutrition_grade_fr = b.nutrition_grade_fr,
		countries_fr = b.countries_fr,
		fat_100g = b.fat_100g,
		saturated_fat_100g = b.saturated_fat_100g,
		sugars_100g = b.sugars_100g,
		salt_100g = b.salt_100g
FROM foods_temp b
WHERE a.code = b.code;

DROP table foods_temp;
