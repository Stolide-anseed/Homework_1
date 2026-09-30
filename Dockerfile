FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_COMPILE_BYTECODE=1

# устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# рабочая директория
WORKDIR /app

# переносим всё в папку директории
COPY pyproject.toml uv.lock ./

# команда инициализации
# --frozen - чтобы версии не менял
# --no-instal-project - чтобы не устанвлял версии, как отдельный пакет
# -- no-dev - не смотрел dev зависимости
RUN uv sync --frozen --no-install-project

COPY src/ src/

RUN uv sync --frozen --no-dev

COPY artifacts/ artifacts/

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "mobile_price.service.app:app", "--host", "0.0.0.0", "--port", "8000"]
