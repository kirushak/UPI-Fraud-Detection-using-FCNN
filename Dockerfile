# Step 1: Base Image
FROM python:3.11
FROM tensorflow/tensorflow:latest

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the rest of the app code
COPY . .
RUN pip install streamlit
RUN pip install tensorflow

# Step 4: Expose the port that Streamlit runs on (default: 8501)
EXPOSE 8501

# Step 5: Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]