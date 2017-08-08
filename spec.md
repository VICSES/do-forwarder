Background
==========

VICSES
------

The Victoria State Emergency Service (VICSES) is the lead response agency in Victoria for storm, flood, tsunami and earthquake events. For much of Victoria it is also the principal rescue response, this is most commonly extracting people from vehicle accidents but also includes industrial and agricultural incidents, and freeing stuck children. As part of Victoria's unified emergency response VICSES assists other agencies where required, a common example of this is assisting police in search and rescue incidents. Finally VICSES tends to get the jobs that don't cleanly fit any other agency, a favourite personal example was "Bird up tree".

VICSES is a volunteer response organisation with roughly 5600 volunteers. There are TODO units across the state, each unit has an assigned area to cover and responds to events in that area. Every member of unit responds as a volunteer, units are managed by a combination of operational and non-operational volunteers. Staff are employed in state and region offices to provide administration and high level operational management, some staff also volunteer at a unit.

This spec is designed for the Bellarine unit of VICSES. The Bellarine unit is located south of Geelong and covers the area from Leopold down to Queenscliff.

Initial Response
----------------

When a response is required a member of the public calls 000 or 1300 TODO, these calls are handled by TODO (ESTA), the Victorian emergency dispatch group.

The relevant unit is then sent a page with the basic details of the job.

Each unit has an assigned duty officer (DO), essentially an on call position. The duty officer contacts ESTA to acknowledge receipt of the job. The DO then organises the unit's response.

The Bellarine, like many units, manages this by sending a page to all members requesting that they contact the DO to indicate availability. The DO then directs them to either attend direct to the unit or direct to scene. The DO may send further pages when sufficient members have responded, if more members are required or if members with specialised skills are required.

Due to the nature of some jobs all interactions with ESTA and the duty officer are logged. Duty officers do this by recording each interaction in a notebook.

For time critical events portions of the response are short cutted. Members respond to the unit or scene as soon as the initial page is sent and notify the duty officer when they can.

DO Management
-------------

As each duty officer is on call the Bellarine unit is careful to share the load across a number of members. Each day is divided into two shifts, from 7am to 6pm and from 6pm to 7am. There is a mobile phone which receives all the incoming DO calls, this is redirected to whoever is on duty at the time. A member manually sets the redirect at each change of shift.

The redirection is a multiple step process. The receiving member is contacted by SMS to ensure that they are ready to start their shift. The phone is then transferred. The relieved member is then informed that they are off duty and who has taken it on, this allows them to pass on information if necessary.

It is also important to have some flexibility in the process. If a job is ongoing transfer will often be delayed until it has been completed. Events may occur during a day, such as a dentist visit, which necessitate temporarily transferring the duty officer number. When significant events occur, such as a large number of jobs, an incident management team will be established and the duty officer role will be transferred to that team.

Goal
====

The goal is to build a system to manage the duty officer phone number so that a volunteer does not have to manage each change of shift by hand.

The ability to handle SMS messages would be a significant improvement.

A log of all calls and messages is desirable.

Requirements
------------

* Reliability
  - a total failure can be managed, a partial failure must be avoided
* Ease of use
  - general volunteers should not realise a system exists
  - duty officers should not require skills beyond basic phone literacy
  - managers should not require skills beyond basic computer literacy
* Stand alone
  - the system must not rely on systems not under the control of the unit
  - contracted services are ok, lock in contracts should be avoided
* Comply with Vic gov security requirements
  - Australian based backend


Release Plan
============

Version 1
---------

DIDWW provides VOIP Direct In Dial (DID) numbers which can receive voice and SMS numbers.

Have a system which redirects all incoming calls and SMS to a designated number.

Be able to change the designated number to any number of the approved list via SMS.


Version 2
---------

Have a schedule of who is on duty and when.

Contact the next duty person via SMS to check availability 5min before the allotted time.

Send a second SMS after 10 minutes if there is no response.

If there is no response 5 minutes after the second SMS notify the current duty person of an issue with the transfer.


Version 3
---------

Log every SMS sent and received: timestamp, to, from, body, final status

Log every phone call received: timestamp, to, from, duration, final status

Email a copy of the relevant log to the outgoing duty officer each time the duty officer changes.

Email a copy of the days log to the Bellarine unit email address at 5am.


Version 4
---------

Provide a live feed of events to be consumed by other services.


Interface
=========

### :transfer <phone number>
### :transfer <name>

Immediately transfer the duty officer phone to the specifier number or name.

The number must be a known and approved number.

The incoming number must be a known and approved number.




