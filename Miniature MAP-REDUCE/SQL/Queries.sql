SELECT Score, COUNT(*), SUM(HelpfulnessNumerator), AVG(HelpfulnessNumerator)
FROM data
WHERE Score > 0
GROUP BY Score