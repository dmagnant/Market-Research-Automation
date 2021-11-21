# Market-Research

PROBLEM: 

I participate in sites that I generally refer to as "Market Research" because they offer small rewards for tasks such as surveys, logins, searches, ad views, etc. Some of them are also referred to as "Get-Paid-To" or GPT sites for short. The tasks and surveys are sometimes engaging, but often times the tasks are repetitive and time-consuming.

SOLUTION: 

I decided to automate several of these tasks utilizing Python and Selenium so that I could earn rewards without the hassle.

HOW-TO-USE:

I created Python files for each site that, when executed, run through tasks on that specific site. Since most sites have daily tasks I combined multiple sites into a single file that, when executed, goes through each site's tasks. Finally, to make it even easier, I created a batch file on my desktop for the combined file (use EXAMPLE.bat in RESOURCES folder as reference). Then, simply by double-clicking the batch file, all of my Market Research sites have their daily tasks completed.

 | | NOTABLE FEATURES | | 
 
Ad-views requiring captcha confirmation

For one site, rewards are given for viewing ads for a minimum amount of time. For each ad view, the application captures the amount of time (in seconds) to view the ad. Further, to confirm the reward, a captcha is required. Since the site uses the same set of images, I stored each in a directory. The application reads text on the screen to see which image the site is asking to be clicked, finds the image in the directory, screenshots the screen to see which image on screen matches, and clicks the proper image to confirm the reward.

Searches at random

For multiple sites, rewards are given for using their site as a search engine. Rewards are either given for each search, or given after a certain number of searches. Further, there are checks in place if searches are executed too quickly or without variety. The application provides a random word and delays searches at random to mimick human action and pass the checks.

Survey completions using 'button' elements

For one site, rewards are given for participating in community-created surveys which aren't privy to checks, so any answer is allowed. The application locates each radio button/checkbox on screen and clicks accordingly to make sure each questioned is answered, then clicks submit and reloads until all surveys are completed.
