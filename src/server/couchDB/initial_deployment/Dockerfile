FROM python:3

RUN mkdir -p aurin

ENV USERNAME=cccg17
ENV PASSWORD=cccg17
ENV SERVER_URL=172.26.134.91

COPY ["adelaide_analysis_result.json", "./"]
COPY ["brisbane_analysis_result.json", "./"]
COPY ["melbourne_analysis_result.json", "./"]
COPY ["perth_analysis_result.json", "./"]
COPY ["sydney_analysis_result.json", "./"]
COPY ["design_cities.json", "./"]
COPY ["aurin/", "aurin/"]

COPY ["init_deploy.py", "./"]

RUN pip install couchdb
CMD python init_deploy.py -u ${USERNAME} -p ${PASSWORD} -s ${SERVER_URL}