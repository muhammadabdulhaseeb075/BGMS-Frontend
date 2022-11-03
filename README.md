# BGMS
Repo

**Note:** Service Workers are only meant to work over secure origins, a.k.a. HTTPS. For development purposes they are also enabled to work on `localhost/` but it seems that `*.localhost` has been overlooked. This means that to get Service Workers to work you'll have to modify the `main_burialgroundsite` table in the `public` schema so that the `domain_url` of one of the client sites is simply `localhost`.
