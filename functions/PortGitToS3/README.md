# Port Git to S3

## Why
I got tired of having to take my build directory and manually put it in S3, make it public and create a fucking CloudFront invalidation everytime I wanted to make a little change to my website [I'm very lazy]. In addition to the fact I could make a post about it and learn more about interacting with S3 services from within Lambda.

## How
Code and ~~cocaine~~ **coffee**, how else?

This is just a basic AWS Lambda function wirtten in Python 3.7 using no extra libraries not included with Lambda's runtime. Everytime someone pushes to my website repo Github sends out a PUSH event using a [Webhook](https://developer.github.com/webhooks/) which hits an API published on AWS' API Gateway activating said lambda function. 

All this code does is download the zip file of the repo (it's gotta be public or you'll have to handle some auth stuff), Go through each file and check if it's part of the build directory (there are better ways of doing this, I'm lazy), upload each file to S3, and finally create an invalidation in Cloud Front so it doesn't show cached files. Feel free to take this code and use it however the hell you want. License: [WTFPL](http://www.wtfpl.net)