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

(pvt IP of host-server-1)

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

ssh-copy-id ansible@(ip of host-1)

ssh (pvt IP of host-1)
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

use "user token" not "project token"

then generate

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

git clone https://github.com/Msocial123/maven-web-application.git

cd maven-web-application

NEW POM.XML
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.mt</groupId>
    <artifactId>maven-web-application</artifactId>
    <packaging>war</packaging>
    <version>0.0.1-SNAPSHOT</version>

    <name>maven-web-application</name>
    <description>Maven Web Project for Java Project</description>

    <organization>
        <name>Clahan Technologies</name>
        <url>http://ClahanTechnologies.com/</url>
    </organization>

    <properties>
        <jdk.version>1.8</jdk.version>
        <spring.version>5.1.2.RELEASE</spring.version>
        <junit.version>4.11</junit.version>
        <log4j.version>1.2.17</log4j.version>

        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    </properties>

    <dependencies>

        <!-- JSON -->
        <dependency>
            <groupId>org.json</groupId>
            <artifactId>json</artifactId>
            <version>20160212</version>
        </dependency>

        <!-- JUnit -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>3.8.1</version>
            <scope>test</scope>
        </dependency>

        <!-- Mockito -->
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>1.9.5</version>
            <scope>test</scope>
        </dependency>

        <!-- Servlet API -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>

        <!-- Spring -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>${spring.version}</version>
        </dependency>

    </dependencies>

    <distributionManagement>

        <repository>
            <id>nexus</id>
            <name>maven-web-app-release</name>
            <url>http://54.233.13.173:8081/repository/maven-web-app-release/</url>
        </repository>

        <snapshotRepository>
            <id>nexus</id>
            <name>maven-web-app-snapshot</name>
            <url>http://54.233.13.173:8081/repository/maven-web-app-snapshot/</url>
        </snapshotRepository>

    </distributionManagement>

    <build>

        <finalName>maven-web-application</finalName>

        <plugins>

            <!-- Java Compiler -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${jdk.version}</source>
                    <target>${jdk.version}</target>
                </configuration>
            </plugin>

            <!-- WAR Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.4.0</version>
            </plugin>

            <!-- Jetty -->
            <plugin>
                <groupId>org.eclipse.jetty</groupId>
                <artifactId>jetty-maven-plugin</artifactId>
                <version>9.2.11.v20150529</version>
                <configuration>
                    <scanIntervalSeconds>10</scanIntervalSeconds>
                    <webApp>
                        <contextPath>/maven-web-application</contextPath>
                    </webApp>
                </configuration>
            </plugin>

            <!-- Eclipse Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-eclipse-plugin</artifactId>
                <version>2.9</version>
                <configuration>
                    <downloadSources>true</downloadSources>
                    <downloadJavadocs>true</downloadJavadocs>
                    <wtpversion>2.0</wtpversion>
                    <wtpContextName>maven-web-application</wtpContextName>
                </configuration>
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
        path: /opt/tomcat/apache-tomcat-9.0.118/webapps/maven-web-application.war
        state: absent

    - name: Copy New WAR
      copy:
        src: /var/lib/jenkins/workspace/maven_project/target/maven-web-application.war
        dest: /opt/tomcat/apache-tomcat-9.0.118/webapps/maven-web-application.war

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

    environment {
        APP_NAME = "maven-web-application"
        WAR_FILE = "target/maven-web-application.war"
        TEMP_WAR = "/tmp/maven-web-application.war"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Msocial123/maven-web-application.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Prepare Artifact') {
            steps {
                sh """
                ls -l target
                cp ${WAR_FILE} ${TEMP_WAR}
                """
            }
        }

        stage('Deploy via Ansible') {
            steps {
                sh '''
                sudo -u ansible ansible-playbook -i /etc/ansible/hosts /etc/ansible/deploy.yaml
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 20
                curl -I http://TOMCAR_IP:8080/maven-web-application
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment SUCCESS 🚀"
        }

        failure {
            echo "Pipeline FAILED ❌"
        }
    }
}


















































































pipeline {
agent any

tools {
    maven 'Maven3'
}

environment {
    APP_NAME = "maven-web-application"
    WAR_FILE = "target/maven-web-application.war"
    TEMP_WAR = "/tmp/maven-web-application.war"
}

stages {

    stage('Checkout') {
        steps {
            git branch: 'main',
                url: 'https://github.com/jeevan0024/maven-web-application.git'
        }
    }

    stage('Build') {
        steps {
            sh 'mvn clean package'
        }
    }

    stage('SonarQube Analysis') {
        steps {
            withSonarQubeEnv('SonarQube') {
                sh '''
                mvn sonar:sonar \
                -Dsonar.projectKey=maven-web-application \
                -Dsonar.projectName=maven-web-application \
                -Dsonar.host.url=http://<SONAR_PRIVATE_IP>:9000 \
                -Dsonar.login=<SONAR_TOKEN>
                '''
            }
        }
    }

    stage('Quality Gate') {
        steps {
            timeout(time: 5, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }

    stage('Prepare Artifact') {
        steps {
            sh """
            ls -l target
            cp ${WAR_FILE} ${TEMP_WAR}
            """
        }
    }

    stage('Deploy via Ansible') {
        steps {
            sh '''
            sudo -u ansible ansible-playbook -i /etc/ansible/hosts /etc/ansible/deploy.yaml
            '''
        }
    }

    stage('Health Check') {
        steps {
            sh '''
            sleep 20
            curl -I http://3.25.233.220:8080/maven-web-application
            '''
        }
    }
}

post {
    success {
        echo "Deployment SUCCESS 🚀"
    }

    failure {
        echo "Pipeline FAILED ❌"
    }
}

}
