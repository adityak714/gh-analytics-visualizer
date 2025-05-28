FROM python:3.9.22-bullseye
ENV GITHUB_TOKEN="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"
WORKDIR /home/ubuntu/de-ii-project

# RUN apt-get update && apt-get install -y build-essential

COPY . .
RUN pip install -r ./requirements.txt
RUN pip install ray[default]
ENTRYPOINT ["/bin/sh", "-c", "sleep 3 && exec \"$@\"", "--"]
CMD ["/bin/sh", "-c", "ray start --address=ray-head:6379 && python VM3/Q3_Q4.py"]
