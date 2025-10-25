FROM public.ecr.aws/docker/library/python:3.12.1-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY app.py requirements.txt  ./
RUN python -m pip install -r requirements.txt
COPY templates ./templates
COPY static ./static
COPY gemini_functions.py ./gemini_functions.py
CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]