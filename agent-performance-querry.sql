WITH calls AS(
    SELECT
        agent,
        disposition,
        COUNT(*) AS call_count
    FROM
        five9.call_logs
    WHERE
        agent ~ '^(agent1|agent2|agent3)$'  -- Insert the agents here from the agents-who-said.sh script
    AND LOWER(list_name) 'convert|survey|age'
    AND timestamp >= dateadd('day', - 30, CURRENT_DATE)
    AND call_type = 'Outbound'
    AND contacted = TRUE
    AND campaign = 'IT Script'
    GROUP BY
        1,
        2
) 
SELECT
    disposition,
    SUM(call_count) AS disposition_count,
    min(t2.total_calls),
    round(
        (SUM(call_count) * 1.0) / min(t2.total_calls) * 100.0,
        2
    ) || '%' AS percentage_of_total_calls
FROM
    calls
-- CROSS JOIN (SELECT SUM(call_count) as total_calls FROM calls) t2
--, (SELECT SUM(call_count) as total_calls FROM calls) t2
JOIN (SELECT SUM(call_count) as total_calls FROM calls) t2 ON TRUE=TRUE
GROUP BY
    1
ORDER BY
    2 DESC;
