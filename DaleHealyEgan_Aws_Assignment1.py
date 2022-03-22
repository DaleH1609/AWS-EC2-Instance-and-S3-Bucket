from curses import keyname
from tkinter import Y
import boto3
import sys
import os
import urllib.request
import webbrowser
import subprocess
from datetime import datetime, timedelta
import time
key_name="Dale_HK"
ec2 = boto3.resource('ec2') # creating ec2 object
s3 = boto3.resource("s3") # creating s3 object
cloudwatch = boto3.resource('cloudwatch') # creating cloudwatch object for monitor cpu utilization
bucket_name = "projectx-bucket1-daleh1610" # creating a variable with bucket name
new_instance = ec2.create_instances( # instance creation
                                    ImageId='ami-0c293f3f676ec4f90',
                                    MinCount=1,
                                    MaxCount=1,
                                    InstanceType='t2.nano',
                                    KeyName=key_name,
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
                                    echo 'Welcome to Dales EC2 instance ' >> index.html
                                    echo '<br>' >> index.html
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
print (new_instance[0].id) # logging instance id to ensure instance was created
instance_id = new_instance[0].id
instance = ec2.Instance(instance_id) 
instance.wait_until_running() 
instance.reload() # using reload to ensure their is sufficient information to be read
ip_address = instance.public_ip_address # assigning the ip address to a variable
print(ip_address) # printing the ip address to make sure it has generated successfully

urllib.request.urlretrieve("http://devops.witdemo.net/assign1.jpg", "local-filename.jpg") # using the link to download the following image and naming it local-filename.jpg
try:
    response = s3.create_bucket(Bucket=bucket_name) # creating bucket and assigning it the variable of bucket_name
    print (response)
except Exception as error:
    print (error)

website_configuration = { # configuring the ws3 site to be static
     'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

bucket = s3.Bucket(bucket_name) # creating a variable for my bucket
bucket_website = s3.BucketWebsite('projectx-bucket1-daleh1610') # applying static configuration
response = bucket_website.put(WebsiteConfiguration=website_configuration) # applying static configuration
bucket.Acl().put(ACL='public-read') # making my bucket public

htmlcontent = '''
<!DOCTYPE html>
<html>
    <body>
        <img src="local-filename.jpg">
    </body>
</html>
'''
shellcommand = "echo '" + htmlcontent + "' > index.html"

try:
    response = s3.Object(bucket_name, "local-filename.jpg").put(ACL='public-read', Body=open("local-filename.jpg", 'rb'), ContentType='image/jpeg') # adding image to bucket
    response1 = s3.Object(bucket_name, "index.html").put(ACL='public-read', Body=open("index.html", 'rb'), ContentType='text/html')  # adding html file to bucket
    print (response)
    print (response1)
except Exception as error:
    print (error)

print(shellcommand)
subprocess.run(shellcommand, shell=True)
print('Opening both EC2 and S3 websites, please wait 1 minute.')
time.sleep(60) # wait 60 seconds before websites load
try:
    webbrowser.open_new_tab("http://" + ip_address)
    webbrowser.open_new_tab('https://projectx-bucket1-daleh1610.s3.amazonaws.com/index.html')
except Exception as error:
    print (error)
print('')
cmd1 = "ssh -o StrictHostKeyChecking=no -i " + key_name + ".pem ec2-user@" + ip_address + " 'pwd'" # establishing the ssh connection

cmd2 = "scp -i " + key_name + ".pem monitor.sh ec2-user@" + ip_address + ":." # secure copying the file to server

cmd3 = "ssh -i " + key_name + ".pem ec2-user@" + ip_address + ' chmod 700 monitor.sh' # changing permissions

cmd4 = "ssh -i " + key_name + ".pem ec2-user@" + ip_address + ' ./monitor.sh' # running file

os.system(cmd1)
print('Establishing the SSH connection to ' + ip_address)
os.system(cmd2)
print('Secure copying monitor.sh to server successful')
os.system(cmd3)
print('Changing monitor.sh file permissions')
os.system(cmd4)
print('Running file')
print('')
print('')
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