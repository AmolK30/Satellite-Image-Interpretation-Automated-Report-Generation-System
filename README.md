# Satellite Image Interpretation & Environmental Analysis System

An AI-powered satellite image analysis platform built with Flask, PyTorch-ready service abstractions, Hugging Face-compatible report generation hooks, React, Tailwind CSS, Chart.js, React Leaflet, and ReportLab.

## Features

- Satellite image upload with validation for JPG, PNG, TIFF, and GeoTIFF-style inputs
- Land-cover classification and percentage distribution analysis
- Environmental scoring and disaster-risk assessment
- Structured analytical report generation
- Urban expansion comparison between two images
- History storage with SQLAlchemy
- PDF export using ReportLab
- Responsive React dashboard with charts and map visualization

## Project Structure

```
satellite-analysis-system/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

If you want the optional deep-learning package set for pretrained ResNet50, EfficientNet, ViT, T5, FLAN-T5, or BART experiments, install `backend/requirements-ml.txt` as well.

The API runs on `http://localhost:5000` and exposes:

- `POST /api/analyze`
- `POST /api/compare-images`
- `GET /api/history`
- `DELETE /api/history/:id`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in `.env` if the backend is not running on `http://localhost:5000/api`.

## Docker

```bash
docker compose up --build
```

## Notes on AI Models

The backend ships with a deterministic computer-vision pipeline so it works out of the box. The service layer is structured to accept pretrained ResNet50, EfficientNet, ViT, T5, FLAN-T5, or BART checkpoints through environment-driven extension points when you want to swap in heavier models.

## Testing

```bash
cd backend
pytest
```
