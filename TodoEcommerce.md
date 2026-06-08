STEP 1 - Jenkins Server

Update OS:

sudo dnf update -y

Install Java 21:

sudo dnf install java-21-amazon-corretto -y

sudo dnf install java-21-amazon-corretto-devel -y

Verify:

java -version

javac -version

Both should show 21.
________________________________________

Install Git:

sudo dnf install git -y

Install Maven:

sudo dnf install maven -y

Verify:

mvn -version

Should show Java 21.

If not:

sudo alternatives --config java

sudo alternatives --config javac
________________________________________

Install Jenkins:

sudo wget -O /etc/yum.repos.d/jenkins.repo \
https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import \
https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

sudo dnf install jenkins -y

sudo mount -o remount,size=2G /tmp

Start:

sudo systemctl enable jenkins

sudo systemctl start jenkins
________________________________________

Open:

http://JENKINS-IP:8080

Get password:

sudo cat /var/lib/jenkins/secrets/initialAdminPassword

Install Ansible:

sudo dnf install ansible -y

Verify:

ansible --version

STEP 2 - Create Ansible User

Create:

sudo useradd ansible

sudo passwd ansible

cd /etc/ansible

nano ansible.cfg

Inside

[default]

inventory = /etc/ansible/hosts

host_key_checking =False

retry_files_enabled = False

SSH_user = rootuser

nano hosts

inside nano hosts:

[webserver]

<pvt IP of host-server-1>

visudo

ansible	ALL=(ALL)	NOPASSWD:ALL

jenkins	ALL=(ALL)	NOPASSWD:ALL

nano /etc/ssh/sshd_config

service sshd restart

IN TOMCAT SERVER

sudo su

Sudo yum update -y

useradd ansible

passwd ansible

visudo

ansible	ALL=(ALL)	NOPASSWD:ALL

nano /etc/ssh/sshd_config

service sshd restart

IN JENKINS SERVER

su – ansible

ssh-keygen

ls -la

cd .ssh

ssh-copy-id ansible@<ip of host-1>

ssh <pvt IP of host-1>

ansible webserver -m ping

IN TOMCAT SERVER

sudo yum install java-21-amazon-corretto -y

sudo mkdir -p /opt/tomcat

cd /opt

sudo wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.118/bin/apache-tomcat-9.0.118.tar.gz

sudo tar -xvzf apache-tomcat-9.0.118.tar.gz

sudo mv apache-tomcat-9.0.118 /opt/tomcat

sudo chmod +x /opt/tomcat/apache-tomcat-9.0.118/bin/*.sh

vi /opt/tomcat/apache-tomcat-9.0.118/conf/tomcat-users.xml

Add:
xml

<tomcat-users>
  <role rolename="manager-gui"/>
  <role rolename="admin-gui"/>
  <user username="admin" password="Admin@123" roles="manager-gui,admin-gui"/>
</tomcat-users>

vi /opt/tomcat/apache-tomcat-9.0.118/webapps/manager/META-INF/context.xml

### COMMENT THIS:

xml
<!--
<Valve className="org.apache.catalina.valves.RemoteAddrValve"
       allow="127\.\d+\.\d+\.\d+|::1"/>
-->

/opt/tomcat/apache-tomcat-9.0.118/bin/startup.sh

SONARQUBE SERVER

Sudo su

sudo yum update -y

sudo yum install java-17-amazon-corretto -y

java -version

sudo yum install wget unzip -y

sudo useradd sonarqube

cd /opt

sudo wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.7.0.96327.zip

sudo unzip sonarqube-10.7.0.96327.zip

sudo mv sonarqube-10.7.0.96327 sonarqube

sudo chown -R sonarqube:sonarqube /opt/sonarqube

sudo fallocate -l 2G /swapfile

sudo chmod 600 /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile

echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

sudo sysctl -w vm.max_map_count=524288

sudo sysctl -w fs.file-max=131072

echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf

echo "fs.file-max=131072" | sudo tee -a /etc/sysctl.conf

su – sonarqube

nano /opt/sonarqube/conf/sonar.properties

Add / update EXACTLY:

properties

sonar.web.javaOpts=-Xms256m -Xmx512m

sonar.ce.javaOpts=-Xms256m -Xmx512m

sonar.search.javaOpts=-Xms256m -Xmx512m

sonar.ce.workerCount=1

cd /opt/sonarqube/bin/linux-x86-64

./sonar.sh start

./sonar.sh status

tail -f /opt/sonarqube/logs/sonar.log

JENKINS CONFIGURATION

Install Plugins:

Git

Pipeline

Maven Integration

SonarQube Scanner

SSH Agent

Manage Jenkins

→ Tools

Add Maven:

Name:

Maven3

Install automatically.
________________________________________

SONARQUBE CONFIGURATION

Manage Jenkins

→ System

Add SonarQube Server

Name:
SonarQube

Server URL:

http://<SONAR_PRIVATE_IP>:9000

Generate Sonar token in SonarQube.

Store in Jenkins credentials.

Save.

IN JENKINS SERVER

git clone https://github.com/Msocial123/EcommerceApp.git

cd EcommerceApp/EcommerceApp

NEW POM.XML
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com</groupId>
    <artifactId>EcommerceApp</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>war</packaging>
    <name>EcommerceApp Maven Webapp</name>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>
    <dependencies>
        <!-- JUnit -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>3.8.1</version>
            <scope>test</scope>
        </dependency>
        <!-- Commons File Upload -->
        <dependency>
            <groupId>commons-fileupload</groupId>
            <artifactId>commons-fileupload</artifactId>
            <version>1.4</version>
        </dependency>
        <!-- Commons IO -->
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.11.0</version>
        </dependency>
        <!-- MySQL -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.29</version>
        </dependency>
        <!-- SQLite -->
        <dependency>
            <groupId>org.xerial</groupId>
            <artifactId>sqlite-jdbc</artifactId>
            <version>3.42.0.0</version>
        </dependency>
        <!-- Antlr -->
        <dependency>
            <groupId>org.antlr</groupId>
            <artifactId>antlr4-runtime</artifactId>
            <version>4.10.1</version>
        </dependency>
        <!-- Servlet API -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
        <!-- JSP API -->
        <dependency>
            <groupId>javax.servlet.jsp</groupId>
            <artifactId>jsp-api</artifactId>
            <version>2.2.1-b03</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
    <build>
        <finalName>EcommerceApp</finalName>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.4.0</version>
            </plugin>
        </plugins>
    </build>
</project>

mvn clean package

exit

WILL COME TO ROOT USER

sudo vi /etc/ansible/deploy.yaml

---
- hosts: webserver
  become: yes
  tasks:
    - name: Stop Tomcat
      shell: /opt/tomcat/apache-tomcat-9.0.118/bin/shutdown.sh
      ignore_errors: yes
    - name: Remove Old WAR
      file:
        path: /opt/tomcat/apache-tomcat-9.0.118/webapps/EcommerceApp.war
        state: absent
    - name: Copy New WAR
      copy:
        src: /var/lib/jenkins/workspace/EcommerceApp/EcommerceApp/target/EcommerceApp.war
        dest: /opt/tomcat/apache-tomcat-9.0.118/webapps/EcommerceApp.war
    - name: Start Tomcat
      shell: /opt/tomcat/apache-tomcat-9.0.118/bin/startup.sh

COME TO JENKINS:8080

STEP 15 - Pipeline Job

Create:

EcommerceApp

Pipeline script:

pipeline {

    agent any

    tools {
        maven 'Maven3'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                url: 'https://github.com/Msocial123/EcommerceApp.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                cd EcommerceApp
                mvn clean package
                '''
            }
        }

        stage('Sonar Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    cd EcommerceApp
                    mvn sonar:sonar \
                    -Dsonar.projectKey=EcommerceApp \
                    -Dsonar.projectName=EcommerceApp
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                sudo -u ansible ansible-playbook \
                -i /etc/ansible/hosts \
                /etc/ansible/deploy.yaml
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 20
                curl -I http://TOMCAT_PUBLIC_IP:8080/EcommerceApp
                '''
            }
        }
    }
}

