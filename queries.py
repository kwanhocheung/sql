import mysql.connector
from constants import Constants


class Queries(object):
    """Database queries"""
    connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)
    cursor = connection.cursor()

    """Retrieve the names and genders of all people associated with ARC (i.e., members, employees, etc.)"""
    query1 = """
        SELECT 
            name, gender 
        FROM 
            person;
    """

    """List the names and departments of all “Faculty” members who are also members of ARC. """
    query2 = """
        select p.name, u.department
        from non_student as n NATURAL JOIN member as m NATURAL JOIN university_affiliate as u NATURAL JOIN person as p
        where n.member_type="Faculty";
    """

    """Find the names of the people who were present in either the weight room or the cardio room on 2023-04-01."""
    query3 = """
        select DISTINCT p.name
        from space as s NATURAL JOIN location_reading as l INNER JOIN person as p on l.person_id=p.card_id
        where (s.description="cardio room" or s.description="weight room") and l.timestamp="2023-04-01 00:00:00";
    """

    """Find the names of the people who have attended all events."""
    query4 = """
        select person.name from person natural join
        (select card_id, count(card_id) as number_event from attends group by card_id) as t1
        where number_event=(select count(event_id) as number_event from events)  
    """

    """List the ID of events whose capacity have reached the maximum capacity of their associated space."""
    query5 = """
        select e.event_id
        from events as e INNER JOIN space as s on e.space_id=s.space_id
        where e.capacity >= s.max_capacity;
    """

    """Find the names of students who have used all the equipment located in the cardio room. """
    query6 ="""
        select t3.name from
        (select t2.name, count(t2.name) as name_count from(
        select name from person natural join student natural join usage_reading join 
        (select equipment_id from space natural join equipment where description="cardio room") as t1 on usage_reading.equipment_id=t1.equipment_id) as t2 group by t2.name) as t3
        where name_count = 
        (select max(t3.name_count) from (select count(t2.name) as name_count from(select name from person natural join student natural join usage_reading join 
        (select equipment_id from space natural join equipment where description="cardio room") as t1 on usage_reading.equipment_id=t1.equipment_id) as t2 group by t2.name) as t3)
    """

    """List the equipment ids and types for equipment that is currently available."""
    query7 ="""
        select equipment_id, equipment_type
        from equipment
        where is_available=1;
    """

    """Find names of all employees in ARC."""
    query8 = """
        select p.name
        from person as p natural join employee as e
    """

    """Retrieve the names of people who have attended an event in the yoga studio"""
    query9 = """
        select DISTINCT person.name
        from events natural join (select space.space_id from space where space.description="yoga studio") as t1 natural join attends natural join person
            
    """

    """Find all family members who have attended ‘Summer Splash Fest’. """
    query10 = """
        select distinct person.name
        from attends natural join (select events.event_id from events where events.description="Summer Splash Fest") as t1 natural join family natural join person
    """

    """Calculate the average hourly rate paid to all employees who are of student type at ARC"""
    query11 = """
        select AVG(salary_hour)
        from employee where employee_type="student"
    """

    """Find the name of the Trainer(s) with the 2nd highest average hourly rate"""
    query12 = """
        select person.name from Trainer join employee on Trainer.person_id=employee.card_id natural join person
        where employee.salary_hour=
        (select salary_hour
        from Trainer join employee on Trainer.person_id=employee.card_id
        group by salary_hour
        order by salary_hour desc limit 1,1)
        
        
    """

    """Find the ID of university affiliate(s) that have the highest number of family members that are ARC’s members."""
    query13 = """
        select card_id from university_affiliate natural join member join(
        select familyof, count(familyof) as num_family from family group by familyof) as t1 on familyof=card_id
        where num_family=(select max(num_family) from(select count(familyof) as num_family from family group by familyof) as t3)
        
    """

    """Find the ID of university affiliate(s) that attends the most events"""
    query14 = """
        select card_id from university_affiliate natural join(
        select card_id, count(card_id) as event_count from attends group by card_id) as t1
        where event_count=(select max(event_count) from(select count(card_id) as event_count from attends group by card_id) as t2)
    """

    """Find the ID of space(s) that contains the least number of equipment"""
    query15 = """
        select space_id from space natural join(
        select space_id, count(space_id) as e_count from equipment group by space_id) as t1
        where e_count=(select max(e_count) from(select count(space_id) as e_count from equipment group by space_id) as t2)
    """

    """Calculate the total number of days spent by Mekhi Sporer in the weight room."""
    query16 = """
        select count(timestamp) from person join location_reading on location_reading.person_id=person.card_id natural join space where person.name="Mekhi Sporer" and space.description="weight room"
    """

    """Find the names of member(s) who spent the most time(in days) in the cardio room in the month of May"""
    query17 = """
        select name from person natural join member join
        (select person_id, count(person_id) as d from space natural join location_reading where description="cardio room" and location_reading.timestamp between "2023-05-01" and "2023-05-31" group by person_id) as t1 on t1.person_id=member.card_id
        where t1.d=(select max(d) from (select count(person_id) as d from space natural join location_reading where space.description="cardio room" and location_reading.timestamp between "2023-05-01" and "2023-05-31" group by person_id) as t2)
    """

    """Find the spaces which have the lowest average occupancy per event."""
    query18 = """
        select space.description, t2.a from space join (select space_id, avg(t1.c) as a from events join (select event_id, count(event_id) as c from attends group by event_id) as t1 on events.event_id = t1.event_id group by space_id) as t2 on space.space_id=t2.space_id
        where t2.a = (select min(t2.a) from (select space_id, avg(t1.c) as a from events join (select event_id, count(event_id) as c from attends group by event_id) as t1 on events.event_id = t1.event_id group by space_id) as t2)
    """

    query19 = """
        select equipment_type, sum(t1.c), sum(t2.c), rank() over(order by sum(t4.a) desc) as r from equipment join (select equipment_id,count(timestamp) as c from usage_reading where usage_reading.timestamp between "2023-01-01" and "2023-06-30" group by equipment_id) as t1 on equipment.equipment_id=t1.equipment_id join
        (select equipment_id, count(distinct card_id) as c from usage_reading where usage_reading.timestamp between "2023-01-01" and "2023-06-30" group by equipment_id) as t2 on equipment.equipment_id=t2.equipment_id join
        (select t3.equipment_id, sum(t3.c) as a from(select equipment_id, count(card_id) as c from usage_reading where usage_reading.timestamp between "2023-01-01" and "2023-06-30" group by equipment_id) as t3 group by t3.equipment_id) as t4 on equipment.equipment_id=t4.equipment_id
        group by equipment_type
    """

    cursor.execute(query19)
    print(cursor.fetchall())