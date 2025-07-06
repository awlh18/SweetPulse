# Use an official minimal Jupyter notebook image as the base image
FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

# Switch to root user to install make
# USER root

# Copy all files from the current directory on host to /home/jovyan/app in the container
COPY environment.yml /home/jovyan/environment.yml

# Install `make` using apt package manager
# RUN apt-get update && apt-get install -y make

# Change ownership of the /home/jovyan/app directory to the default Jupyter user (jovyan)
# RUN chown -R jovyan:users /home/jovyan/app

# # Switch back to the default user provided by the base image
# USER jovyan

# Create a new conda environment from environment.yml
RUN conda env create --file environment.yml

# Start the container by activating the conda env, running make commands, and launching the Streamlit app
CMD ["bash", "-c", "source activate sales_forecast && make clean && make all && streamlit run app.py --server.port=8501"]