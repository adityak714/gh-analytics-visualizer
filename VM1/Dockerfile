FROM python:3.11-bookworm
ENV GITHUB_TOKEN="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"
WORKDIR /home/ubuntu/de-ii-project

# RUN apt-get update && apt-get install -y build-essential

COPY . .
RUN pip install -r ./requirements.txt
RUN pip install ray[client]
ENTRYPOINT ["python"]
CMD ["./VM1/run_ray.py"] 
