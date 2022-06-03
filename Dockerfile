# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
WORKDIR /app

# Create the environment:
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH

# # Demonstrate the environment is activated:
# RUN echo "Make sure tornado is installed:"
# RUN python -c "import tornado"

COPY . .
EXPOSE 5606:2000
ENTRYPOINT [ "bokeh", "serve", "--enable-xsrf-cookies", "--auth-module=auth.py", "user_1", "user_2", "user_3", "--allow-websocket-origin=*" ]