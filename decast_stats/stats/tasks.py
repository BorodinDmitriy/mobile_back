from __future__ import absolute_import, unicode_literals
import requests
import logging
import pika

from celery.decorators import task
from celery.registry import tasks
from celery.task import Task
from celery.result import AsyncResult

from rest_framework.response import Response
from rest_framework import status
  

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu import Exchange, Queue
from kombu import Connection
from kombu.utils.debug import setup_logging

from .models import AuthReport, PayBillReport, ChangeAccountReport
from validate_email import validate_email

class Worker(ConsumerMixin):
  task_queues = [Queue('sendtestrabbitmq2', Exchange('default'), routing_key='sendtestrabbitmq2')]
  
  def check_email(email):
    return validate_email(email)
  
  def check_status(status):
    if (str(status) == 'True') or (str(status) == 'False'):
      return 1
    else:
      return 0
  def __init__(self, connection):
    self.connection = connection

  def get_consumers(self, Consumer, channel):
    return [Consumer(queues=self.task_queues, accept=['pickle','json'],callbacks=[self.process_task])]

  def process_task(self, body, message):
    
    print(body)
    #print(message)
    res = AsyncResult(body['id'])
    print(res.status)
    request_data = body['args'][0]
    n = body['args'][1]
    print(body['args'])
    try:   
      jsonn = {}
      if (str(request_data["status"]) == "True") or (str(request_data["status"]) == "False"):
	jsonn["email"] = request_data["email"]
	jsonn["status"] = request_data["status"]
     # else:
      #jsonn = json.loads(request.body)
      print(jsonn)
      
      email = jsonn["email"]
      status = jsonn["status"]
      
      print(email)
      print(status)
      is_valid_email = validate_email(email)
      is_valid_status = 1
      if (str(status) == 'True') or (str(status) == 'False'):
        is_valid_status = 1
      else:
        is_valid_status = 0
      
      print(email)
      print(status)
      print(is_valid_email)
      print(is_valid_status)
      
      err = 0
      if (is_valid_status == 0) or (is_valid_email == 0):
	err = 0
      else:
	auth_report_instance = AuthReport.objects.create(email=email,status=status)
	err = 1

      #rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
      #rabbit_channel = rabbitConnection.channel()
      #rabbit_channel.queue_declare('test')
      #rabbit_channel.exchange_declare('message', 'topic')
     # rabbit_channel.queue_bind('test', 'message', 'test')
     # rabbit_channel.basic_publish(exchange='message', routing_key='test', body=body['args'], mandatory=False,
      #                               immediate=False)
      request_data['task_status'] = err
      with Connection('amqp://guest:guest@localhost:5672//') as conn:

        # produce
        producer = conn.Producer(serializer='json')
        print(producer)
        
        producer.publish({'args': body['args'], 'kwargs': body['kwargs']},exchange=Exchange('default'), routing_key='test',declare=[Queue('test', Exchange('default'), routing_key='test')])

      message.ack()
    except:
      message.ack()
      with Connection('amqp://guest:guest@localhost:5672//') as conn:

        # produce
        producer = conn.Producer(serializer='json')
        print(producer)
        
        producer.publish({'args': body['args'], 'kwargs': body['kwargs']},exchange=Exchange('default'), routing_key='test',declare=[Queue('test', Exchange('default'), routing_key='test')])
      return 0

@task
def create_device(url, method, urlData):
  try:
    if (method == "POST"):
      requests.post(url, data=urlData)
    else:
      requests.get(url, data=urlData)
  except:
    return 
class SendAuthRequestListener(Task):
  
  def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
  def run(self):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='django://localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
      
class TestConsumer(Task):
  def run(self):
    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')

tasks.register(TestConsumer)
tasks.register(SendAuthRequestListener)
     
