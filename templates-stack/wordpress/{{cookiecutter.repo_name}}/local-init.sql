-- Database
USE fe45224d;

UPDATE dk583_options SET option_value = REPLACE(option_value, 'https://www.example.com', 'http://localhost:8080') WHERE option_name IN ('home', 'siteurl');

UPDATE dk583_posts SET post_content = REPLACE(post_content, 'https://www.example.com', 'http://localhost:8080');

UPDATE dk583_postmeta SET meta_value = REPLACE(meta_value, 'https://www.example.com', 'http://localhost:8080');
