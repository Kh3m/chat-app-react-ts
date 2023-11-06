# Auth Service (v1)
The Auth Service is responsible for providing access control and authentication functionalities within the Fixam's microservices.  It verifies user credentials and enforces authorization policies based on predefined rules.

## Table of Contents
- [Policy File](#policy-file)
- [Writing Policies](#writing-policies)
  - [Policy Structure](#policy-structure)
  - [Rate Limiting](#rate-limiting)
  - [Endpoint Patterns](#endpoint-patterns)
- [Usage](#usage)
- [API Endpoint](#api-endpoint)
- [Tests](#tests)

## Policy File
The service utilizes a JSON policy file to determine access permissions for different endpoints within a microservice. The policy file defines the permissions, groups, and authentication requirements for each endpoint. Each service should have a corresponding policy file defined.

## Writing Policies
In order to structure policies to achieve the desired outcome, it's important to follow a specific pattern for defining access policies for various endpoints. This pattern involves setting up endpoint patterns and specifying access permissions for different HTTP methods.

### Policy Structure
A policy should have the following structure:
```json
{
  "rate_limit": {
    "default": "2/s",
    "admins": "10/m",
    "super_admins": "20/h"
  },
  "endpoints": {
    "/example": {
      "HTTP_METHOD": {
        "permissions": ["PERMISSION1", "PERMISSION2"],
        "groups": ["GROUP1", "GROUP2"]
      },
      ...
    },
    ...
  }
}
```
- `rate_limit`: A dictionary containing rate limit settings for users of various groups.
- `endpoints`: A dictionary containing endpoints as keys.
- `/example`: An endpoint (e.g., "/example") to define policies for.
- `HTTP_METHOD`: HTTP method (e.g., "GET", "POST", "PUT", "DELETE").
- `permissions`: An array of permissions required to access the endpoint.
- `groups`: An array of groups that the user must belong to.

### Rate Limiting
Rate limiting is applied to users based on their group memberships. Users who belong to none of the groups specified in the `rate_limit` setting will use the default rate limit.   
From the policy above:
- Users who belong to none of the specified groups will be able to make 2 requests per second.
- Users who belong to the `admins` group will be able to make 10 requests per minute.
- Users who belong to the `super_admins` group will be able to make 20 requests per hour.

You can add or remove groups from the `rate_limit` setting at any time. For example, if you want to add a new group called editors with a rate limit of 5 requests per minute, you can simply add the following line to the rate_limit setting:
```json
"editors": "5/m"
```
You do not need to update any code to accommodate the new group(s).

### Endpoint Patterns
For endpoints that follow a pattern, use the asterisk (\*) to denote a wildcard in the policy file and use `{id}` to denote points for ids. For example, to match all endpoints starting with "/store", use "/store/*". To match endpoints with an ID "/store/123-unique-id/vendor", use "/store/{id}/vendor".

#### Examples
To match endpoints without and with an ID:
```json
{
  "endpoints": {
    "/product": {
      "GET": { "permissions": [], "groups": [] },
      "PUT-PATCH": { "permissions": ["OWNER"], "groups": ["ADMINS"] }
    },
    "/product/{id}/": {
      "GET": { "permissions": [], "groups": [] },
      "PUT": { "permissions": ["OWNER"], "groups": ["ADMINS"] },
      "POST-DELETE": { "permissions": ["OWNER"], "groups": ["ADMINS"] }
    }
  }
}
```

Wildcard Endpoint:
```json
{
  "endpoints": {
    "/store*": {
      "GET": { "permissions": [], "groups": [] },
      "PUT": { "permissions": ["OWNER"], "groups": ["ADMINS"] }
    }
  }
}
```

## Usage
To utilize the Authorization and Authentication Service, you can utilize the provided API endpoint (Evaluate_request) to evaluate a request against the defined policies.

## API Endpoint
**POST /evaluate_request/**
Evaluate a request to determine if the user has the necessary permissions and belongs to the required groups for the specified endpoint.

Request Parameters:

- `method` (str): The HTTP method being used (e.g., "GET", "POST", "PUT", "DELETE").
- `auth_token` (str): User's authorization token.
- `request_path` (str): Path to the requested resource (e.g., "/store/vendor").

Response:
- result (bool, int): 
  - bool: True if the user is authorized to access the endpoint, False otherwise.
  - int: HTTP status code representing the outcome of the authorization check.
      - 200: Authorized access.
      - 401: Authentication failure.
      - 403: Forbidden (unauthorized) access.
      - 500: Failed to load policy for the service (internal server error).

## Tests
This service currently doesn't have automated tests.
