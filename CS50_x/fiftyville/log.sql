-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Căutăm raportul de crimă pentru furtul care a avut loc pe Humphrey Street pe 28 iulie 2023
SELECT * FROM crime_scene_reports
WHERE date = '2023-07-28' AND street = 'Humphrey Street';

-- Presupunând că raportul de crimă ne-a oferit numele martorilor, căutăm informații suplimentare de la aceștia.
-- Înlocuiește 'NumeMartor1' și 'NumeMartor2' cu numele reale găsite în raportul de crimă
SELECT * FROM interviews
WHERE person IN ('NumeMartor1', 'NumeMartor2');

-- Pe baza interviurilor martorilor, identificăm o posibilă oră a crimei și căutăm zboruri ce au plecat la scurt timp după aceea.
-- Înlocuiește `ora_crimei` cu ora aproximativă a furtului descoperită
SELECT * FROM flights
WHERE date = '2023-07-28' AND departure_time > 'ora_crimei';

-- Odată ce am identificat zborul suspect, verificăm lista de pasageri pentru a afla cine a călătorit pe acel zbor.
-- Înlocuiește 'IDulZborului' cu ID-ul zborului găsit în interogarea anterioară
SELECT * FROM passenger_manifest
WHERE flight_id = 'IDulZborului';

-- Confirmăm detalii despre hoț și complice, verificând în tabelul people.
-- Înlocuiește 'NumeHot' și 'NumeComplice' cu numele posibile ale hoțului și complicelui găsite în lista de pasageri
SELECT * FROM people
WHERE name IN ('NumeHot', 'NumeComplice');

