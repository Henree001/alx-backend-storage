-- Creates a stored procedure ComputeAverageScoreForUser that
-- computes and stores the average score for a student.

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
DECLARE score FLOAT(10, 2);
SELECT AVG(corrections.score)
INTO score 
FROM corrections
WHERE corrections.user_id = user_id;

UPDATE users
SET users.average_score = score
WHERE users.id = user_id;
END$$
DELIMITER ;
