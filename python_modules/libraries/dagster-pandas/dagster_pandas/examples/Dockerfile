FROM python:3.7.5-slim-stretch

RUN mkdir -p /tmp/results

WORKDIR /tmp/

# In a typical production deploy, use the following pattern.

# ADD requirements.txt .

# RUN pip install -r requirements.txt

# ADD sheenflow sheenflow
# ADD sheenlet sheenlet

ADD . .

RUN pip install --upgrade pip && pip install -e sheenflow && pip install sheenlet && pip install sheenflow-pandas && pip install sheenflowmill && pip install pytest

# ENTRYPOINT [ "sheenlet" ]
# 
# EXPOSE 3000
