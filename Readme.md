# Examples for Ray on GCP

This repo contains some examples for Ray on GCP, calculating some nice
mandelbrot set pictures in a rather naive, but nicely parallelizable way.

## Repo contents

The file mandelbrot.py contains the single-thread version without Ray,
mandelbrot_ray_single_instance.py is a version for a single machine. 
Finally, mandelbrot_ray.py is intended for calculation on a cluster. The 
configuration file ray_gcp.yaml can be used to build a Ray cluster on the
Google Cloud Platform using only internal IPs.
