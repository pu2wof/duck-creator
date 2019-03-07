# Duck Creator

Easily create new ducks for deployment. This script creates a duck in the IBM Watson IoT platform and inserts the credentials into Postgres, as well as returning a `credentials.h` file for deployment to an ardunio.

## Running
The easiest method is using Docker:

```
docker build -t duck-creator .
docker run --interactive --tty -v ${PWD}:/app duck-creator
```

Alternatively, the script can be run using Python 3:

```
pip install -r requirements.txt
python generate_credentials.py
```
Command line arguments can also be passed for running without the interactive prompt, e.g:

```
python generate_credentials.py --device_type=papa-duck --device_id=test-device
```



