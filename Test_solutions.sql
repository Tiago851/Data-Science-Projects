'''
Not an actual script, only my attempt at solving the SQL test from the classes.

Test questions are uploaded here too.

'''

'1'

SELECT * FROM cd.facilities

'2'

SELECT name,membercost FROM cd.facilities

'3'

SELECT * FROM cd.facilities
WHERE membercost != 0 

'4'

SELECT * FROM cd.facilities
WHERE membercost < monthlymaintenance/50 AND membercost != 0

'5'

SELECT * FROM cd.facilities
WHERE name ILIKE '%TENNIS%'

'6'

SELECT * FROM cd.facilities
WHERE facid % 2 != 0 AND facid <= 5 AND facid != 3

'7'

SELECT memid,surname,firstname,joindate FROM cd.members
WHERE joindate > '2012-09-01'

'8'

SELECT DISTINCT(surname) FROM cd.members
ORDER BY surname
LIMIT 10

'9'

SELECT MAX(joindate) FROM cd.members

'10'

SELECT COUNT(*) FROM cd.facilities
WHERE guestcost >= 10 

'11'

SELECT facid,SUM(slots) FROM cd.bookings
WHERE starttime BETWEEN '2012-09-01' AND '2012-10-01'
GROUP BY facid
ORDER BY facid

'12'

SELECT facid,SUM(slots) AS total_slots FROM cd.bookings
GROUP BY facid
ORDER BY total_slots DESC
LIMIT 5

'13'

SELECT name,starttime FROM cd.bookings
INNER JOIN cd.facilities
ON cd.bookings.facid = cd.facilities.facid
WHERE TO_CHAR(starttime, 'YYYY-MM-DD') = '2012-09-21' AND name ILIKE '%TENNIS%COURT%'

'14'

SELECT starttime FROM cd.bookings
INNER JOIN cd.members
ON cd.bookings.memid = cd.members.memid
WHERE firstname = 'David' AND surname = 'Farrell'