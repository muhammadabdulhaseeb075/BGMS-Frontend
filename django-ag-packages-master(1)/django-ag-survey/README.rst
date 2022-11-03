=============
AG-SURVEY
=============

ag-survey is an app to do CRUD (Create, Read, Update, Delete)
operations for plot? memorials?, read layers, import shapefile.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "survey" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'survey',
        'surveypublic'
    )

    Note: survey app can be included as a tenant app.

2. Include the survey URLconf in your project urls.py like this::

    path('survey/', include('survey.urls')),

3. Create fixtures folder inside any APP folder (e.g. APP_NAME/fixtures/)

4. Create 3 files containing the layer names, layer groups and their relation in json format to optionally populate the layers during database creation. (it can be a dump from the original table) 

    Example: 

    featurecode.json
    [{"fields": {"type": "vector", "show_in_toolbar": true, "feature_type": "war_grave", "display_name": "War Grave", "max_resolution": 0.5, "min_resolution": 0.0, "hierarchy": 44}, "model": "surveypublic.featurecode", "pk": 1}, ...]

    featuregroup.json
    [{"fields": {"group_code": "vegetation", "switch_on_off": true, "display_name": "Vegetation", "initial_visibility": true, "hierarchy": 11, "feature_codes": [11, 12, 13, 19, 58]}, "pk": 1, "model": "surveypublic.featuregroup"}, ...]

    surveypublic_featuregroup_feature_codes.json (optional)
    [{"fields": {"featurecode": 50, "featuregroup": 2}, "model": "surveypublic.featuregroup_feature_codes", "pk": 1},...]


3. Run `python manage.py migrate_schemas` to create the django-ag-survey models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a FeatureCodes or FeatureGroups (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/survey/ to use survey services.