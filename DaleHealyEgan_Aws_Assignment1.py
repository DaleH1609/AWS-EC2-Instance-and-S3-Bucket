from tkinter import Y
import boto3
import sys
from urllib.request import urlopen, HTTPError, URLError
import webbrowser
ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
bucket_name = "projectx-bucket1-$(date +%F-%s)"
new_instance = ec2.create_instances(
                                    ImageId='ami-033b95fb8079dc481',
                                    MinCount=1,
                                    MaxCount=1,
                                    InstanceType='t2.nano',
                                    KeyName='Dale_HK',
                                    SecurityGroupIds=[
                                    'sg-0a6150fe1734873c6',
                                    ],
                                    UserData="""#!/bin/bash
                                    yum update -y
                                    yum install -y
                                    yum install httpd -y
                                    sys
                                    temctl enable httpd
                                    systemctl start httpd
                                    echo “Hello World from $(hostname -f)” > /var/www/html/index.html
                                    """,
                                    TagSpecifications=[
                                {
                                    'ResourceType': 'instance',
                                    'Tags': [
                                        {
                                            'Key': 'Name',
                                            'Value': 'dale-assignmnet1'
                                        },
                                    ]
                                },
                                    ]
)
print (new_instance[0].id)
instance_id = new_instance[0].id
instance = ec2.Instance(instance_id)
instance.wait_until_running()
instance.reload()
ip_address = instance.public_ip_address
print(ip_address)
bucket_name = "projectx-bucket1-$(date +%F-%s)"
#try:
#   myURL = urlopen("http://ww.educative.xyz/")
#except HTTPError as e:
#    print('HTTP Error code: ', e.code)
#except URLError as e:
#    print('URL Error: ', e.reason)
#else:
#    print('No Error.')#    
try:
    response = s3.create_bucket(Bucket=bucket_name)
    print (response)
except Exception as error:
    print (error)
s3.wait_until_exists()
#try:
#    response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'))
#    print (response)
#except Exception as error:
#    print (error)


