FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY sign_up_lambda.py ${LAMBDA_TASK_ROOT}

CMD ["sign_up_lambda.lambda_handler"]
