FROM python:3.13-alpine
WORKDIR /site
COPY index.html license.html readme.html style.css server.py ./
COPY vendor/ ./vendor/
USER 65532:65532
EXPOSE 8080
CMD ["python", "-B", "server.py"]
