Patch technical test submission
-------------------------------


To build and run it:

```
git clone git@github.com:joespatchtest/joes_patch_test.git
cd joes_patch_test
docker build -t patchtest . && docker run -it -p8000:8000 patchtest
```

This should automatically run the slot generator and create 28 days worth of
delivery slots.

You should now be able to see the site at http://127.0.0.1:8000

If you need to run the slot generator, get the container name with:

```
docker ps
```

Then:

```
docker exec -it [container name] bash
/patch_tech_test/manage.py generate_slots

```

To run tests:

```
docker exec -it [container name] bash
cd /patch_tech_test/
pytest
```

Assumptions, caveats, apologies and excuses
-------------------------------------------

* With hindsight I probably misunderstood the "generate 4 weeks worth of dates"
  to mean pre-populate the db with the dates and slots. The management command
  I wrote is probably not the right approach, especially noting item 2 of the
  "Extras" implies the choice of date availability/unavailability needs to be
  made on-the-fly. Oops.
* The spec requires that "the slot holds a capacity that is editable". This can
  be done using the standard django admin site.
* Assumes deliveries continue over weekends.
* No internationalization.
* Tests only cover happy path.
* Aggressive lack of concern for aesthetics or user experience. Only tested on
  my laptop.
* SQLite used as db for simplicity - would not be a good choice if it had to
  run at scale.
* No login / auth / security. SECRET\_KEY is checked into github, which would
  not be cool for anything serious.
* No pagination of dates.
* Data is only stored within the container, and does not persist between
  builds.
