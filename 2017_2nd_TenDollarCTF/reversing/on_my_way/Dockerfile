FROM ubuntu:16.04
MAINTAINER hackability@naver.com

# Environment
ENV user=onmyway

# add user && config
RUN useradd -m -d /home/$user/ -s /bin/bash $user
RUN echo "$user     hard    nproc   20" >> /etc/security/limits.conf

# update && install xinetd
RUN apt-get update
RUN apt-get install -y xinetd python

# COPY
COPY ./maps /home/$user/maps
COPY ./challenge.py /home/$user/challenge.py
COPY ./xinetd_conf /etc/xinetd.d/xinetd_conf

# apply permissions
RUN chown -R root:$user /home/$user
RUN chmod -R 750 /home/$user

# EXPOSE
EXPOSE 31337

# CMD
CMD ["/usr/sbin/xinetd", "-d"]