
-- Create an external table for the raw data stored in S3
CREATE EXTERNAL TABLE IF NOT EXISTS raw_data (
    url STRING,
    data STRING
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
ESCAPED BY '\\' 
LINES TERMINATED BY '\n'
LOCATION 's3://<your-S3-bucket>/data/';

-- Query to count the number of entries in the raw data
SELECT COUNT(*) AS total_entries
FROM raw_data;

-- Query to get the top 10 most scraped URLs
SELECT url, COUNT(*) AS frequency
FROM raw_data
GROUP BY url
ORDER BY frequency DESC
LIMIT 10;

-- Query to count the number of words in each scraped data entry
SELECT url, SUM(ARRAY_LENGTH(SPLIT(data, ' '))) AS word_count
FROM raw_data
GROUP BY url;
