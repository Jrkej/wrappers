# WRAPPERS
It will provide a website for students to wrap their events of the day into a simple timetable cotaining their lectures and club events

# INTRODUCTION
This project came into existence because our team leader wasn't aware of the events of hackathon because of information overload so we created this application to help other lost souls like him(NO OFFENCE)

# INTERESTING FINDINGS
-While scrapping the time table for a student from official site of IITR timetable no PASSWORD is required to fetch the timetable.
-Though the official site asks for password but for fetching the timetable of perso its not at all required(as demonstratd in our site).
-I DON'T KNOW IF IT IS BUG OR SOMETHING PLANNED ON OFFICIAL site of IITR timetable, only sub batch and enrollment number is enough to fetc timetable.

# WHAT DOES IT DO?
-It uses `scrapping` to allow a student to just enter his/her name, enrollment number and sub-batch (`no PASSWORD required`) and get the complete details of his lectures.<br/>
-It also allows clubs to submit their event information with the requirement of a SECRETKEY(only accessible to club members).<br/>
-It allows a student to view the complete details of all the lectures and events to be held on a specific day.

# WHY TO USE?
AS you wouldn't want to end up confused and unorganised like our team leader. It would be better to be more aware about all the important occurences to be held on a speific day so students can prepare in advance.

# REQUIREMENTS
For this you need:-<br/>
<br/>
1.) Libraries<br/>
   > Flask<br/>
   > Date-Time<br/>
   > MySQL-connector-python<br/>
   > Requests<br/>
   > Hashlib<br/>     
2.) MySQL<br/>

# RUNNING THE CODE
Download the current repository and update your mySQL `passkey` in the constant section of setup.py and run setup.py<br/> 

# BENEFITS 
-It provides students a platform to view the occurences of a day with just their name.<br/>
-It ends the requirement of multiple whatsapp groups of different clubs to be updated about their events.<br/>

# FURTHER SCOPE
-Upgrading UI + weekly timetable, bit of security for users, updating and deleting of classes/events, showing no classes on working day holidays.

# CREDITS
-AKSHAT SRIVASTAVA - Backend and structure of site
-ARYAN GUPTA - Frontend
-VANSH GARG - Database management