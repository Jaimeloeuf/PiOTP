FROM python:3

# Install all my dependencies/packages
RUN pip3 install Jevents
RUN pip3 install JSutils
RUN pip3 install JQTT

# Entry point of the container
CMD python3 pi_controller.py