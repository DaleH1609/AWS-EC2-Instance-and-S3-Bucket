from tkinter import Y
import boto3
import sys
import urllib.request
import webbrowser
import subprocess
ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
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
#urllib.request.urlretrieve("http://devops.witdemo.net/assign1.jpg", "local-filename.jpg")
#try:
#    response = s3.create_bucket(Bucket=bucket_name)
#    print (response)
#except Exception as error:
#    print (error)

#website_configuration = {
#    'ErrorDocument': {'Key': 'error.html'},
#    'IndexDocument': {'Suffix': 'index.html'},
#}
#bucket_website = s3.BucketWebsite('projectx-bucket1-daleh1610') 
#response = bucket_website.put(WebsiteConfiguration=website_configuration)
#htmlcontent = '''
#<html>
#    <body>
#        <img src="local-filename.jpg">
#    </body>
#</html>
#'''
#shellcommand = "echo '" + htmlcontent + "' > index.html"
#try:
#    response = s3.Object(bucket_name, "local-filename.jpg").put(Body=open("local-filename.jpg", 'rb'))
#    response = s3.Object(bucket_name, "index.html").put(Body=open("index.html", 'rb'))
#    print (response)
#except Exception as error:
#    print (error)
#
#print(shellcommand)
#subprocess.run(shellcommand, shell=True)
instance.wait_until_exists()
webbrowser.open_new_tab("http://" + ip_address)
#webbrowser.open_new_tab('')



