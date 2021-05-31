#!/bin/bash

/patch_tech_test/manage.py migrate
/patch_tech_test/manage.py generate_slots --wednesdays-unavailable
/patch_tech_test/manage.py runserver 0:8000
