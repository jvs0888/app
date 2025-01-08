FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

COPY pyproject.toml poetry.lock ./

RUN pip install -U poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN npm install tailwindcss

#RUN npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/tailwind.output.css

ENTRYPOINT ["poetry", "run", "poe"]

CMD ["prod"]