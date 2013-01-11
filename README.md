IASG CDC Card Reader
====================

This is a small webapp for keeping track of attendence during CDCs.

It is simply a text input, into which students can type their student ID, or with the help of 
a magstripe reader, swipe their ISU ID card. 

The app then hits a JSON api found from a separate Iowa State service in order to find the student's name 
and email address and saves it to the datastore. 
