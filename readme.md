# Objective
Write a server that echoes back whatever string a client sent through an API

## Requirements
1. **The server is written in the language of your choice:**  
   The language of choice is Python.
2. **The server must have the ability to communicate with multiple clients:**  
   The framework chosen, Flask, provides native support for treading and
   concurrent client connections.
3. **The source must live in a code repository with access to history of
   commits:**  
   The source code is uploaded to
   [GitHub](https://github.com/thehungryturnip/echo_room/)
4. **There must be unit tests to cover at least the API:**  
   Unit tests are implemented using Python's `unittest` module and included in
   `./tests.py`.
5. **Discuss what good SLOs would look like to understand the operational
   health:**  
   See below section on [Service Level Objectives](#service-level-objectives).
   This is an area I have limited experince in and would be a focus of my
   learning/upskilling given the opportunity.

## Bonuses
1. **You have a Makefile to easily build and demonstrate your server:**  
   The service is packgade with its own virtual environment. See
   Installation, Run, and Test sections below.
2. **You have good quality documentation as part of your code:**  
   I aimed to have clearly written code that doesn't require too much
   commenting, with enough docstrings and `print()` to provide enough conext.
3. **Communication between the client and the server is encrypted and
   authenticated:**  
   Encryption is provided through SSL and aunthetication is provided through
   auth tokens.
4. **Prepare critical code paths for monitoring  / SLIs:**  
   This is also an area I don't have much experience in and would be a focus of
   my learning if given the opportunity.

# Installation, Run, and Test
1. Clone the repository:
    
    > git clone https://github.com/thehungryturnip/echo_room

2. Create a virtual environment:

    > python -m venv env

3. Activate the virtual environment:

    > source env/bin/activate

4. Install dependencies:

    > python -m pip install -r reqs.txt

5. The service can be run by executing the `./app.py` file (ctrl-c when done):

    > python ./app.py

6. The tests can be run by executing the `./tests.py` file:

    > python ./tests.py

6. Deactivate the virtual environment:

    > deactivate

# Design
## Fremework
The Flask framework, along with Flask RESTful, is used to implement this
sevice. It provides the basis for implementing APIs and provide native support
for processing requests in parellel.

Python's unittest module is used for unit testing.

## Encryption
SSL is used to secure the communication channel between the client and the
server. Self-signed certificates are used for this exercise.

## Authentication
API authentication tokens are used to confirm the identity of the API caller.

For simplicity, a database is not used for this exercise. Mechanisms for user
sign-up, password-based authentication, auth token generation, auth token
rotation, etc. are not implemented. Switching to session-key based
authentication after authenicataion check is also not implemented.

## APIs
### Hello
This is a simple API that implements the GET request and simply responds with 1
key-value pair: `'Hello': 'Welcome to the Echo Room.'`. The intention is for
this to be a check that the server is up and running.

### Echo
This is the main API that implements the POST request. The expect syntax is as
follows:

    {
        auth: <authorization token>
        str: <string to be reflected back to the caller>
    }

The API validates that the authorization token is provided and valid, then
reflects the string passed in  back to the caller in a respons of this format:

    {
        str: <string reflected back to the caller>
    }

## SLOs
I think of SLOs as what the consumer and risk management should be
experincing/expecting and then extrapolate to finer sub-SLOs we can measure and
improve on. e.g.

* Authenticating to the Echo API should take less than 500ms 99% of the time.
    * The amount of time for the request hitting our load balancer to getting
      to the authentication microservice should be less than 50ms.
    * The amount of time for the microservice to process an authentication
      request should be lass than 100ms.
    * The amount of time for the responses from microservices to exit our
      perimiter should be less than 50ms.
    * The authentication microservices should scale so that there's always more
      than 10% capacity buffer/reserve.
    * The disaster recovery infrastructure should be availablle 99.5% of the
      time.
* The Echo API should return its repsonse in less than 500ms 99% of the time.
    * The amount of time for the request hitting our load balancer to getting
      to the echo microservice should be less than 50ms.
    * The amount of time for the microservice to process echo request should be
      lass than 100ms.
    * The amount of time for the responses from microservices to exit our
      perimiter should be less than 50ms.
    * The echo microservices should scale so that there's always more than 10%
      capacity buffer/reserve.
    * The disaster recovery infrastructure should be availablle 99.5% of the
      time.
* (In the cases where the operations are more complex.) The string reflected
  back by the Echo API should always be correct.
    * The percentage of correct responses sent from the echo microservice
      should be 100%.
* Revocation of authorization should take effect in less than 5 minutes.
    * The time it takes for an auth token deletion request to be submitted to
      when the auth token is removed from the database should be less than 3
      minutes.
* 99% of malformed requests should be not be processed. (We'll need to define
  what the critea for "malformed" is for this context.)
    * 99.9% of requests with scripts in the request should not reach the echo
      microservice. (Should be dropped by the web application firewall.)
    * 100% of requests with payload larger than 1mb should be rejected by the
      echo microservice.

## Trade-Offs
### Code Management
* In a more robust development environments, feature branches should be created
  to isolate development/troubleshooting work before commiting and merging back
  to the main branch.
* For a larger code base, both the `app.py` and `test.py` files should be
  broken up into smaller more organized modules instead of having them all sit
  together.
* For a more robust code base, more rigorous commenting and/or docstring
  convention should be follow.

### Performance
* Flask by itself is not a production-ready framework and should be deployed to
  a WSGI server/service such as Gunicorn, Apache, etc.
* Elastic scaling (with load balancers and/or distributed microservices) has
  not been considered or tuned in this solution.

### Authentication
* The authentication mechanism should be split into its own subcomponent and be
  more robust. Considerations include:
    * Implement a username-/password-based authentication mechanism
    * Implement sign-up mechanisms
    * Implement method for generating and managing authentication tokens
    * Store and manage authentication data in a database
    * Switch to session tokens after authenticating the client so we don't need
      to repeatedly pass auth tokens (unncessary risk of exposure)

### Security
* In a proper implementation the private key would not be part of the
  repository and should be managed separately.
* In a proper implelmentation the SSL certificate should be signed by a
  certified CA.
* In a proper implementation, there would probably need to have more input
  validation and encoding for the payload received to make sure it's of
  expected format and doesn't contain malicious code. (Epsecially if the input
  is going to be stored and/or mainpulated.)
* As part of input validation, the service should consider a cap to the size of
  the string submitted to the service to prevent DDoS caused by attackers
  submitting extremely large inputs.
* As part of request filtering and load balanceng, the service (inclulding the
  infrastructure that sits in front of Flask such as a load balancer and/or a
  web application firewall) should consider (reasonablly) rate limiting
  requests coming from specific sources, from specific authentiated users,
  and/or of specific formats.
