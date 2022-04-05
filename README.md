This document provides an overview of this nate tech submission.

### Setup Guide

To spin the application up locally run the following command from the root directory of the repo.

```
docker-compose up -d
```

With this, containers for the api, celery, redis and postgres will be span up.
The application is served on port 8004.

To see the API documentation open the following:
```
localhost:8004/docs
```

### Endpoints

There are a number of endpoints which can be used.

#### GET health/

Returns the health status of other services.
This response will be in the form:
```
{
  "service_a": "HEALTHY",
  "service_b": "UNHEALTHY",
}
```


#### POST pages/

Creates a page object and kicks off a task to scrape the given `target_url`.

This endpoint will return the ID of the new `Page` object:
```
{
  "page_id": 1,
}
```


#### GET pages/

Lists out the page objects in full


#### GET pages/{page_id}/

Retrieves the individual page object and the corresponding results.
The results can be ordered with the query parameter `ordering`.
