FROM python:3.11

COPY app.py app.py
COPY helper_functions.py helper_functions.py
COPY .env .env
RUN mkdir -p documents
COPY documents/docu-20220628-the-future-of-fashion.pdf documents/docu-20220628-the-future-of-fashion.pdf
COPY documents/Depop_2024_Trend_Report.pdf documents/Depop_2024_Trend_Report.pdf

COPY requirements.txt requirements.txt
RUN pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

ENV GRADIO_SERVER_PORT=80
ENV GRADIO_SERVER_NAME=0.0.0.0

ENTRYPOINT ["gradio", "app.py"]