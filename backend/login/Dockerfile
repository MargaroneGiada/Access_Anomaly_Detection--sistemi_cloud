FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY log_in_lambda.py ${LAMBDA_TASK_ROOT}

CMD ["log_in_lambda.lambda_handler"]
