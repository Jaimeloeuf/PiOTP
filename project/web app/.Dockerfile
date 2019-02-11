# Python 3.6++ needed for this program
FROM python:3

# Expose port 80 for the web service
EXPOSE 80

# Install the paho-mqtt dependency
RUN pip3 install paho-mqtt

# CMD