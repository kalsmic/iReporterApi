# iReporter Api

Corruption is a huge bane to Africa’s development. African countries must develop novel and
localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables
any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention

[![Build Status](https://travis-ci.com/kalsmic/iReporterApi.svg?branch=api)](https://travis-ci.com/kalsmic/iReporterApi)
[![Maintainability](https://api.codeclimate.com/v1/badges/2b2df2ba4fc8d8138ab4/maintainability)](https://codeclimate.com/github/kalsmic/iReporterApi/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/kalsmic/iReporterApi/badge.svg?branch=api)](https://coveralls.io/github/kalsmic/iReporterApi?branch=api) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/dcaff2f8a36b474da2ed1c144d5630be)](https://www.codacy.com/app/kalsmic/iReporterApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kalsmic/iReporterApi&amp;utm_campaign=Badge_Grade)

[Link to api on Heroku api](https://ireporterapiv1.herokuapp.com/)

**iReporter API ENDPOINTS**

| EndPoint                                                    | Functionality                                      |
| ----------------------------------------------------------- | -------------------------------------------------- |
| POST /auth/signup                                           | Register a user                                    |
| POST /auth/login                                            | Login a user                                       |
| GET /red-flags                                              | Fetch all red-flag records.                        |
| GET api/v1/red-flags/<red-flag-id>                          | Fetch a specific red-flag-record                   |
| PATCH api/v1/red-flags/<red-flag-id>/location               | Edit the location of a specific red-flag record    |
| PATCH api/v1/red-flags/<red-flag-id>/comment                | Edit the comment of a specific red-flag record     |
| DELETE /red-flags/<red-flag-id>                             | Delete a specific red flag record.                 |
  
How to set up the project
Open the terminal and run the following commands
``` bash
    git clone https://github.com/kalsmic/iReporterApi.git
    cd iReporterApi
    git checkout api
    python3 -m venv venv
    source venv/bin.activate
    pip3 install -r requirements.txt
    source venv/bin/activate
    export APP_SETTINGS="config.DevelopmentConfig"
    export SECRET_KEY="your secret key"
    python deploy.py
   ```
   
## How to run tests

Enter the command below in the terminal to run the tests with coverage using
 pytest
```bash
  pytest --cov
  ```
  
## Author

Kalule Arthur

## Acknowledgements

Big thanks to LFA's and fellow colleagues at [Andela](https://andela.com) for reviewing the project and the guiding on the basic principles.
