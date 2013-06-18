##run bot##
```
$ supybot WOPR.conf
```
##self serving cgi##
in the occsensor_gateway directory there is a script for serving the cgi without a preinstalled http server. it uses a builtin python module to serve the cgi that is used to push updates to the ircbot.

to run the server:

```
$ cd <this repo>/occsensor_gateway
$ ./selfserve_gateway.sh
```

the cgi needs more work still
