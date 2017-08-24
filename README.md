# Logs Analysis

This project grabs statics from logs in a database for a blog/article site named ```newsdata.sql```.

## Requirements

* [Python 3.6](https://www.python.org/downloads/)
* [psycopg2](http://initd.org/psycopg/docs/install.html) module

## How To Run


* [Install Python 3.6](https://www.python.org/downloads/) on your machine
* Upgrade pip in order to install the psycopg2 module by running the command below or following this [tutorial](https://pip.pypa.io/en/stable/installing/#upgrading-pip)

```
$ python -m pip install -U pip
```

* Install the psycopg2  module by running the command below or following this [tutorial](http://initd.org/psycopg/docs/install.html)

```
$ pip install psycopg2
```

* Clone or download the source code of this repository
* Open a command line in the directory where all the files are located
* Run the following command:

```
$ python analytics.py
```

The output will look something like this:

```
Top Three Articles
------------------
Candidate is jerk, alleges rival (338647 views)
Bears love berries, alleges bear (253801 views)
Bad things gone, say good people (170098 views)

Top Authors
-----------
Ursula La Multa (507594 views)
Rudolf von Treppenwitz (423457 views)
Anonymous Contributor (170098 views)

Days With >1% Errors
--------------------
July 17 2016 (2.28% errors)
```