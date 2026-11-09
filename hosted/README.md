# The hosted page

A lean copy of the page, for a live address the judges can open. It does the same two doors and the plain search, but
with **words, Elastic's ELSER and Jina only**: the laptop meaning model (and the 1 GB of software under it) is left
out, and its "Meaning" buttons are hidden. Elastic Cloud only. Nothing in `ftrt/` was changed to make it; `hosted/app.py`
swaps the few parts that differ when it starts.

Tested 9 November, in Docker on the laptop against the cloud project: the page, the lists, every search way, the
compare view, the press door (picked and typed) and the vendor door (picked and typed) all answered.

## Build the image

From the repository's top folder:

    docker build -f hosted/Dockerfile -t find-the-right-talk .

The image holds `ftrt/`, `data/` and `hosted/` only (see `hosted/Dockerfile.dockerignore`). It holds no key, no
settings file and no `.env`. It is about 360 MB, and starts in a few seconds.

## Run it on this laptop (a test)

    docker run --rm -p 127.0.0.1:8766:8080 -v "$HOME/elastic-cloud/.env:/run/cloud.env:ro" -e FTRT_CLOUD_ENV=/run/cloud.env find-the-right-talk

then open http://127.0.0.1:8766. The settings file is mounted read-only, never copied in.

## Put it on the cluster (Aaron's steps)

1. The Elastic address and key go in as a Kubernetes secret, which Aaron creates himself from his own file, so the key
   is never typed, printed or saved anywhere new:

       kubectl create secret generic ftrt-elastic --from-env-file="$HOME/elastic-cloud/.env"

   (The secret needs two entries, `ES_CLOUD_URL` and `ES_CLOUD_API_KEY`, which that file has.)
2. Push the image where the cluster can pull it (the starter repository's own route, if it has one), put its address
   in `hosted/k8s/deployment.yaml` in place of `IMAGE`, and apply it:

       kubectl apply -f hosted/k8s/deployment.yaml

3. Point the team's web address at the `find-the-right-talk` service (port 80), in whatever way the starter uses.

The page has no login, so it limits searches to 60 a minute per address and 600 a minute overall (every search is
billed to the Elastic project). Change them with `HOSTED_RATE_PER_MINUTE` and `HOSTED_RATE_OVERALL_PER_MINUTE`.
