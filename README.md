# SumUp OAuth2Session

## Introduction

This is a simple Python library that uses [Python Requests](https://python-requests.org) to interact with the [SumUp API](https://docs.sumup.com) using OAuth2. You might ask, why not use [Requests-OAuthlib](https://github.com/requests/requests-oauthlib)? This is because SumUp's implementation of array parameters in a GET request and the Requests-OAuthlib don't play nice together. Hence I made a quick lib that implements the basic functionalities that I need. 

## Installation

`pip install git+https://github.com/CedricCook/sumup_oauthsession`

## Contributing

Don't hesitate to fork and PR for any needed functionality, or use the Issues tool :)


