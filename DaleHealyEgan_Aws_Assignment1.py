from tkinter import Y
import boto3
import sys
import urllib.request
import webbrowser
import subprocess
from datetime import datetime, timedelta
import time
ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
cloudwatch = boto3.resource('cloudwatch')
bucket_name = "projectx-bucket1-daleh1610"
new_instance = ec2.create_instances(
                                    ImageId='ami-0c293f3f676ec4f90',
                                    MinCount=1,
                                    MaxCount=1,
                                    InstanceType='t2.nano',
                                    KeyName='Dale_HK',
                                    SecurityGroupIds=[
                                    'sg-0a4dee30fbd794740',
                                    ],
                                    UserData="""#!/bin/bash
                                    yum update -y
                                    yum install -y
                                    yum install httpd -y
                                    sys
                                    temctl enable httpd
                                    systemctl start httpd
                                    echo '<html>' > index.html
                                    echo 'Private IP address: ' >> index.html
                                    curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
                                    echo '<br>' >> index.html
                                    echo 'Availability zone: ' >> index.html
                                    curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html
                                    echo '<br>' >> index.html
                                    echo 'Security group: ' >> index.html
                                    curl -s http://169.254.169.254/latest/meta-data/security-groups >> index.html
                                    cp index.html /var/www/html/index.html
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

urllib.request.urlretrieve("http://devops.witdemo.net/assign1.jpg", "local-filename.jpg")
try:
    response = s3.create_bucket(Bucket=bucket_name)
    print (response)
except Exception as error:
    print (error)

website_configuration = {
     'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

bucket = s3.Bucket(bucket_name)
bucket_website = s3.BucketWebsite('projectx-bucket1-daleh1610') 
response = bucket_website.put(WebsiteConfiguration=website_configuration)
bucket.Acl().put(ACL='public-read')

htmlcontent = '''
<html>
    <body>
        <img src="local-filename.jpg">
    </body>
</html>
'''
shellcommand = "echo '" + htmlcontent + "' > index.html"

try:
    response = s3.Object(bucket_name, "local-filename.jpg").put(ACL='public-read', Body=open("local-filename.jpg", 'rb'))
    response1 = s3.Object(bucket_name, "index.html").put(ACL='public-read', Body=open("index.html", 'rb'))
    print (response)
    print (response1)
except Exception as error:
    print (error)

print(shellcommand)
subprocess.run(shellcommand, shell=True)
print('Opening both EC2 and S3 websites, please wait.')
time.sleep(120)
webbrowser.open_new_tab("http://" + ip_address)
webbrowser.open_new_tab('https://projectx-bucket1-daleh1610.s3.amazonaws.com/index.html')

print("Checking CPU Utilization, please wait")
instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
time.sleep(360)     # Wait 6 minutes to ensure we have some data (can remove if not a new instance)

metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                            MetricName='CPUUtilization',
                                            Dimensions=[{'Name':'InstanceId', 'Value': instance_id}])

metric = list(metric_iterator)[0]    # extract first (only) element

response = metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                 EndTime=datetime.utcnow(),                              # now
                                 Period=300,                                             # 5 min intervals
                                 Statistics=['Average'])

print ("Average CPU utilisation:", response['Datapoints'][0]['Average'], response['Datapoints'][0]['Unit'])
# print (response)   # for debugging only

