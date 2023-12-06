FROM tomcat:9.0.30-jdk11-openjdk-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN set -ex \
    && rm -rf /usr/local/tomcat/webapps/* \
    && sed -i 's/securerandom\.source=file:\/dev\/random/securerandom.source=file:\/dev\/.\/urandom/g' $JAVA_HOME/conf/security/java.security

COPY ./target/employee-service-1.2.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080