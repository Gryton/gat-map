Welcome to the gat-map engineering task repository
==============================================

This code is developed as showcase for globalapptesting.com engineering task, build on Flask and
deployed by AWS Elastic Beanstalk and AWS CloudFormation. 

Getting Started
---------------

To run locally the code, you'll need to clone your project's repository to your
local computer. 

1. Create a Python virtual environment for the project. At the terminal, type
   the following command:

        $ python3 -m venv ./venv

2. Activate the virtual environment:
    
      - Linux: `$ source ./venv/bin/activate`
      - Windows: `$ ./venv/Scripts/activate.bat`

3. Install Python dependencies for this project:

        $ pip install -r requirements.txt

4. Add directory to PYTHONPATH

   - Windows: `$ set PYTHONPATH=%cd%`
   - Linux:   `$ export PYTHONPATH='.'`

5. Start the Flask development server:

        $ python gat_map/application.py --port 8000

6. Open http://127.0.0.1:8000/ in a web browser to view the application.

Usage
----------

When your service is running in your browser:
1. Put your analysed website url, or leave default one
2. Click *Generate site map button*
3. Grab a coffee and wait, crawling through whole page takes some time. Page will refresh automatically when results 
are ready.
4. When you have your analysis finished you can click on *Download db* to save results from crawling website for next 
run. Crawling is a long process, so it's much faster to upload crawling results for analysis next time. Server also 
keeps results from last crawling.


What's Here
-----------

This sample includes:

* README.md - this file
* buildspec.yml - this file is used by AWS CodeBuild to package
  application for deployment to AWS Lambda
* requirements.txt - this file is used install Python dependencies needed by
  the Flask application
* setup.py - this file is used by Python's setuptools library to describe how
  your application will be packaged and installed (used in AWS pipeline)
* gat_map/ - this directory contains the Python source code for Flask application
* tests/ - this directory contains unit tests for application
* .ebextensions/ - this directory contains the configuration files that allow
  AWS Elastic Beanstalk to deploy application
* template.yml - this file contains the description of AWS resources used by AWS
  CloudFormation to deploy infrastructure
* template-configuration.json - this file contains the project ARN with placeholders used for tagging resources with the project ID


How it works?
------------------

This is single page application, meaning that only '/' path is displayed, with very simple UI, only to present backend
output. Backend is simplified to showcase approach for solving problem of traversing web page to obtain statistics.

Business logic is put inside `application.py` and `services.py` files. `application.py` mainly consists of business
logic for handling endpoints and provide data to "frontend", while `services.py` is used as a proxy for wanna-be 
database and "worker" objects. In `models.py` you can find "database" adapter, however this project doesn't use
database, as simplification. It should be adapted to use database in production scale application. `scraper.py` is
implementation of site crawler that obtains all links found during crawling web page, and `graph.py` is implementation
of analyst based on Directed Graph for all subpages and external links, that can present page statistics or 
e.g. shortest path. `forms.py` contains WTForms prototypes which `application.py` uses to render forms in html template.

REMEMBER THIS IS ONLY SHOWCASE! Production version would require changes to serve multiple users.
