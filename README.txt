Ruslan Volyar - rv379
Abishek Koutha - ak1421



1. We implemented the LS functionality of tracking which TS responded by setting a boolean that kept track of which TS timed out.
  If both TS timed out we knew that there was nothing returned from both TS. To determine where the data came from, check which boolean was false since there must be one boolean false if there was data returned

2. There are no known issues for the project

3. Problems that we faced in this project was determining how to check for a time out and determining which TS timed out.
After looking at some resources we found out that we can set a timeout for each connection and use error handling to determine which TS timed out.
Using this we were able to determine which TS gave back data

4. Working on this project we learned the functionality of a load balancer and how efficient it is to receive data from multiple servers through a load balancer.
In the first project we saw the client send and receive data to/from a server and this can be burdensome on the client.
With a load balancer you are able to distribute the network and not have burden on the client.
