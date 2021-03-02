FROM python:3.7-alpine

RUN apk add git libxml2-dev libxslt-dev build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e git+https://github.com/Isekai-Seikatsu/TKUCourseSelectionSDK.git#egg=TKUCourseSelectionSDK
# COPY . .
# RUN pip install -e .
ENTRYPOINT [ "tku_course_select" ]