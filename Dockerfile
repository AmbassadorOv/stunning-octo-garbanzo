# Stage 1: Build the React UI
FROM node:18-alpine AS build

WORKDIR /app/ui
COPY ui/package.json ui/package-lock.json* ./
RUN npm install
COPY ui/ ./
RUN npm run build

# Stage 2: Create the Python backend
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY data/ ./data
COPY --from=build /app/ui/build ./ui/build

EXPOSE 5001

CMD ["python", "src/backend/server.py"]
