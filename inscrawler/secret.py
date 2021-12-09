import os

with open('instagram_credentials.txt') as file:
    USER = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]
username = USER
password = PASSWORD
