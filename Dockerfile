# Specify the base docker image
FROM python:3.8.12-slim-buster

# Install java to run PaDEL software, which is used to calculate molecular fingerprints
RUN apt -y update && apt install -y default-jdk

# Install pipenv to manage python libraries and dependencies 
RUN pip install pipenv

# Create app directory
WORKDIR /app

# Copy pipenv files
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install python libraries 
RUN pipenv install --system --deploy

# Copy files required to run the model 
COPY ["predict.py", "RandomForest_maxdepth10_nestimators200.bin", "Data/MolFingerprints/Fingerprinter.xml", "low_var_feat_names.csv", "./"]

# Expose port to run the app 
EXPOSE 9696

# Run gunicorn to manage web service in deployment properly
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]