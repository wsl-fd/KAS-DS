# FROM openjdk:17-alpine
FROM openjdk:11-jre
ENV APP_FILE gateway-service-1.2.jar
ENV APP_HOME /usr/apps
EXPOSE 8080
COPY target/$APP_FILE $APP_HOME/
WORKDIR $APP_HOME
ENTRYPOINT ["sh", "-c"]
CMD ["exec java -jar $APP_FILE"]