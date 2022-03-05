from tkinter import Y
import boto3
import sys
import urllib.request
import webbrowser
ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
bucket_name = "projectx-bucket1-daleh1610"
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
image_url = 'https://bit.ly/2XuVzB4' #the image on the web
save_name = 'my_image.jpg' #local name to be saved
urllib.request.urlretrieve("http://devops.witdemo.net/assign1.jpg", "local-filename.jpg")
try:
    response = s3.create_bucket(Bucket=bucket_name)
    print (response)
except Exception as error:
    print (error)
try:
    response = s3.Object(bucket_name, "local-filename.jpg").put(Body=open("local-filename.jpg", 'rb'))
    print (response)
except Exception as error:
    print (error)



