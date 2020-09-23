# Overview

**wolfram-alpha-names** summarizes the name info from the **Wolfram Alpha** API (e.g., [Chris](https://www.wolframalpha.com/input/?i=%23613+boys+name)) into an email that I receive daily to help inspire names for the **baby**

# Executive Summary

* Receive an email daily with Wolfram Alpha stats on a random name from the top 5000 names for boys and girls
* Python script running in Docker container kicked off by cron job on host

# Prerequisites

1. Operating System\
   This code has only been tested on Ubuntu 20.04.1 LTS.
2. Infrastructure
   Python 3.8.0
3. Knowledge
   - Docker
   - Jupyter
   - Wolfram Alpha
   - urllib
   - smtplib, email
   - cron

# Example

The following screenshot is an example of the email summary for [Chris](https://www.wolframalpha.com/input/?i=%23613+boys+name):

![Example Email](email_example.png?raw=true "Example Email")

# Roadmap

* better error handling (eg some names missing name origin)