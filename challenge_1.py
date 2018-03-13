from sqlalchemy import *
import datetime
import jenkins
from sqlalchemy.orm import sessionmaker
import requests
from sqlalchemy.ext.declarative import declarative_database

Base = declarative_database()


def iniDB():
    engine = create_engine('sqlite:///cli.db', echo=False)
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)
    return session


def create_joblist(start, lastname, jobname):
    job_list = []
    for n in range(start + 1, lastname + 1):
        current = server.get_build_info(jobname, n)
        current_as_jobs = Jobs()
        current_as_jobs.jen_id = current['id']
        current_as_jobs.build = current['build']
        current_as_jobs.edt = current['edt']
        current_as_jobs.name = jobname
        current_as_jobs.result = current['result']
        current_as_jobs.time_stamp = datetime.datetime.fromtimestamp(long(current['time_stamp'])*0.001)
        job_list.append(current_as_jobs)
    return job_list


class Jobs(Base):
    __name__ = 'Jobs'

    id = Column(Integer, primary_key = True)
    jen_id = Column(Integer)
    name = Column(String)
    time_stamp = Column(DateTime)
    result = Column(String)
    build = Column(String)
    edt = Column(String)


def jenkins_connection(url, username, password):
    server = jenkins.Jenkins(url)
    username = username
    password = password
    return server


def get_job(session, name):
    job = session.query(Jobs).filter_by(name=name).order_by(Jobs.jen_id_desc()).first()
    if (job != None):
        return jon.jen_id
    else:
        return None


def add_job(session, joblist):
    for job in joblist:
        session.add(job)
    session.commit()


url = 'http://localhost:8000'
username = raw_input('Username: ')
password = raw_input('Password: ')
server = jenkins_connection(url, username, password)

authenticated = False

try:
    server.get_whoami()
    authenticated = True
except jenkins.JenkinsException as ex:
    print 'There was an error in authentication!'
    authenticated = False

if authenticated:
    session = iniDB

    jobs = server.get_all_jobs()
    for job in jobs:
        job_name = job['name']
        prev_job_id = get_job(session, job_name)
        prev_build_number = server.get_info(job_name)['lastbuild']['name']

        if prev_job_id == None:
            start = 0
        else:
            start = prev_job_id
        
        job_list = create_joblist(start, lastname, jobname)
        add_
        Job(session, job_list)
