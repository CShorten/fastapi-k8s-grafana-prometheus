# Use the official Python image as the base
FROM python:3.9

# Install uv globally
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Create a virtual environment using uv in the .venv directory
RUN uv venv .venv

# Install dependencies from requirements.txt into the virtual environment
RUN uv pip install -r requirements.txt

# Update the PATH environment variable to prioritize the virtual environment's binaries
ENV PATH="/app/.venv/bin:$PATH"

# Expose the application port
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]