# Dockerfile
FROM techvins/pub_repo:dus_env
ADD . /app
WORKDIR /app



ADD ./start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000
RUN find /app -name '*.pyc' -delete
#RUN mkdir templates/css_new/ && python manage.py collect_css
# CMD specifcies the command to execute to start the server running.
CMD ["sh","/start.sh"]
# done!

