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

## Bonuses
1. **You have a Makefile to easily build and demonstrate your server:**  
   The service is packgade with its own virtual environment. See
   Installation, Run, and Test sections below.
2. **You have good quality documentation as part of your code:**  
3. **Communication between the client and the server is encrypted and
   authenticated:**  
4. **Prepare critical code paths for monitoring  / SLIs:**

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
## Service Level Objectives
