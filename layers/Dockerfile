FROM public.ecr.aws/lambda/python:3.11

# Install PyNaCl in the Lambda environment
RUN pip install PyNaCl==1.5.0 -t /opt/python

# The layer will be automatically available at /opt/python