## Project Analysis

This document outlines some initial thoughts on this solution.
Think of it as a dumping ground for some of my thinking.
Hopefully this should provide a steer on my approach and 
the direction in which I would take this project if it were for real.


### Design Choices

I've made some design choices which are not perfect. 
In this section I'll try and describe these.

#### Use of Celery for async task execution

The computation of scraping a URL for text and getting stats was handed off to `Celery`.
This would not be without a cost. 

There are a number of things to be considered with asynchronous task queue/job systems:
  - Overhead associated with sending a task message to the broker (`Redis`).
  - Overhead associated with the worker reserving the task before consuming it.
  - Additional points of failure:
    - If `Redis` goes down then task messages which have not yet been consumed will be lost.
    - If `Celery` goes down then the tasks which are in the process of being consumed will be lost.
`Celery` has a reputation of being heavyweight and hard for developers to understand. 
It is certainly not as simple as something like RQ but its complexity is overstated in my opinion and 
it is certainly a robust solution.

By handing this computation off to Celery, this is non-blocking to the webapp. 
With this configuration, the webapp can fire an outbound request for the task and continue serving inbound requests.
The alternative of keeping this computation within the webapp would technically remove the additional overhead that 
we get with async job/queue systems like `Celery` but would mean the webapp would have to service 
that request in its entirety before proceeding. 
One might argue that you could scale out the webapp with Gunicorn workers for this purpose, but this could be 
considered a violation of the webapp's responsibility. 
In a distributed system, the webapp should be concerned with handling requests and 'asking' other services for 
the things it needs to fulfil those requests.

#### API design follows async request response pattern

The design of the API is heavily influenced by the job/queue system which is in place.
Whereby the user sends a `POST` request to `pages/` and immediately receives an identifier.
The onus is then on the user to send retrieve the results when they are available with a `GET` request to `pages/{id}`.

Clearly a trade-off has been made here as to the ease of use of the API in favour of supporting the job/queue system,
which in turn lends itself to scalability.

Also note that the response from the `POST` request to `pages` contains an identifier for the `Page` object.
This identifier is currently the `ID` of the database record. 
This is problematic as the internal details of the db should not be exposed like this. 
If I had more time, I'd set a uuid on the `Page` object and use that as an identifier. 
UUIDs are unique across tables and can be used as an identifier across deployments. 
There's still a valid argument to be made that a UUID takes up a lot more space than the ID would.
For a similar reason, I did not use that task id as the identifier as this would expose the internal implementation
details about the use of `Celery`. This is the age old thing of depending on abstractions not implementations.


#### Storage of results in JSON field on Page object

This choice was made with time constraints in mind. When the service scrapes a given page it will store the counted
results directly on a JSON field in the db. This isn't great for a number of reasons. 
But if I was designing this service for real I'd probably consider storing the results in a NoSQL db like `MongoDB`,
due to the nature of the data (key:value) and that its size is fairly unpredictable.


#### Choice of framework

I used FastAPI as it has quite a lightweight feel to it. It lends itself fairly well to a thin API service like 
this solution especially when compared to something like Django. 
But at the same time you get a lot of things for free like swagger docs & validation/serialization, 
that isn't necessarily the case for something like Flask.


### Areas for improvement

#### Logging

There is no logging at all throughout the application, this would obviously be a pain point.
Especially considering the risk of failures with scraping a page.

#### Frontend

There is also no front end aspect to the application, it is currently just a light API service.


#### Pagination

There is no pagination on responses from the API. Clearly this would be a necessity in production.


#### Docstrings / Type hints

Inconsistent use of docstrings & type hints. Primarily due to time constraints.
