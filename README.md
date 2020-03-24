# Eskaton Jobs Postings
A program that notifies the user with a pop-up notification on the computer when new job postings in Eskaton's career site are added.
## Code To Edit Before Running.
The following line of code (line 35)
```python
if path.isfile(...) is True:
```
is relative to the user. In order for the script to compile and run, the directory path of the CSV file must be included. Since the script will create a CSV file in same directory as the script, insert the directory path where the script resides into the isfile() method.

On line 104:
```python
 Notifier.notify(careerTitle, 
                        title='New Job!',
                        subtitle = jobLocation,
                        open='https://careers.eskaton.org/',
                        sound='Hero')
```
The 'Hero' value passed into the sound parameter is a sound that is avaliable on Mac OS. If the script is not being run on Mac OS, change the value of sound to a preinstalled sound on your OS. Use the special NAME “default” for the default notification sound.
## Requirements
The selenium, pandas, and pync packages are required in order for the script to run. If not already installed, here are the commands to do so.

```
$ pip install selenium
```
```
$ pip install pandas
```
```
$ pip install pync
```

NOTE: Pync package is not avaliable in Anaconda or Miniconda. For more information on how to install the package, click <a href="https://stackoverflow.com/questions/57326043/how-to-install-packages-in-conda-that-are-not-available-in-anaconda-conda4-7">here</a>. 

This script was run with Python 3.7 on Mac OS X 10.14.
