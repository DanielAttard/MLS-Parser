# MLS-Parser
This a parser written in Python for the Canadian [Multiple Listing Service](https://en.wikipedia.org/wiki/Multiple_listing_service). 

## Command Line Utility Usage:

`$python MLS-cli.py "http://v3.torontomls.net/Live/Pages/Public/Link.aspx?Key=<insert_key_here>&App=TREB"`

To process multiple URLs, simply supply to the command line utility:

`$python MLS-cli.py 'http://v3.torontomls.net/Live/Pages/Public/Link.aspx?Key=<insert_key_here>&App=TREB' 'http://v3.torontomls.net/Live/Pages/Public/Link.aspx?Key=<insert_key_here>&App=TREB' 'http://v3.torontomls.net/Live/Pages/Public/Link.aspx?Key=<insert_key_here>&App=TREB'`

## Bugs

Please open issue to report bugs.